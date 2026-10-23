import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "experiments" / "week7" / "results"

VULNERABLE_FILE = RESULTS / "vulnerable_model_evaluation.json"
CANDIDATE_FILE = RESULTS / "sanitized_candidate_evaluation.json"
OUTPUT_FILE = RESULTS / "promotion_validation.json"

# Explicit project validation thresholds.
MIN_CLEAN_ACCURACY = 0.85
MAX_ATTACK_SUCCESS_RATE = 0.02
MIN_VULNERABLE_ATTACK_SUCCESS_RATE = 0.90


def load_json(path):
    if not path.is_file():
        raise FileNotFoundError(
            f"Required evaluation report is missing: {path}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-report", type=Path, default=CANDIDATE_FILE)
    parser.add_argument("--vulnerable-report", type=Path, default=VULNERABLE_FILE)
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    args = parser.parse_args()

    vulnerable = load_json(args.vulnerable_report)
    candidate = load_json(args.candidate_report)

    checks = {
        "candidate_evaluation_completed": (
            candidate.get("status") == "evaluated_not_yet_approved"
        ),
        "vulnerable_evaluation_completed": (
            vulnerable.get("status") == "evaluated_not_yet_approved"
        ),
        "same_test_sample_count": (
            candidate.get("test_samples")
            == vulnerable.get("test_samples")
        ),
        "same_attack_eligible_sample_count": (
            candidate.get("attack_eligible_samples")
            == vulnerable.get("attack_eligible_samples")
        ),
        "candidate_clean_accuracy_passes": (
            candidate.get("clean_accuracy", 0)
            >= MIN_CLEAN_ACCURACY
        ),
        "candidate_attack_success_rate_passes": (
            candidate.get("attack_success_rate", 1)
            <= MAX_ATTACK_SUCCESS_RATE
        ),
        "vulnerable_model_shows_attack": (
            vulnerable.get("attack_success_rate", 0)
            >= MIN_VULNERABLE_ATTACK_SUCCESS_RATE
        ),
    }

    passed = all(checks.values())

    report = {
        "project": "PoisonGuard",
        "stage": "Week 7 candidate promotion validation",
        "candidate_model": candidate.get("model"),
        "vulnerable_model": vulnerable.get("model"),
        "thresholds": {
            "minimum_clean_accuracy": MIN_CLEAN_ACCURACY,
            "maximum_attack_success_rate": MAX_ATTACK_SUCCESS_RATE,
            "minimum_vulnerable_attack_success_rate": (
                MIN_VULNERABLE_ATTACK_SUCCESS_RATE
            ),
        },
        "observed_metrics": {
            "candidate_clean_accuracy": candidate.get(
                "clean_accuracy"
            ),
            "candidate_attack_success_rate": candidate.get(
                "attack_success_rate"
            ),
            "vulnerable_attack_success_rate": vulnerable.get(
                "attack_success_rate"
            ),
        },
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "validation_status": (
            "passed_pending_manual_review"
            if passed
            else "blocked"
        ),
        "promotion_status": "not_promoted",
        "limitations": [
            "Passing these checks does not prove all backdoors "
            "or poisoning attacks have been eliminated.",
            "The checks cover the configured CIFAR-10 test and "
            "single 4x4 white-square trigger evaluation.",
            "Manual review and additional validation are required "
            "before model promotion."
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print("\n===== WEEK 7 PROMOTION VALIDATION =====")
    for name, result in checks.items():
        print(f"{'PASS' if result else 'FAIL'}: {name}")

    print(
        f"\nChecks passed: {report['checks_passed']}"
        f"/{report['checks_total']}"
    )
    print("Validation status:", report["validation_status"])
    print("Promotion status:", report["promotion_status"])
    print("Report saved to:", args.output)


if __name__ == "__main__":
    main()
