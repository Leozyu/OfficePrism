"""Task-level deduplication for generated task sets."""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .verifier import _parse_tool_chain


_NON_WORD_RE = re.compile(r"\s+")


def _normalize_text(text: str) -> str:
    return _NON_WORD_RE.sub(" ", (text or "").strip().lower())


def _task_score(task: Dict[str, Any]) -> float:
    judge = task.get("judge_result") or {}
    logic = judge.get("logic_score")
    natural = judge.get("naturalness_score")
    difficulty = judge.get("difficulty_score")
    vals = [v for v in (logic, natural, difficulty) if isinstance(v, (int, float))]
    if vals:
        return float(sum(vals)) / float(len(vals))
    return 0.0


def _task_level(task: Dict[str, Any]) -> str:
    return str(task.get("level") or "UNKNOWN").upper()


def _caller_role(task: Dict[str, Any]) -> str:
    caller = task.get("caller") or {}
    return str(caller.get("role_type") or caller.get("position") or "unknown").lower()


def _tool_names(task: Dict[str, Any]) -> List[str]:
    answer = task.get("answer") or ""
    try:
        calls = _parse_tool_chain(answer)
        names = [str(c.get("name", "")) for c in calls if isinstance(c, dict)]
        return [n for n in names if n]
    except Exception:
        return []


def _structural_signature(task: Dict[str, Any]) -> Tuple[Tuple[str, ...], str, str]:
    return tuple(sorted(set(_tool_names(task)))), _caller_role(task), _task_level(task)


def _char_ngram_vector(text: str, n: int = 3) -> Dict[str, float]:
    text = _normalize_text(text)
    if not text:
        return {}
    if len(text) < n:
        return {text: 1.0}
    counts: Dict[str, float] = {}
    for i in range(len(text) - n + 1):
        key = text[i : i + n]
        counts[key] = counts.get(key, 0.0) + 1.0
    norm = math.sqrt(sum(v * v for v in counts.values()))
    if norm <= 0:
        return counts
    return {k: v / norm for k, v in counts.items()}


def _cosine_sparse(a: Dict[str, float], b: Dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    score = 0.0
    for key, value in a.items():
        score += value * b.get(key, 0.0)
    return score


class _SemanticEncoder:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name
        self._st_model = None
        if model_name:
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore

                self._st_model = SentenceTransformer(model_name)
            except Exception:
                self._st_model = None

    def encode(self, texts: Sequence[str]) -> List[Any]:
        normalized = [_normalize_text(x) for x in texts]
        if self._st_model is not None and normalized:
            vectors = self._st_model.encode(normalized, normalize_embeddings=True)
            return [v.tolist() if hasattr(v, "tolist") else v for v in vectors]
        return [_char_ngram_vector(text) for text in normalized]

    @staticmethod
    def similarity(vec_a: Any, vec_b: Any) -> float:
        if isinstance(vec_a, dict) and isinstance(vec_b, dict):
            return _cosine_sparse(vec_a, vec_b)
        try:
            a = vec_a
            b = vec_b
            dot = 0.0
            na = 0.0
            nb = 0.0
            for x, y in zip(a, b):
                dot += float(x) * float(y)
                na += float(x) * float(x)
                nb += float(y) * float(y)
            if na <= 0 or nb <= 0:
                return 0.0
            return dot / (math.sqrt(na) * math.sqrt(nb))
        except Exception:
            return 0.0


@dataclass
class DedupReport:
    input_count: int
    kept_count: int
    removed_structural: int
    removed_semantic: int

    @property
    def removed_total(self) -> int:
        return self.input_count - self.kept_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_count": self.input_count,
            "kept_count": self.kept_count,
            "removed_total": self.removed_total,
            "removed_structural": self.removed_structural,
            "removed_semantic": self.removed_semantic,
            "kept_rate": (self.kept_count / self.input_count) if self.input_count else 0.0,
        }


def deduplicate_tasks(
    tasks: List[Dict[str, Any]],
    *,
    semantic_threshold: float = 0.85,
    embedding_model: Optional[str] = None,
    existing_tasks: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[List[Dict[str, Any]], DedupReport]:
    if not tasks:
        return [], DedupReport(0, 0, 0, 0)

    encoder = _SemanticEncoder(embedding_model)
    items = list(tasks)
    seed_items = list(existing_tasks or [])
    all_items = seed_items + items
    indexed = list(enumerate(all_items))
    indexed.sort(key=lambda it: _task_score(it[1]), reverse=True)

    seen_struct: Dict[Tuple[Tuple[str, ...], str, str], int] = {}
    kept_indices: List[int] = []
    removed_structural = 0
    seed_count = len(seed_items)

    for idx, task in indexed:
        sig = _structural_signature(task)
        if sig in seen_struct:
            if idx >= seed_count:
                removed_structural += 1
            continue
        seen_struct[sig] = idx
        kept_indices.append(idx)

    kept_indices.sort()
    bucket_vectors: Dict[Tuple[str, str], List[Tuple[int, Any]]] = {}
    removed_semantic = 0
    final_kept: List[int] = []

    texts_by_idx = {idx: _normalize_text(all_items[idx].get("question") or "") for idx in kept_indices}
    vecs = encoder.encode([texts_by_idx[idx] for idx in kept_indices])
    vec_by_idx = {idx: vecs[pos] for pos, idx in enumerate(kept_indices)}

    for idx in sorted(kept_indices, key=lambda i: _task_score(all_items[i]), reverse=True):
        task = all_items[idx]
        key = (_task_level(task), _caller_role(task))
        question = texts_by_idx.get(idx, "")
        if not question:
            final_kept.append(idx)
            bucket_vectors.setdefault(key, []).append((idx, vec_by_idx[idx]))
            continue
        duplicated = False
        for kept_idx, kept_vec in bucket_vectors.get(key, []):
            sim = encoder.similarity(vec_by_idx[idx], kept_vec)
            if sim >= semantic_threshold:
                duplicated = True
                if idx >= seed_count:
                    removed_semantic += 1
                break
        if duplicated:
            continue
        final_kept.append(idx)
        bucket_vectors.setdefault(key, []).append((idx, vec_by_idx[idx]))

    final_kept.sort()
    kept_generated = [all_items[i] for i in final_kept if i >= seed_count]
    report = DedupReport(
        input_count=len(tasks),
        kept_count=len(kept_generated),
        removed_structural=removed_structural,
        removed_semantic=removed_semantic,
    )
    return kept_generated, report


def _load_tasks(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} is not a JSON array")
    return [x for x in data if isinstance(x, dict)]


def _save_tasks(path: Path, tasks: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(list(tasks), f, ensure_ascii=False, indent=2)


def deduplicate_file(
    input_path: Path,
    *,
    output_path: Optional[Path] = None,
    semantic_threshold: float = 0.85,
    embedding_model: Optional[str] = None,
    existing_path: Optional[Path] = None,
) -> DedupReport:
    tasks = _load_tasks(input_path)
    existing = _load_tasks(existing_path) if existing_path else None
    deduped, report = deduplicate_tasks(
        tasks,
        semantic_threshold=semantic_threshold,
        embedding_model=embedding_model,
        existing_tasks=existing,
    )
    target = output_path or input_path
    _save_tasks(target, deduped)
    return report


def deduplicate_directory(
    directory: Path,
    *,
    pattern: str = "tasks_*.json",
    semantic_threshold: float = 0.85,
    embedding_model: Optional[str] = None,
    in_place: bool = False,
    output_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    files = sorted(directory.glob(pattern))
    if not files:
        return {"files": {}, "overall": {"input_count": 0, "kept_count": 0}}

    global_pool: List[Dict[str, Any]] = []
    file_reports: Dict[str, Any] = {}
    total_input = 0
    total_kept = 0

    if in_place:
        out_root = directory
    else:
        out_root = output_dir or directory.parent / f"{directory.name}_dedup"
        out_root.mkdir(parents=True, exist_ok=True)

    for file_path in files:
        tasks = _load_tasks(file_path)
        deduped, report = deduplicate_tasks(
            tasks,
            semantic_threshold=semantic_threshold,
            embedding_model=embedding_model,
            existing_tasks=global_pool,
        )
        total_input += report.input_count
        total_kept += report.kept_count
        global_pool.extend(deduped)

        if in_place:
            target = file_path
        else:
            target = out_root / file_path.name
        _save_tasks(target, deduped)
        file_reports[file_path.name] = report.to_dict()

    return {
        "files": file_reports,
        "overall": {
            "input_count": total_input,
            "kept_count": total_kept,
            "removed_total": total_input - total_kept,
            "kept_rate": (total_kept / total_input) if total_input else 0.0,
        },
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deduplicate generated task JSON files")
    parser.add_argument("path", help="Task JSON file path or directory path")
    parser.add_argument("--pattern", default="tasks_*.json", help="File pattern when path is a directory")
    parser.add_argument("--semantic-threshold", type=float, default=0.85, help="Semantic similarity threshold")
    parser.add_argument("--embedding-model", default=None, help="Optional sentence-transformers model name")
    parser.add_argument("--existing", default=None, help="Optional existing task file for incremental dedup")
    parser.add_argument("--inplace", action="store_true", help="Overwrite source files")
    parser.add_argument("--output", default=None, help="Output file path (single file mode)")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (directory mode). Default: <input_dir>_dedup",
    )
    parser.add_argument("--report", default=None, help="Optional report output path")
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    target = Path(args.path)
    if target.is_dir():
        report = deduplicate_directory(
            target,
            pattern=args.pattern,
            semantic_threshold=args.semantic_threshold,
            embedding_model=args.embedding_model,
            in_place=args.inplace,
            output_dir=Path(args.output_dir) if args.output_dir else None,
        )
        if args.report:
            report_path = Path(args.report)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with report_path.open("w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    output_path = Path(args.output) if args.output else (target if args.inplace else target)
    report = deduplicate_file(
        target,
        output_path=output_path,
        semantic_threshold=args.semantic_threshold,
        embedding_model=args.embedding_model,
        existing_path=Path(args.existing) if args.existing else None,
    )
    report_dict = report.to_dict()
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
    print(json.dumps(report_dict, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
