import pytest

from backend.app.services.threat_intelligence.atlas_mapping import (
    ATLAS_MAPPINGS,
    get_atlas_mapping,
    get_atlas_mappings,
)


def test_atlas_mapping_contains_four_techniques():
    result = get_atlas_mappings()
    assert result["mapping_count"] == 4
    assert len(result["mappings"]) == 4


def test_required_poisoning_and_model_techniques_exist():
    ids = {item["technique_id"] for item in ATLAS_MAPPINGS}
    assert {"AML.T0020", "AML.T0018", "AML.T0015", "AML.T0115"} <= ids


def test_each_mapping_has_documented_controls():
    for item in ATLAS_MAPPINGS:
        assert item["technique"]
        assert item["description"]
        assert item["existing_controls"]
        assert item["coverage"] in {"PARTIAL", "IMPLEMENTED", "NOT_IMPLEMENTED"}


def test_specific_technique_lookup():
    result = get_atlas_mapping("AML.T0020")
    assert result["technique"] == "Training Data Poisoning"


def test_unknown_technique_is_rejected():
    with pytest.raises(ValueError):
        get_atlas_mapping("AML.UNKNOWN")


def test_mapping_never_authorizes_automatic_actions():
    result = get_atlas_mappings()
    assert result["automatic_action_taken"] is False
    assert result["activation_authorized"] is False
