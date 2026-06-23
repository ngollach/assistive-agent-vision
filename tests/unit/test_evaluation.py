import json

from evaluation.run_evaluation import evaluate_dataset


def test_evaluation_dataset_runs(tmp_path):
    dataset = [
        {
            "id": "test_case",
            "prompt": "Describe this desk.",
            "image_path": "desk.jpg",
            "expected_risk_level": "low",
            "expected_phrases": ["desk", "table"],
            "must_not_include": ["guaranteed safe"],
        }
    ]

    dataset_path = tmp_path / "dataset.json"
    dataset_path.write_text(json.dumps(dataset), encoding="utf-8")

    report = evaluate_dataset(str(dataset_path))

    assert report["total"] == 1
    assert report["passed"] == 1
    assert report["pass_rate"] == 1

from pathlib import Path
from unittest.mock import patch

from evaluation import run_evaluation


def test_evaluation_main_writes_report(tmp_path, monkeypatch):
    dataset = [
        {
            "id": "test_case",
            "prompt": "Describe this desk.",
            "image_path": "desk.jpg",
            "expected_risk_level": "low",
            "expected_phrases": ["desk", "table"],
            "must_not_include": ["guaranteed safe"],
        }
    ]

    dataset_dir = tmp_path / "evaluation" / "datasets"
    dataset_dir.mkdir(parents=True)

    dataset_path = dataset_dir / "assistive_eval_dataset.json"
    dataset_path.write_text(json.dumps(dataset), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    run_evaluation.main()

    report_path = Path("logs/evaluation_report.json")

    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["total"] == 1
    assert report["passed"] == 1
    assert report["pass_rate"] == 1