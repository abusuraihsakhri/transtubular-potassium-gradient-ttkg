"""
Automated Pytest for transtubular-potassium-gradient-ttkg Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    BaseEnrichmentEngine,
    TranstubularpotassiumgradientttkgEnrichmentSuite,
    enrichment_suite,
    ELECTROLYTE_REPLACEMENT,
    NEPHROTOXIC_DRUG_INTERACTION,
    AKI_STAGING_PROGRESSION,
    CRRT_DOSE_MONITORING,
    NEPHROLOGY_CONSULT,
    TTKG_ASSESSMENT,
    DIFFERENTIAL_DIAGNOSIS,
    DRUG_REVIEW,
)

def test_enrichment_suite_execution():
    suite = TranstubularpotassiumgradientttkgEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) >= 1
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = TranstubularpotassiumgradientttkgEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0

def test_individual_engine():
    engine = BaseEnrichmentEngine("Test Engine", threshold=5.0)
    res = engine.evaluate(3.0)
    assert res.status == "OPTIMAL"
    assert res.score == 3.0

def test_engine_critical_alert():
    engine = BaseEnrichmentEngine("Test Engine", threshold=5.0)
    res = engine.evaluate(15.0)
    assert res.status == "CRITICAL_ALERT"
    assert len(res.alerts) > 0
