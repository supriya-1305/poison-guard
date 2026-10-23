import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ml/evaluation/validate_week7_promotion.py"
REPORT = ROOT / "experiments/week7/results/promotion_validation.json"


def test_week7_validation_gate_runs_successfully():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        env={
            **__import__("os").environ,
            "PYTHONPATH": str(ROOT),
        },
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert REPORT.is_file()


def test_week7_validation_does_not_promote_automatically():
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["promotion_status"] == "not_promoted"
    assert report["validation_status"] in {
        "passed_pending_manual_review",
        "blocked",
    }


def test_week7_validation_contains_all_required_checks():
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    required_checks = {
        "candidate_evaluation_completed",
        "vulnerable_evaluation_completed",
        "same_test_sample_count",
        "same_attack_eligible_sample_count",
        "candidate_clean_accuracy_passes",
        "candidate_attack_success_rate_passes",
        "vulnerable_model_shows_attack",
    }

    assert required_checks.issubset(report["checks"])
