"""核心任务生成器：p.txt 风格的直接 prompt，一次 LLM 调用生成 question + answer。"""
import json
import random
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from bench.data_model.message import UserMessage
from bench.environment.toolkit import ToolKitBase, get_tool_signatures
from bench.utils.llm_utils import extract_json_from_llm_response, generate
from loguru import logger
# ──────────────────────────────────────────────
# L1 / L2 / L3：按「工具链复杂度 + 信息依赖」分级，题材不限定
# （口语、不泄工具名、参数来自数据等硬约束见 _PROMPT_TEMPLATE）
# ──────────────────────────────────────────────

_LEVEL_INSTRUCTIONS = {
   "L1": """【L1｜明确指令与单点直达】
- 业务目标：员工随口问一个具体的小事，或者下达一个明确的单次操作指令。无需复杂的中间推理。
- 逻辑特征：系统只需要“定位人/物” -> “查一条数据或改一个状态”。最多 2-3 步，纯线性流转。""",


    "L2": """【L2｜单条依赖链与隐式判断】
- 业务目标：处理一个带有明确上下文依赖的办公问题。用户通常只提出一个工作诉求，但要先确认某个关键信息，后续动作或结论才能成立。
- 逻辑特征：任务通常包含 3-4 步，核心是一条连续的信息依赖链。后一步的查询对象、操作对象或判断依据，必须来自前一步的真实结果。
- 说明：L2 可以包含业务判断，但这种判断应自然隐藏在任务语境中，而不是把问题写成“如果 A 就做 B”的显式规则。""",

    "L3": """【L3｜多阶段闭环与复杂依赖】
- 业务目标：处理一个表面自然、实际涉及多个对象、多个环节或多个条件的复杂办公问题。
- 逻辑特征：通常需要 5 步及以上，且不能只是机械串联。任务中应包含以下至少两类结构：多对象筛选、跨实体信息传递、条件分支、执行后验证、异常补救、结果汇总。
- 说明：L3 不限定为 Leader 视角，也不强制要求聚合盘点；盘点、排查、批量处理、跨系统流转、补救闭环等都可以属于 L3。""",
}

_PROMPT_TEMPLATE = """你是一位资深的企业业务架构师和真实办公场景还原专家。你的目标是基于给定的公司数据和系统工具，生成一个【真实、自然、逻辑严密】的办公求助任务。

=== 提问者身份（caller）===
{caller_info}
（提示：提问者在和客服/系统对话时，默认对方知道自己是谁，不用刻意自我介绍，直接说事。）

=== 任务难度与结构目标 ===
{level_instruction}

=== 可用系统工具 ===
{tool_signatures}

=== 真实公司数据切片 ===
{data_slice}

=== 公司业务规则（生成任务时必须遵循）===
{business_rules}

=== Few-shot 参考样例 ===
{few_shot_block}

=== 跨域约束 ===
{cross_domain_requirement}

=== 任务目标 ===
1. 你要生成的不是“题面”，而是一段真实员工发给 AI/助手的消息或工作指令。
2. question 可以很短，也可以在复杂场景下像 GAIA 任务那样写得更长、更完整；允许包含背景、限制条件、期望交付物和异常兜底要求。
3. 无论长短，question 都必须像人话，像工作软件里的真实消息，而不是像评测样题或解题提示。

=== 高优先级生成原则（必须同时满足）===
1. 先有真实诉求，再有工具链：
   - question 必须先有明确的业务目标，再去承载后续推理链。
   - 任务中的每一步都必须有真实业务必要性，不能为了增加复杂度而硬拼。
2. 像消息或指令，不像解题提示：
   - 提问者是在交代一件事、推动一个结果、补一个信息缺口，而不是在教 Agent 应该怎么做。
   - 可以提出结果要求、时间要求、格式要求、异常处理要求，但不要把中间求解顺序写成“先查X，再查Y，最后算Z”。
3. 动机必须真实：
   - 用户为什么要问这个问题，必须符合真实办公语境。
   - 不要生成“人类通常不会这样问”的诉求，尤其不要无缘无故查询他人隐私信息、全年汇总信息或不自然的跨实体统计。
4. 复杂度要自然外露：
   - 简单任务可以一句话说清，复杂任务可以完整展开。
   - 高质量复杂任务的难点应来自真实上下文、限制条件、隐含依赖和闭环动作，而不是来自生硬的“盘点、汇总、顺手再查、合计”。

=== ⚠️ 绝对不可触碰的红线（Anti-patterns）===
1. 禁止指令泄露：提问中绝对不能出现“视情况而定”、“跨实体”、“聚合”、“条件链”、“分支”等评测术语，必须用职场自然口语。
2. 禁止暴露底层：提问中严禁出现工具名（如 find_employee_ref_by_name）、数据库表名、JSON字段名或内部 ID（如 EMP001）。
3. 禁止把 question 写成步骤提示：如果 question 读起来像是在暗示工具调用顺序、参数来源或计算方式，则该问题不合格。
4. 禁止替 Agent 做算术：最终生成的工具链（answer）中，如果涉及 calculate 工具，其参数中的数字必须来自前置查询工具结果的自然传递，绝不能凭空捏造。
5. 职场“班味”约束：请适度、克制地使用互联网公司黑话（如：拉通、对齐、碰一下、同步、兜底、卡点了、复盘、抓手、赋能），最多 1-2 个词，且必须符合语境。

=== 输出前自检（只在内部思考，不要输出这些检查过程）===
在输出前，先逐条自检；只要有任一项不满足，就重新生成：
1. 这段 question 是否像真实员工会发给 AI/助手的一条消息或指令？
2. 如果遮住 answer，这个 question 是否仍然成立，而不是明显在提示解法？
3. 任务里的每一步是否都由真实业务需要驱动，而不是为了凑复杂度？
4. 复杂 case 是否允许自然展开，而不是被你硬压成短句？
5. 若涉及统计、筛选、汇总、补救或写操作，它们是否都拥有清晰的业务动机和交付要求？

=== 输出格式要求 ===
请严格只输出如下 JSON 格式：
{{
    "business_scenario": "（内部思考）先构思业务背景。caller 遇到了什么具体的业务痛点？为什么要查这些数据？背后的真实意图是什么？",
    "question": "（对外展示）基于背景生成的自然语言消息或工作指令。语气要符合 caller 的身份，像是在工作软件里发给 AI/助手；简单场景可以短，复杂场景可以完整展开，但不能写成解题步骤提示。",
    "tool_chain": "（参考答案）工具调用链，用 [tool(args), tool(args)] 的 list 表示。参数必须真实存在于数据切片中！",
    "expected_answer": "（参考结论）最终精确的答案，一个具体的值、名字或一句明确的执行结果短句。"
}}
JSON 字符串内如需引用文字，请使用中文引号「」或“”，不要使用 ASCII 双引号 "。
请直接输出 JSON，不要附加任何其他内容。"""


_DEFAULT_FEW_SHOT_PATH = Path("data/few_shots/task_gen_few_shots.json")
_BUSINESS_RULES_DIR = Path("data/domains")


# "reasoning": "（内部思考）根据背景，规划出一条严密的工具调用链路。说明每一步调用的原因。",
# ──────────────────────────────────────────────
# Few-shot：按 domain / level 组织，优先当前域，避免跨域误导
# ──────────────────────────────────────────────

def _make_few_shot(
    *,
    tool_names: List[str],
    business_scenario: str,
    # reasoning: str,
    question: str,
    answer: str,
    final_answer: str,
) -> Dict[str, Any]:
    """构造 few-shot 样例，统一字段结构。"""
    return {
        "tool_names": tool_names,
        "content": json.dumps(
            {
                "business_scenario": business_scenario,
                # "reasoning": reasoning,
                "question": question,
                "tool_chain": answer,
                "expected_answer": final_answer,
            },
            ensure_ascii=False,
            indent=2,
        ),
    }


_FEW_SHOT_POOLS: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "hr": {
        "L1": [
            _make_few_shot(
                tool_names=["find_employee_ref_by_name", "get_employee_salary_structures"],
                business_scenario="同事临时要补一份人事口径，想确认某位员工当前生效中的基本工资，任务目标单一且不需要额外判断。",
                # reasoning="先根据姓名定位何桂芳的员工引用，再读取她当前生效的薪资结构记录并取基础工资；两步线性，无分支。",
                question="帮我看一下何桂芳现在生效中的基本工资是多少，我这边要补一份人事说明。",
                answer="[find_employee_ref_by_name(display_name='何桂芳'), get_employee_salary_structures(employee_ref='EMP003')]",
                final_answer="31901.0",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "find_employee_ref_by_name",
                    "get_employee_details",
                    "get_employee_leave_balances",
                    "calculate",
                ],
                business_scenario="提问者在安排孟萍这条线后续的评审和审批窗口，担心她直属主管后面若集中休假会拖慢节奏，所以想先确认这位主管今年剩余假期的大致总量。",
                # reasoning="先定位孟萍，再通过员工详情拿到她直属主管王龙的 employee_ref；随后查询王龙 2024 年的请假余额，并把三类剩余天数相加得到总数。后一步强依赖前一步返回的主管信息。",
                question="这周在排孟萍这条线后面的评审节奏，担心她直属领导下半年如果集中休假会把窗口卡住。帮我看下她老板今年大概还剩多少假可以休，给我一个总数就行，我好预留时间。",
                answer="[find_employee_ref_by_name(display_name='孟萍'), get_employee_details(employee_ref='EMP002'), get_employee_leave_balances(employee_ref='EMP001', year=2024), calculate(expression='9.0 + 14.3 + 9.0')]",
                final_answer="孟萍的直属主管王龙在2024年的假期余额合计还有32.3天。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "find_employee_ref_by_name",
                    "get_employee_tax_special_deductions",
                ],
                business_scenario="财务正在补做一轮专项附加扣除复核，只需确认几位指定员工里谁当前仍有生效中的大病医疗扣除，以便继续追后续材料。",
                # reasoning="依次定位四位员工，再分别查询他们的专项附加扣除记录；筛选 deduction_type 为大病医疗且状态为 active 的记录，最后把符合条件的人名聚合输出。属于多人盘点后的筛选汇总。",
                question="财务这边在补做专项附加扣除复核。麻烦看一下王龙、孟萍、何桂芳和唐玉华这几个人里，谁当前还有生效中的大病医疗扣除；有的话直接把名字给我，如果都没有就回我“无生效记录”。",
                answer="[find_employee_ref_by_name(display_name='王龙'), get_employee_tax_special_deductions(employee_ref='EMP001'), find_employee_ref_by_name(display_name='孟萍'), get_employee_tax_special_deductions(employee_ref='EMP002'), find_employee_ref_by_name(display_name='何桂芳'), get_employee_tax_special_deductions(employee_ref='EMP003'), find_employee_ref_by_name(display_name='唐玉华'), get_employee_tax_special_deductions(employee_ref='EMP006')]",
                final_answer="王龙、唐玉华",
            ),
        ],
    },
    "admin": {
        "L1": [
            _make_few_shot(
                tool_names=["list_parking_spaces"],
                business_scenario="员工只想确认某个园区当前有没有空闲停车位，属于单次列表查询，不需要跨实体推断。",
                # reasoning="上海创新园区对应 CAMP001，直接按园区和可用状态筛停车位即可；属于一步直达的浅链路任务。",
                question="帮我看下上海创新园区现在还有没有空着的停车位，有的话把能用的列给我。",
                answer="[list_parking_spaces(campus_ref='CAMP001', status='available')]",
                final_answer="上海创新园区目前有2个空闲停车位：PS002（B区，小型车位，支持充电桩）和PS009（地下停车区，标准车位）。",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "find_employee_ref_by_name",
                    "list_workstations",
                    "assign_workstation",
                ],
                business_scenario="新同事要在指定楼层区域落位，提问者已经给出了区域约束，系统需要先确认员工，再确认该区域确实有可用工位后执行分配。",
                # reasoning="先通过姓名定位姚凯，再查询指定楼栋、楼层、区域里的可用热桌工位；确认存在 WS001 后执行分配。写操作依赖前序查询结果，符合条件链。",
                question="姚凯这两天会去 1 楼西区设备区办公，麻烦帮他看看那边现在还有没有能直接用的热桌工位；如果有，就顺手安排一个给他，不用再回我确认。",
                answer="[find_employee_ref_by_name(display_name='姚凯'), list_workstations(building_ref='BLDG001', floor_ref='FLR001', zone_ref='ZONE004', workstation_type='hot_desk', status='available'), assign_workstation(workstation_ref='WS001', employee_ref='EMP008')]",
                final_answer="已将工位WS001分配给姚凯（EMP008）。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "find_department_ref_by_name",
                    "find_employee_ref_by_name",
                    "get_employee_details",
                    "list_campuses",
                    "list_buildings",
                    "list_floors",
                    "list_workstations",
                    "assign_workstation",
                ],
                business_scenario="行政正在给同部门两位同事统一调整办公位，希望一次性把两人的站立工位都落到同一栋楼的同一楼层，减少来回沟通成本。",
                # reasoning="先定位后端开发组和两位员工，再通过上海园区、楼宇、楼层逐步定位到目标区域；查询该楼层所有可用工位后，筛出 standing_desk 类型的 WS006 和 WS007，分别分配给唐玉华和姚凯，最后汇总分配结果。",
                question="后端开发组这边准备统一调一下办公位。麻烦帮唐玉华和姚凯都安排到上海那栋楼 1 楼还能用的站立工位里，尽量一次性处理完；安排好之后把分配结果和工位编号一起发我。",
                answer="[find_department_ref_by_name(department_name='后端开发组'), find_employee_ref_by_name(display_name='唐玉华'), find_employee_ref_by_name(display_name='姚凯'), get_employee_details(employee_ref='EMP006'), get_employee_details(employee_ref='EMP008'), list_campuses(city='上海'), list_buildings(campus_ref='CAMP001'), list_floors(building_ref='BLDG001'), list_workstations(floor_ref='FLR001', building_ref='BLDG001', campus_ref='CAMP001', status='available'), assign_workstation(workstation_ref='WS006', employee_ref='EMP006'), assign_workstation(workstation_ref='WS007', employee_ref='EMP008')]",
                final_answer="共分配了2个站立式工位：WS006 给唐玉华，WS007 给姚凯。",
            ),
        ],
    },
    "it": {
        "L1": [
            _make_few_shot(
                tool_names=["search_software_catalog", "list_software_licenses"],
                business_scenario="员工想确认某个常用软件在公司目录里有没有可分配许可证，本质是先搜软件目录再下钻许可证记录。",
                # reasoning="先搜索 Postman 在软件目录中的条目，拿到 software_catalog_ref 后再查询 active 状态的许可证记录；两步线性，结论是是否有可分配席位。",
                question="帮我查一下公司里 Postman 现在还有没有能分出去的许可证，我这边想给同事补一个席位。",
                answer="[search_software_catalog(keyword='Postman'), list_software_licenses(software_catalog_ref='SWC008', status='active')]",
                final_answer="Postman 在软件目录里有条目（SWC008），但没有查到 active 状态的独立许可证记录。",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "find_team_ref_by_name",
                    "get_team_details",
                    "find_code_repository_ref_by_name",
                    "add_code_repository_member",
                ],
                business_scenario="项目组想把负责人补进指定代码仓库，提问者只给了团队和仓库名，需要系统先找到团队 owner，再执行成员授权。",
                # reasoning="先定位 AI 算法项目组并读取负责人信息，再定位 ticket-engine-6 仓库；最后把团队 owner EMP018 以 developer 权限加进仓库。授权对象完全依赖前序团队详情。",
                question="AI 算法项目组那个 `ticket-engine-6` 仓库需要补权限，直接把这个组现在的负责人加进去，权限给 developer，授权人记我就行。",
                answer="[find_team_ref_by_name(team_name='AI算法项目组'), get_team_details(team_ref='TEAM004'), find_code_repository_ref_by_name(repository_name='ticket-engine-6'), add_code_repository_member(code_repository_ref='REPO006', employee_ref='EMP018', access_level='developer', granted_by_ref='EMP021')]",
                final_answer="已将AI算法项目组负责人EMP018以developer权限加入ticket-engine-6仓库，授权人为EMP021。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "find_team_ref_by_name",
                    "list_team_members",
                    "get_employee_details",
                    "list_it_system_accounts_for_employee",
                    "find_department_ref_by_name",
                    "list_email_distribution_lists",
                    "create_it_service_ticket",
                ],
                business_scenario="提问者在收一轮安全整改尾项，既要确认某个团队里是否还有活跃账号没开 MFA，也要顺手处理一个部门邮件组可能失效的问题，避免后面继续遗漏。",
                # reasoning="先定位篮球兴趣小组并列出成员，再逐个拉取其 active IT 账号，筛出未启用 MFA 的账号；随后查询后端开发组邮件组状态，若不是 active，则创建一张恢复工单。属于先筛后动并带额外条件动作的 L3 任务。",
                question="这边在收一轮安全整改尾项，麻烦把篮球兴趣小组里还在用的系统账号看一下，哪些人有活跃账号但没开 MFA，整理成清单给我。另外后端开发组邮件组也顺手确认下状态，如果现在不是正常可用的，就直接帮我提个恢复工单。",
                answer="[find_team_ref_by_name(team_name='篮球兴趣小组'), list_team_members(team_ref='TEAM011'), get_employee_details(employee_ref='EMP022'), list_it_system_accounts_for_employee(employee_ref='EMP022', account_status='active'), get_employee_details(employee_ref='EMP035'), list_it_system_accounts_for_employee(employee_ref='EMP035', account_status='active'), get_employee_details(employee_ref='EMP048'), list_it_system_accounts_for_employee(employee_ref='EMP048', account_status='active'), find_department_ref_by_name(department_name='后端开发组'), list_email_distribution_lists(department_ref='DEPT009'), create_it_service_ticket(requester_employee_ref='EMP022', ticket_category='service_request', ticket_subcategory='email_issue', title='后端开发组邮件组状态异常需要恢复', description='后端开发组邮件组（eng-be@groups.zhiliankj.com）当前状态为dissolved，需要恢复为active状态以保证组内正常通知和协作沟通。', urgency='medium', impact='team', priority='P3')]",
                final_answer="后端开发组邮件组当前状态异常，已创建恢复工单；篮球兴趣小组中未开MFA的活跃账号需按查询结果汇总输出。",
            ),
        ],
    },
    "work": {
        "L1": [
            _make_few_shot(
                tool_names=["list_todo_items_for_employee"],
                business_scenario="员工只想看自己名下待办，没有任何额外筛选或跨实体依赖，caller 身份本身就是查询条件。",
                # reasoning="直接使用 caller 的 employee_ref 查询待办列表即可，无需前置定位或分支判断。",
                question="帮我把我名下现在还没清掉的待办拉一下，我准备集中处理。",
                answer="[list_todo_items_for_employee(employee_ref='EMP005')]",
                final_answer="共2条待办：1. 处理缺陷单；2. 完成设计评审。",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "find_team_ref_by_name",
                    "list_team_members",
                    "get_employee_details",
                    "list_todo_items_for_employee",
                    "create_todo_item",
                ],
                business_scenario="提问者准备把一个新的跟进事项直接压给项目组负责人，但在落任务前希望确认当前负责人是谁，以及对方是否已经有在推进中的待办，避免安排错人。",
                # reasoning="先定位核心平台项目组，再通过成员和员工详情确认组长是 EMP011；查询他当前 in_progress 的待办后，为其创建一条新的高优先级待办。创建动作依赖前面识别出来的负责人。",
                question="核心平台项目组这边要补一个跟进项，我想直接压给现在在带这个组的人。你帮我看看负责人是谁；如果他手上已经有正在推进的待办，就再给他补一条高优先级待办，标题叫“平台架构评审跟进”，截止到 2025-08-01。",
                answer="[find_team_ref_by_name(team_name='核心平台项目组'), list_team_members(team_ref='TEAM001'), get_employee_details(employee_ref='EMP011'), list_todo_items_for_employee(employee_ref='EMP011', todo_status='in_progress'), create_todo_item(owner_employee_ref='EMP011', title='平台架构评审跟进', description='请跟进核心平台架构评审会议的后续行动项', priority='high', due_date='2025-08-01')]",
                final_answer="已为核心平台项目组组长EMP011创建高优先级待办“平台架构评审跟进”，截止日期为2025-08-01。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "find_team_ref_by_name",
                    "list_projects",
                    "list_project_risks",
                    "get_project_details",
                ],
                business_scenario="团队负责人准备开一次项目风险同步会，想先把当前真正卡住推进的项目和对应风险整理出来，避免会上再临时翻记录。",
                # reasoning="先定位数据平台项目组，再分别拉取 draft 和 on_hold 状态的项目；对命中的项目继续查询 open 和 accepted 状态的风险，并补充项目风险等级，最终汇总项目名称与未关闭风险。",
                question="数据平台项目组这边最近有几个项目一直没推进，我要拉一个风险同步。麻烦把当前还处在草稿或搁置状态的项目找出来，再把这些项目还没处理完的风险标题也带上，方便我直接拿去开会。",
                answer="[find_team_ref_by_name(team_name='数据平台项目组'), list_projects(team_ref='TEAM003', project_status='draft'), list_projects(team_ref='TEAM003', project_status='on_hold'), list_project_risks(project_ref='PROJ001', risk_status='open'), list_project_risks(project_ref='PROJ001', risk_status='accepted'), get_project_details(project_ref='PROJ001')]",
                final_answer="数据平台项目组当前命中的项目是“会议效率提升专项专项”（PROJ001），状态为草稿，风险等级为high，未关闭风险包括“需求频繁变更”。",
            ),
        ],
    },
    "finance": {
        "L1": [
            _make_few_shot(
                tool_names=["list_budgets", "get_budget_utilization"],
                business_scenario="业务同学只知道预算编号，想看这笔预算的使用情况和剩余额度，需要先从预算列表定位再查看使用概览。",
                # reasoning="先按财年和状态列出预算，定位到 BG-2025-0001 对应的 BUDG001，再查询这笔预算的使用概况；两步线性，结论可直接回答。",
                question="帮我看下预算编号 BG-2025-0001 现在用了多少、还剩多少，我要回领导一个口径。",
                answer="[list_budgets(fiscal_year=2025, budget_status='approved'), get_budget_utilization(budget_ref='BUDG001')]",
                final_answer="预算BG-2025-0001当前总额为2646943.94元，已支出520476.50元，冻结7982.85元，剩余可用额度约2118484.59元。",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "get_employee_details",
                    "list_budgets",
                    "get_budget_utilization",
                ],
                business_scenario="提问者正在核一笔与某同事相关的费用，希望顺着这位同事所在部门确认当前预算空间，判断后续还能不能继续走这条预算线。",
                # reasoning="先读取姚凯的员工详情拿到所属部门设计部，再按部门维度列预算，最后查询目标预算的使用情况。预算查询对象依赖员工所属部门信息。",
                question="姚凯上个月有笔报销挂在设计部这条线，我现在要确认后面的预算空间。帮我看下他归哪个部门，以及那个部门当前在用预算的使用情况，给我一个能直接回人的口径。",
                answer="[get_employee_details(employee_ref='EMP008'), list_budgets(scope_type='department', scope_ref='DEPT004'), get_budget_utilization(budget_ref='BUDG010')]",
                final_answer="姚凯所在部门是设计部，对应预算BUDG010当前总额517215.58元，已使用176243.75元，冻结8312.06元，剩余约332659.77元。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "find_department_ref_by_name",
                    "list_employee_loans",
                    "get_employee_details",
                    "list_payment_requests",
                ],
                business_scenario="财务在清一个部门当前的挂账与待支付情况，希望同时看清已批准借款和未真正提交出去的付款申请，方便判断是否需要继续追催。",
                # reasoning="先定位市场营销部，再筛出该部门已批准的员工借款，并为每笔借款补充借款人姓名；随后查询同一部门 draft 状态的付款申请，最后按“有借款明细 + 是否存在草稿付款申请”汇总输出。",
                question="财务这边在清市场营销部的挂账情况。麻烦把这个部门现在已经批准的员工借款整理一下，每笔带上借款人和金额；另外再看一下他们名下还有没有停在草稿里的付款申请，如果没有就直接写“暂无草稿付款申请”。",
                answer="[find_department_ref_by_name(department_name='市场营销部'), list_employee_loans(department_ref='DEPT007', loan_status='approved'), get_employee_details(employee_ref='EMP048'), get_employee_details(employee_ref='EMP011'), list_payment_requests(department_ref='DEPT007', request_status='draft')]",
                final_answer="市场营销部已批准借款共2笔：姚凯46718.04元，EMP011对应借款34031.46元；暂无草稿付款申请。",
            ),
        ],
    },
    "law": {
        "L1": [
            _make_few_shot(
                tool_names=[
                    "get_approval_flow_details",
                    "list_approval_steps",
                    "get_employee_details",
                ],
                business_scenario="发起人想追一条审批流第一步卡在谁手里，需要先确认审批流存在，再查看步骤和审批人信息。",
                # reasoning="先查询审批流详情确认 LAF007 有效，再列出其审批步骤，锁定第一步审批人 EMP008，最后读取该员工详情拿到姓名。",
                question="我之前提过一条合同审批，编号是 LAF007。你帮我看下第一步现在是谁在审，我好去催一下。",
                answer="[get_approval_flow_details(approval_flow_ref='LAF007'), list_approval_steps(approval_flow_ref='LAF007'), get_employee_details(employee_ref='EMP008')]",
                final_answer="LAF007 审批流的第一步审批人是姚凯（EMP008）。",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "find_employee_ref_by_name",
                    "list_seal_usage_requests",
                    "get_seal_details",
                    "find_department_ref_by_name",
                    "get_department_details",
                ],
                business_scenario="提问者正在确认一枚合同章当前归属谁在管理，只记得某位同事曾经用过这枚章，因此想顺着历史用印记录把所属部门和部门信息补齐。",
                # reasoning="先定位姚凯，再查他已使用过的指定用印申请；根据印章详情读出归属部门，最后查询该部门详情。后续查询对象由前面印章详情决定，属于典型跨实体条件链。",
                question="姚凯之前经手过 SEAL-007 那枚合同章，我现在要确认这枚章归谁在管。帮我把它当前所属部门和那个部门的基本信息一起带回来。",
                answer="[find_employee_ref_by_name(display_name='姚凯'), list_seal_usage_requests(applicant_employee_ref='EMP008', seal_ref='LSEAL007', request_status='used'), get_seal_details(seal_ref='LSEAL007'), find_department_ref_by_name(department_name='前端开发组'), get_department_details(department_ref='DEPT010')]",
                final_answer="SEAL-007 当前归前端开发组（DEPT010）管理，部门编码为 ENG-FE，状态为 active。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "find_team_ref_by_name",
                    "list_team_members",
                    "list_ip_assets_by_inventor",
                    "get_ip_asset_details",
                    "list_ip_rewards",
                ],
                business_scenario="法务在收一批知识产权奖励发放事项，想先把一个团队里仍然有效的 IP 资产和对应未发放奖励梳理干净，避免后续漏发。",
                # reasoning="先定位核心平台项目组并列出成员，再逐个查询成员名下 IP 资产；筛出状态为 active 的资产后，继续查询这些资产下 reward_status 为 pending 的奖励记录，最后汇总待支付条数和涉及员工。",
                question="法务这边在收一批知识产权奖励，核心平台项目组这条线想先梳理干净。麻烦把组里成员名下目前还有效的 IP 资产找出来，再把这些资产下面还没发出去的奖励一起汇总下，告诉我一共有几条、涉及哪些人。",
                answer="[find_team_ref_by_name(team_name='核心平台项目组'), list_team_members(team_ref='TEAM001'), list_ip_assets_by_inventor(employee_ref='EMP011'), list_ip_assets_by_inventor(employee_ref='EMP002'), list_ip_assets_by_inventor(employee_ref='EMP029'), list_ip_assets_by_inventor(employee_ref='EMP026'), list_ip_assets_by_inventor(employee_ref='EMP017'), get_ip_asset_details(ip_asset_ref='LIPA002'), get_ip_asset_details(ip_asset_ref='LIPA004'), get_ip_asset_details(ip_asset_ref='LIPA006'), get_ip_asset_details(ip_asset_ref='LIPA007'), get_ip_asset_details(ip_asset_ref='LIPA008'), list_ip_rewards(ip_asset_ref='LIPA002', reward_status='pending'), list_ip_rewards(ip_asset_ref='LIPA004', reward_status='pending'), list_ip_rewards(ip_asset_ref='LIPA006', reward_status='pending'), list_ip_rewards(ip_asset_ref='LIPA007', reward_status='pending'), list_ip_rewards(ip_asset_ref='LIPA008', reward_status='pending')]",
                final_answer="当前共命中1条待支付IP奖励：LIPRWD006，涉及员工EMP018，对应资产LIPA004，金额47236.13元。",
            ),
        ],
    },
    "purchase": {
        "L1": [
            _make_few_shot(
                tool_names=[
                    "find_supplier_ref_by_name",
                    "list_supplier_contacts",
                ],
                business_scenario="采购同学只想确认某家供应商当前主联系人是谁以及联系方式，先定位供应商，再查联系人列表即可。",
                # reasoning="先通过供应商全称定位 SUP001，再查询其 active 联系人列表，并从中取主联系人信息；两步线性、单意图明确。",
                question="鑫博腾飞信息有限公司网络有限公司那边现在主要联系人是谁？电话和邮箱也一起给我，我要拉个会。",
                answer="[find_supplier_ref_by_name(supplier_name='鑫博腾飞信息有限公司网络有限公司'), list_supplier_contacts(supplier_ref='SUP001', status='active')]",
                final_answer="主要联系人是商帅，电话16786210781，邮箱proczt62px@126.com。",
            ),
        ],
        "L2": [
            _make_few_shot(
                tool_names=[
                    "find_supplier_ref_by_name",
                    "list_supplier_evaluations",
                    "get_supplier_evaluation_details",
                    "list_supplier_categories",
                ],
                business_scenario="采购负责人正在复核一家供应商近期合作情况，想同时确认最近一次已通过评估的结果和当前挂载的采购品类，方便一次性判断是否继续沿用。",
                # reasoning="先定位四通传媒有限公司设备有限公司，再拉取其 approved 的评估记录并读取 2024 年 Q4 那条详情；最后查询该供应商关联的采购品类。后一步都依赖前面的供应商定位结果。",
                question="帮我把四通传媒有限公司设备有限公司最近那份已经通过的季度评估捞出来，综合分和评级给我一下；另外把它现在挂着的采购品类也一并带上，我这边要一起复核。",
                answer="[find_supplier_ref_by_name(supplier_name='四通传媒有限公司设备有限公司'), list_supplier_evaluations(supplier_ref='SUP003', status='approved'), get_supplier_evaluation_details(supplier_evaluation_ref='SPE004'), list_supplier_categories(supplier_ref='SUP003')]",
                final_answer="这家供应商 2024 年 Q4 评估综合得分 90.16，评级 A；当前关联品类为 PCAT023 和 PCAT026。",
            ),
        ],
        "L3": [
            _make_few_shot(
                tool_names=[
                    "list_suppliers",
                    "get_supplier_details",
                    "list_supplier_evaluations",
                ],
                business_scenario="采购团队正在处理一批合作风险偏高的供应商，希望先把仍处于高风险但合作已获批准的对象筛出来，再补齐最近已通过的评估结论，方便决定后续跟进动作。",
                # reasoning="先筛出合作状态为 approved 且风险等级为 high 的供应商，再逐个补全供应商详情，并分别查询 approved 状态的评估记录；最后汇总“供应商名称 + 最新已审批评估结果或无”。",
                question="采购这边现在在看合作风险，麻烦把已经批准合作但风险等级还高的供应商筛出来。每家如果已经有通过的评估，就把最新的评分和评级一起带上；如果没有，也直接标明。",
                answer="[list_suppliers(cooperation_status='approved', risk_level='high'), get_supplier_details(supplier_ref='SUP007'), get_supplier_details(supplier_ref='SUP010'), list_supplier_evaluations(supplier_ref='SUP007', status='approved'), list_supplier_evaluations(supplier_ref='SUP010', status='approved')]",
                final_answer="当前命中2家高风险已批准合作供应商：SUP007 和 SUP010；两家都没有已审批通过的评估记录。",
            ),
        ],
    },
}


def _load_few_shot_pools_from_file(path: Path) -> Optional[Dict[str, Dict[str, List[Dict[str, Any]]]]]:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return None
    if not isinstance(raw, dict):
        return None
    normalized: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    for domain, level_map in raw.items():
        if not isinstance(level_map, dict):
            continue
        domain_key = str(domain).strip().lower()
        normalized[domain_key] = {}
        for level, examples in level_map.items():
            if level not in ("L1", "L2", "L3") or not isinstance(examples, list):
                continue
            valid_examples = []
            for example in examples:
                if not isinstance(example, dict):
                    continue
                tool_names = example.get("tool_names", [])
                content = example.get("content", "")
                if isinstance(tool_names, list) and isinstance(content, str):
                    valid_examples.append({"tool_names": tool_names, "content": content})
            if valid_examples:
                normalized[domain_key][level] = valid_examples
    return normalized or None


_FILE_FEW_SHOT_POOLS = _load_few_shot_pools_from_file(_DEFAULT_FEW_SHOT_PATH)
if _FILE_FEW_SHOT_POOLS:
    _FEW_SHOT_POOLS = _FILE_FEW_SHOT_POOLS


def _load_business_rules(domain: str) -> str:
    domain = str(domain or "").strip().lower()
    if not domain:
        return ""
    rule_path = _BUSINESS_RULES_DIR / domain / "business_rules.md"
    if not rule_path.exists():
        return ""
    try:
        return rule_path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def _normalize_domain(domain: Optional[str]) -> str:
    """归一化 domain，避免大小写和空值导致选样失败。"""
    return (domain or "").strip().lower()


def _infer_domain_from_toolkit(toolkit: ToolKitBase) -> str:
    """从 toolkit 类型推断当前 domain。"""
    cls_name = toolkit.__class__.__name__.lower()
    module_name = toolkit.__class__.__module__.lower()
    for domain in ("hr", "admin", "it", "work", "finance", "law", "purchase", "base"):
        if domain in cls_name or f".{domain}." in module_name:
            return domain
    return ""


def _tool_overlap_score(example_tools: List[str], available_tools: Set[str]) -> int:
    """计算样例工具与当前工具集的重合度。"""
    return sum(1 for name in example_tools if name in available_tools)


def _pick_few_shot(level: str, domain: str, tool_names: Optional[List[str]] = None) -> str:
    """按 domain / level 选择样例，并在必要时做安全回退。"""
    domain = _normalize_domain(domain)
    available_tools = set(tool_names or [])
    domain_pool = _FEW_SHOT_POOLS.get(domain, {}).get(level, [])

    if not domain_pool:
        domain_pool = []

    if not available_tools:
        return random.choice(domain_pool)["content"] if domain_pool else ""

    exact = [
        example for example in domain_pool
        if set(example["tool_names"]).issubset(available_tools)
    ]
    if exact:
        return random.choice(exact)["content"]

    scored = [
        (example, _tool_overlap_score(example["tool_names"], available_tools))
        for example in domain_pool
    ]
    scored = [item for item in scored if item[1] > 0]
    if scored:
        best_score = max(score for _, score in scored)
        best_examples = [example for example, score in scored if score == best_score]
        return random.choice(best_examples)["content"]

    cross_domain_exact: List[Dict[str, Any]] = []
    for pool_domain, pool_by_level in _FEW_SHOT_POOLS.items():
        if pool_domain == domain:
            continue
        for example in pool_by_level.get(level, []):
            if set(example["tool_names"]).issubset(available_tools):
                cross_domain_exact.append(example)
    if cross_domain_exact:
        return random.choice(cross_domain_exact)["content"]

    return ""


def _format_few_shot_block(level: str, domain: str, tool_names: Optional[List[str]] = None) -> str:
    """格式化 few-shot 区块，明确样例只可借鉴风格与结构。"""
    sample = _pick_few_shot(level, domain, tool_names)
    if not sample:
        return "（当前没有匹配到足够贴近本轮工具集的样例，请完全依据工具签名和数据切片生成，不要臆造工具或参数。）"
    return (
        "下面是一条高质量参考样例。你只能借鉴它像真实员工发给 AI/助手的消息口吻、任务感、上下文组织方式和隐式依赖设计，"
        "绝对不能照抄其中的实体名、内部编号、工具链、数字或最终答案；也不能模仿任何把求解步骤直接写进 question 里的表达。"
        "本轮任务必须严格以当前可用工具和数据切片为准。\n"
        f"{sample}"
    )


def format_tool_signatures(
    toolkit: ToolKitBase,
    tool_names: Optional[List[str]] = None,
    base_tool_names: Optional[List[str]] = None,
) -> str:
    """格式化工具签名，供 prompt 使用。base 工具单独分节标注。"""
    sigs = get_tool_signatures(toolkit)
    base_set = set(base_tool_names or [])

    def _fmt(name: str, sig) -> str:
        params_str = ""
        if sig.params and sig.params.get("properties"):
            params_str = ", ".join(sig.params["properties"].keys())
        doc = sig.doc[:300] if sig.doc else ""
        return f"{name}({params_str})\n{doc}\n"

    base_lines, biz_lines = [], []
    for name, sig in sigs.items():
        if tool_names and name not in tool_names:
            continue
        (base_lines if name in base_set else biz_lines).append(_fmt(name, sig))

    parts = []
    if base_lines:
        parts.append("【基础定位工具】（仅用于查找人员/组织 ID，不能作为任务核心）\n" + "\n".join(base_lines))
    if biz_lines:
        parts.append("【业务操作工具】（任务核心必须涉及这些工具中的至少一个）\n" + "\n".join(biz_lines))
    return "\n".join(parts)


def build_data_slice(
    toolkit: ToolKitBase,
    table_names: Optional[List[str]] = None,
    max_per_table: int = 100,
) -> str:
    """从 DB 中切出相关表的样本数据。

    Args:
        toolkit: 已加载 DB 的 ToolKit
        table_names: 要包含的表名列表（None 则全量）
        max_per_table: 每表最多行数
    """
    db_dict = toolkit.db.model_dump()
    # 基础表始终包含
    base_tables = {"employee", "user_profile", "department", "position", "team", "role"}
    include = base_tables | (set(table_names) if table_names else set(db_dict.keys()))

    sample = {}
    for table in include:
        data = db_dict.get(table)
        if data is None:
            continue
        if isinstance(data, dict):
            sample[table] = dict(list(data.items())[:max_per_table])
        elif isinstance(data, list):
            sample[table] = data[:max_per_table]
    return json.dumps(sample, ensure_ascii=False, default=str, indent=2)


def format_caller_info(caller: Dict[str, Any]) -> str:
    """格式化 caller 信息。"""
    lines = []
    for k, v in caller.items():
        if v is not None:
            lines.append(f"  {k}: {v}")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# 主类
# ──────────────────────────────────────────────

class TaskGenerator:
    """p.txt 风格的任务生成器：一次 LLM 调用生成完整的 GAIA 风格任务。"""

    def __init__(
        self,
        model: str,
        llm_config: Dict[str, Any],
        toolkit: ToolKitBase,
        domain: Optional[str] = None,
    ):
        self.model = model
        self.llm_config = llm_config
        self.toolkit = toolkit
        self.domain = _normalize_domain(domain) or _infer_domain_from_toolkit(toolkit)
        self.business_rules = _load_business_rules(self.domain)

    def generate_one(
        self,
        level: str = "L2",
        caller: Optional[Dict[str, Any]] = None,
        tool_names: Optional[List[str]] = None,
        table_names: Optional[List[str]] = None,
        base_tool_names: Optional[List[str]] = None,
        max_per_table: int = 10,
    ) -> Optional[Dict[str, Any]]:
        """生成一个 GAIA 风格任务。

        Args:
            level: 难度级别 L1/L2/L3
            caller: 提问者身份信息 dict
            tool_names: 限定使用的工具名列表（None 则全量）
            table_names: 限定使用的数据表列表（None 则全量）
            max_per_table: 数据切片每表最大行数
        Returns:
            任务 dict，失败返回 None
        """
        if level not in _LEVEL_INSTRUCTIONS:
            raise ValueError(f"level 必须为 L1/L2/L3，收到 {level}")

        if caller is None:
            caller = self._pick_default_caller()

        prompt = _PROMPT_TEMPLATE.format(
            level_instruction=_LEVEL_INSTRUCTIONS[level],
            caller_info=format_caller_info(caller),
            tool_signatures=format_tool_signatures(self.toolkit, tool_names, base_tool_names),
            data_slice=build_data_slice(self.toolkit, table_names, max_per_table),
            business_rules=self.business_rules or "（暂无结构化业务规则，必须严格遵循数据库中的 policy/配置字段。）",
            few_shot_block=_format_few_shot_block(level, self.domain, tool_names),
            cross_domain_requirement=(
                "当前为跨域模式：question 与 answer 必须涉及至少 2 个不同业务域的工具，且链路需有真实上下游依赖。"
                if self.domain == "cross"
                else "当前为单域模式：问题应聚焦本域核心业务，不要无意义跨域拼接。"
            ),
        )

        messages = [UserMessage(content=prompt)]
        resp = None
        try:
            resp = generate(model=self.model, messages=messages, llm_config=self.llm_config)
            finish_reason = None
            if isinstance(resp.raw_data, dict):
                finish_reason = resp.raw_data.get("_finish_reason")
            logger.debug(f"[TaskGenerator] Response (finish_reason={finish_reason}): {resp.content}")
            result = extract_json_from_llm_response(resp.content)
            if not isinstance(result, dict):
                raise ValueError("生成结果不是 JSON 对象")
        except Exception as e:
            finish_reason = None
            raw_content = ""
            if resp is not None:
                raw_content = resp.content or ""
                if isinstance(resp.raw_data, dict):
                    finish_reason = resp.raw_data.get("_finish_reason")
            print(
                f"[TaskGenerator] 生成失败（finish_reason={finish_reason}）: {e}\n"
                f"[TaskGenerator] Raw response: {raw_content}"
            )
            return None
        # logger.debug(f"[TaskGenerator] Prompt: {prompt}")
        task_id = f"{level.lower()}_{uuid.uuid4().hex[:8]}"
        # prompt 规范输出 tool_chain/expected_answer，历史数据用 answer/final_answer；
        # 两种字段名都接受，并补齐四个字段（与 tasks_clean 发布 schema 对齐）
        answer = result.get("answer") or result.get("tool_chain", "")
        final_answer = result.get("final_answer") or result.get("expected_answer", "")
        return {
            "task_id": task_id,
            "level": level,
            "business_scenario": result.get("business_scenario", ""),
            "question": result.get("question", ""),
            "answer": answer,
            "tool_chain": answer,
            "final_answer": final_answer,
            "expected_answer": final_answer,
            "reasoning": result.get("reasoning", ""),
            "caller": caller,
            "metadata": {
                "tool_subset": tool_names,
                "table_subset": table_names,
            },
        }

    def generate_batch(
        self,
        n: int = 1,
        level: str = "L2",
        caller: Optional[Dict[str, Any]] = None,
        tool_names: Optional[List[str]] = None,
        table_names: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """批量生成同一难度级别的任务。"""
        tasks = []
        callers = self._list_callers() if caller is None else [caller]
        for i in range(n):
            c = callers[i % len(callers)] if len(callers) > 1 else callers[0]
            task = self.generate_one(level=level, caller=c, tool_names=tool_names, table_names=table_names)
            if task:
                tasks.append(task)
        return tasks

    def _pick_default_caller(self) -> Dict[str, Any]:
        """从 DB 中随机选一个 active 员工作为 caller。"""
        callers = self._list_callers()
        active = [c for c in callers if c.get("employment_status") == "active"]
        pool = active or callers
        return random.choice(pool) if pool else {"employee_ref": "EMP001", "display_name": "默认用户"}

    def _list_callers(self) -> List[Dict[str, Any]]:
        """从 DB 中提取 caller 候选列表，包含岗位、部门、团队、直属领导等上下文。"""
        try:
            db = self.toolkit.db.model_dump()
            employees = db.get("employee", {})
            profiles = db.get("user_profile", {})
            positions = db.get("position", {})
            departments = db.get("department", {})
            dept_members = db.get("department_member", {})
            teams = db.get("team", {})
            team_members = db.get("team_member", {})

            # 构建 employee_ref → 部门/团队的反查表
            emp_dept: Dict[str, str] = {}
            for dm in dept_members.values():
                if isinstance(dm, dict) and dm.get("is_primary"):
                    emp_dept[dm["employee_ref"]] = dm.get("department_ref", "")

            emp_team: Dict[str, str] = {}
            for tm in team_members.values():
                if isinstance(tm, dict):
                    emp_team.setdefault(tm["employee_ref"], tm.get("team_ref", ""))

            callers = []
            for emp_ref, emp in employees.items():
                if not isinstance(emp, dict):
                    continue
                profile = profiles.get(emp.get("user_profile_ref", ""), {})
                pos = positions.get(emp.get("position_ref", ""), {})
                dept_ref = emp_dept.get(emp_ref, "")
                dept = departments.get(dept_ref, {})
                team_ref = emp_team.get(emp_ref, "")
                team = teams.get(team_ref, {})
                manager_ref = emp.get("manager_ref", "")
                manager_profile = profiles.get(
                    employees.get(manager_ref, {}).get("user_profile_ref", ""), {}
                )
                callers.append({
                    "employee_ref": emp_ref,
                    "display_name": profile.get("display_name", emp_ref),
                    "position": pos.get("position_name", ""),
                    "department": dept.get("department_name", ""),
                    "team": team.get("team_name", ""),
                    "manager": manager_profile.get("display_name", ""),
                    "employment_status": emp.get("employment_status", ""),
                })
            return callers if callers else [{"employee_ref": "EMP001"}]
        except Exception:
            return [{"employee_ref": "EMP001"}]
