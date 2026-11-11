# PoisonGuard — Week 10 Advanced Security Report

## 1. Project Overview

**Project:** PoisonGuard — Automated Framework for Detecting and Preventing Data Poisoning and Backdoor Attacks in Machine Learning Models

**Week:** 10

**Focus:** Advanced Security Enhancements and Dashboard Integration

**Model:** ResNet18

**Dataset:** CIFAR-10

## 2. Objective

The objective of Week 10 was to extend PoisonGuard with advanced security capabilities that improve model integrity verification, explainability, security evaluation, attack simulation, and threat intelligence mapping.

Five security features were implemented and integrated into the Advanced Security dashboard.

## 3. Implemented Security Features

### 3.1 Explainable AI (XAI)

- Generates rule-based explanations using supplied detector evidence.
- Displays sample ID and risk score.
- Reports detected security signals and supporting evidence.
- Provides recommendations based on risk score.
- Uses the following recommendation levels:
  - Risk score 80 or above: QUARANTINE_PENDING_REVIEW.
  - Risk score 50–79: MANUAL_REVIEW.
  - Risk score below 50: CONTINUE_MONITORING.
- Does not automatically quarantine samples or execute security actions.

### 3.2 Model Integrity Verification

- Implements SHA-256 checkpoint hashing.
- Calculates a checkpoint hash using a streaming file read.
- Compares the calculated hash against an independently supplied expected hash.
- Reports whether the checkpoint is VERIFIED or MODIFIED.
- Supports model integrity checking without changing the model file.

An independently trusted expected hash is required for meaningful integrity verification.

### 3.3 Automated Model Security Gate

The security gate evaluates candidate model security conditions.

Checks include:

- Evaluation completion.
- Matching evaluation counts.
- Clean accuracy threshold of at least 0.85.
- Attack Success Rate (ASR) threshold of at most 0.02.
- Vulnerable model ASR threshold of at least 0.90.
- Model integrity verification status.

Possible outcomes include:

- PASS_PENDING_MANUAL_REVIEW
- MANUAL_REVIEW
- REJECT

**Important:** A passing security gate does not automatically promote or activate a model. Existing manual authorization safeguards remain in place.

### 3.4 Controlled Attack Simulation Lab

The simulation lab provides controlled security scenarios:

1. Checkpoint tampering.
2. High-risk sample.
3. Candidate security-gate failure.

The simulations demonstrate how PoisonGuard responds to security events.

Safety controls:

- Simulations do not modify model files.
- Simulations do not promote models.
- Simulations do not activate models.
- No automatic security action is performed.

### 3.5 MITRE ATLAS Threat Mapping

The threat mapping feature connects PoisonGuard security scenarios with relevant MITRE ATLAS techniques.

| Technique ID | Technique |
|---|---|
| AML.T0020 | Training Data Poisoning |
| AML.T0018 | Manipulate AI Model |
| AML.T0015 | Evade AI Model |
| AML.T0115 | Publish Poisoned AI Artifacts |

The current mapping reports PARTIAL coverage. The mappings provide threat context and do not establish complete defense against these techniques.

## 4. Backend API Integration

The following endpoints were implemented:

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /security/explain | Generate detector-evidence explanations |
| POST | /security/verify-integrity | Verify checkpoint SHA-256 integrity |
| POST | /security/gate | Evaluate candidate model security |
| POST | /security/attack-simulation | Run controlled attack scenarios |
| GET | /security/atlas | Retrieve MITRE ATLAS mappings |

## 5. Dashboard Integration

All five features were integrated into the existing Streamlit dashboard under the **Advanced Security** section.

Dashboard panels:

- Explainable AI (XAI)
- Model Integrity Verification
- Automated Model Security Gate
- Attack Simulation Lab
- MITRE ATLAS Threat Mapping

Clickable sidebar navigation was added for direct access to each panel.

The existing dashboard design and navigation structure were preserved.

## 6. Testing and Validation

The following Week 10 test files were added:

- `tests/test_week10_security.py`
- `tests/test_week10_security_api.py`
- `tests/test_week10_security_gate.py`
- `tests/test_week10_attack_simulation.py`
- `tests/test_week10_atlas.py`

Validation performed:

- Python compilation check for the dashboard and API.
- Unit tests for security logic.
- API endpoint tests.
- Security-gate validation tests.
- Attack simulation tests.
- MITRE ATLAS mapping tests.
- Full project regression test suite.

**Recorded result:** 44 tests passed.

## 7. Security Safeguards

The implementation preserves the following safeguards:

- Model promotion requires explicit manual authorization.
- Model activation requires explicit authorization.
- Security-gate approval does not itself authorize activation.
- Integrity verification requires a trusted expected hash.
- Attack simulations do not modify model files.
- Explainability recommendations do not execute automatic actions.
- Threat mapping coverage is explicitly identified as partial.

## 8. Limitations

- XAI currently provides rule-based explanations from supplied detector evidence; it is not SHAP or LIME feature attribution.
- Integrity verification depends on the trustworthiness of the expected SHA-256 value.
- The security gate evaluates configured conditions and does not replace human review.
- Attack simulations are controlled scenarios, not a complete adversarial testing framework.
- MITRE ATLAS mappings are partial and do not demonstrate comprehensive threat coverage.
- Automatic model promotion and activation are intentionally not implemented.

## 9. Conclusion

Week 10 implementation and dashboard integration added five advanced security capabilities to PoisonGuard: explainability, model integrity verification, a model security gate, controlled attack simulation, and MITRE ATLAS threat mapping.

The complete project test suite recorded 44 passing tests. Existing manual model promotion and activation safeguards remain intact.

## 10. Final Submission Checklist

- [x] Five Advanced Security features implemented.
- [x] Backend API integration completed.
- [x] Dashboard integration completed.
- [x] Sidebar navigation added.
- [x] Full project test suite passed (44 tests).
- [x] Main README updated.
- [ ] Capture final dashboard screenshots.
- [ ] Review supporting documentation.
- [ ] Commit Week 10 documentation and code.
- [ ] Push the Week 10 branch to GitHub.

---

**Project:** PoisonGuard
**Report:** Week 10 — Advanced Security Enhancements
**Status:** Implementation and integration completed; final submission activities pending.
