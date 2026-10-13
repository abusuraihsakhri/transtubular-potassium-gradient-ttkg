"""Clinical calculation and audit integrity regression tests."""
import math
import pytest

from ttkg_calc import calc_ttkg, calc_ttna_gradient, calc_urine_k_cr_ratio, full_potassium_assessment
from agents.base import AuditTrail
from agents.llm_factory import LLMFactory


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
def test_ttkg_rejects_nonfinite(invalid):
    with pytest.raises(ValueError, match="finite"):
        calc_ttkg(5, 285, 400, invalid)
    with pytest.raises(ValueError, match="finite"):
        calc_ttkg(5, invalid, 400, 2.5)


def test_ttkg_prerequisites():
    valid = calc_ttkg(5, 285, 400, 2.5, urine_na=30)
    assert valid["assumptions_met"] is True
    assert math.isclose(valid["ttkg"], 1.43, abs_tol=0.001)
    assert valid["limitations"]
    assert calc_ttkg(5, 285, 200, 2.5, urine_na=30)["assumptions_met"] is False
    assert calc_ttkg(5, 285, 400, 2.5, urine_na=20)["assumptions_met"] is False
    assert calc_ttkg(5, 285, 400, 2.5)["assumptions_met"] is False


def test_kcr_conventional_threshold():
    assert "conservation" in calc_urine_k_cr_ratio(12, 100)["interpretation"].lower()
    assert "threshold" in calc_urine_k_cr_ratio(13, 100)["interpretation"].lower()
    assert "wasting" in calc_urine_k_cr_ratio(14, 100)["interpretation"].lower()


def test_invalid_optional_measurement_must_not_be_ignored():
    with pytest.raises(ValueError):
        full_potassium_assessment(5, 2.5, 285, 400, urine_cr=-2)
    with pytest.raises(ValueError):
        calc_ttkg(5, 285, 400, 2.5, urine_na=-1)
    with pytest.raises(ValueError):
        calc_ttna_gradient(-1, 140, 400, 285)


def test_audit_detects_payload_hash_and_signature_tampering():
    audit = AuditTrail(secret_key="test-key")
    audit.log("tester", "analysis", "CALCULATION", {"task_id": "A-01"})
    audit.log("tester", "analysis", "CALCULATION", {"task_id": "A-02"})
    assert audit.verify_integrity()
    snapshot = audit.get_trail()
    snapshot[0]["event_type"] = "CHANGED"
    assert audit.verify_integrity()  # snapshot is read-only from the ledger's perspective
    audit.logs[0]["payload_hash"] = "deadbeef"
    assert not audit.verify_integrity()


def test_audit_does_not_accept_nonfinite_details():
    audit = AuditTrail(secret_key="test-key")
    with pytest.raises(ValueError):
        audit.log("tester", "analysis", "CALCULATION", {"measurement": math.inf})


def test_unimplemented_remote_model_providers_are_not_faked():
    with pytest.raises(ValueError, match="Only the deterministic mock"):
        LLMFactory.create("openai")
    assert LLMFactory.create("mock").invoke("safe test")
