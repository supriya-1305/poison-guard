"""MITRE ATLAS threat mapping for PoisonGuard.

This module documents defensive coverage. It does not execute attacks,
modify model files, or authorize model promotion.
"""

ATLAS_MAPPINGS = [
    {
        "technique_id": "AML.T0020",
        "technique": "Training Data Poisoning",
        "description": "Manipulation of training data to influence model behaviour.",
        "project_relevance": "CIFAR-10 data poisoning and backdoor experiments.",
        "existing_controls": [
            "Activation Clustering",
            "STRIP-style Detection",
            "Backdoor Risk Scoring",
        ],
        "coverage": "PARTIAL",
    },
    {
        "technique_id": "AML.T0018",
        "technique": "Manipulate AI Model",
        "description": "Manipulation of model artifacts or components to change behaviour.",
        "project_relevance": "Backdoored checkpoint and model integrity risks.",
        "existing_controls": [
            "SHA-256 Model Integrity Verification",
            "Automated Model Security Gate",
        ],
        "coverage": "PARTIAL",
    },
    {
        "technique_id": "AML.T0015",
        "technique": "Evade AI Model",
        "description": "Adversarial data designed to cause incorrect model predictions.",
        "project_relevance": "Adversarial input and runtime detection evaluation.",
        "existing_controls": [
            "Runtime Monitoring",
            "Controlled Attack Simulation",
        ],
        "coverage": "PARTIAL",
    },
    {
        "technique_id": "AML.T0115",
        "technique": "Publish Poisoned AI Artifacts",
        "description": "Publishing poisoned AI artifacts through distribution channels.",
        "project_relevance": "Model and dataset supply-chain integrity risks.",
        "existing_controls": [
            "SHA-256 Model Integrity Verification",
            "Model Registry",
        ],
        "coverage": "PARTIAL",
    },
]


def get_atlas_mappings():
    """Return documented ATLAS mappings without performing security actions."""
    return {
        "project": "PoisonGuard",
        "framework": "MITRE ATLAS",
        "mapping_count": len(ATLAS_MAPPINGS),
        "mappings": ATLAS_MAPPINGS,
        "automatic_action_taken": False,
        "activation_authorized": False,
    }


def get_atlas_mapping(technique_id):
    """Find one mapping by its exact ATLAS technique ID."""
    for mapping in ATLAS_MAPPINGS:
        if mapping["technique_id"] == technique_id:
            return mapping
    raise ValueError(f"Unknown ATLAS technique ID: {technique_id}")
