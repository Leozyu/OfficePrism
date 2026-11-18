"""task_gen: 精简版 GAIA 风格任务生成 Pipeline。

用法：
    from task_gen import TaskGenPipeline

    pipeline = TaskGenPipeline.from_config("configs/app.yaml", toolkit, domain="HR")

    # target_counts：每个分组在各级别生成的条数（非全库合计）
    tasks = pipeline.batch_generate(
        target_counts={"L1": 5, "L2": 5, "L3": 5},
        output_path="tasks.json",
        max_concurrent=5,
    )
"""
from .generator import TaskGenerator
from .verifier import verify_task

__all__ = ["TaskGenerator", "verify_task"]
