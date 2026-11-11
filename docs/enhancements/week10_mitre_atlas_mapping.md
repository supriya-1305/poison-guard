# Week 10 — MITRE ATLAS Threat Mapping

## Purpose
Document how PoisonGuard's existing defensive capabilities relate to
selected MITRE ATLAS techniques.

## Mappings

| ATLAS ID | Technique | PoisonGuard relevance |
|---|---|---|
| AML.T0020 | Training Data Poisoning | Dataset poisoning and backdoor experiments |
| AML.T0018 | Manipulate AI Model | Model artifact and checkpoint integrity |
| AML.T0015 | Evade AI Model | Adversarial input and evasion evaluation |
| AML.T0115 | Publish Poisoned AI Artifacts | Model and dataset supply-chain integrity |

## Coverage limitation
Mappings describe related project controls; they do not prove that every
attack variant is detected or prevented. Coverage is currently marked
PARTIAL and requires further validation.

## Safety
This module is informational only. It does not modify model files,
activate models, promote candidates, or execute attacks.

## Reference
MITRE ATLAS: https://atlas.mitre.org/
