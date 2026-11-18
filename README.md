# OfficePrism — Task Synthesis

This branch contains the **prompt-driven synthesis pipeline** of OfficePrism: it turns business definitions into runnable **DB + tools + tasks + ground truth** for enterprise office domains, plus the same simulation-based evaluation framework as the `eval-only` branch.

> **Paper**: citation to be added (TODO).

## Branches

| Branch | Contents |
|---|---|
| `eval-only` (default) | Benchmark data + evaluation framework + external agent adapters |
| `task-synthesis` (this branch) | Full synthesis pipeline + evaluation framework |

## Synthesis pipeline

The pipeline builds a shared world model first, then layers business increments on top:

1. **Base** — organization, personnel, roles, and permissions shared by all domains (`synthesis/domain_gen/base_gen_data.py`, `synthesis/prompts/base/`).
2. **Domain / module** — per-domain DB increments, tool sets, and policies (`synthesis/domain_gen/*_gen_data.py`, `synthesis/prompts/<domain>/`).
3. **Tasks** — realistic, solvable, verifiable user requests generated from the world model (`synthesis/task_gen/pipeline.py`).
4. **Ground truth** — high-signal completion assertions (environment / tool-return / output assertions).

Key components:

| Path | Description |
|---|---|
| `synthesis/prompts/` | Prompt templates for each synthesis step |
| `synthesis/domain_gen/` | Domain data generators (Faker-based, fixed seeds) |
| `synthesis/task_gen/` | Task generation pipeline, verification, dedup |
| `synthesis/notebooks/` | Historical synthesis notebooks (reference only; some cells predate the current API) |
| `synthesis/exploration_memory/` | Exploration records used during synthesis |
| `data/few_shots/` | Few-shot examples for task generation |

## Installation

Python 3.10+ recommended.

```bash
git clone https://github.com/Leozyu/OfficePrism.git
cd OfficePrism
git checkout task-synthesis
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env   # fill in LLM_API_KEY / LLM_BASE_URL
```

`.env` is loaded automatically (`python-dotenv`). Synthesis LLM settings live in `configs/app.yaml` (`synthesis.llm`) and `configs/app_notebook.yaml` (notebooks). API keys are read from environment variables — no secrets live in the config files.

## Quickstart

```bash
# Generate tasks for selected domains (with global dedup), from the repo root
./synthesis/gen_tasks.sh --domains "hr it" --concurrent 5

# Or invoke the pipeline directly
python -m synthesis.task_gen.pipeline \
    --domain hr \
    --output data/tasks/tasks_hr.json \
    --max-concurrent 5
```

Generated tasks land in `data/tasks/`; cleaned per-domain pools are in `data/tasks_clean/`. To evaluate agents on them, use the same runner as the `eval-only` branch:

```bash
./eval.sh --dry-run
python -m bench.run_domain_eval --domain hr \
    --task-path data/tasks_clean/tasks_hr_70.json \
    --agent react_agent --max-steps 50 \
    --save-to data/results/hr/react.json
```

## License

Apache-2.0. See [LICENSE](LICENSE).