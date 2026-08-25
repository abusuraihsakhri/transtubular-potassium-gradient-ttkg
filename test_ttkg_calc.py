import pytest
from ttkg_calc import (
    calc_ttkg,
    calc_urine_k_cr_ratio,
    calc_ttna_gradient,
    full_potassium_assessment,
    main,
)


# --- TTKG ---

def test_ttkg_normal():
    """UK=60, POsm=285, UOsm=300, PK=4.0 → (60×285)/(300×4) = 14.25"""
    r = calc_ttkg(60, 285, 300, 4.0)
    assert abs(r["ttkg"] - 14.25) < 0.01
    assert r["clinical_context"] == "normokalemia"


def test_ttkg_hypokalemia_appropriate():
    """Low K, low UK → appropriate conservation"""
    r = calc_ttkg(5, 285, 400, 2.5)
    assert r["ttkg"] < 2
    assert r["clinical_context"] == "hypokalemia"
    assert "conservation" in r["interpretation"].lower()


def test_ttkg_hypokalemia_wasting():
    """Low K but high UK → inappropriate wasting"""
    r = calc_ttkg(40, 285, 400, 2.5)
    assert r["ttkg"] > 4
    assert "wasting" in r["interpretation"].lower()


def test_ttkg_hyperkalemia_retention():
    """High K, low UK → inappropriate retention"""
    r = calc_ttkg(10, 290, 350, 6.5)
    assert r["ttkg"] < 6
    assert r["clinical_context"] == "hyperkalemia"
    assert "retention" in r["interpretation"].lower()


def test_ttkg_hyperkalemia_excretion():
    """High K, high UK → appropriate excretion"""
    r = calc_ttkg(80, 290, 350, 6.0)
    assert r["ttkg"] > 10
    assert "excretion" in r["interpretation"].lower()


def test_ttkg_hyperkalemia_indeterminate():
    """Borderline TTKG in hyperkalemia: need TTKG between 6 and 10.
    TTKG = (UK × POsm) / (UOsm × PK) = (50 × 290) / (350 × 6.0) = 14500/2100 = 6.9"""
    r = calc_ttkg(50, 290, 350, 6.0)
    assert 6 <= r["ttkg"] <= 10
    assert "indeterminate" in r["interpretation"].lower()


def test_ttkg_hypokalemia_indeterminate():
    """Borderline TTKG in hypokalemia"""
    # TTKG between 2 and 4
    # UK=15, POsm=285, UOsm=400, PK=2.5 → (15×285)/(400×2.5) = 4275/1000 = 4.275
    # Need TTKG ~3: UK=10, POsm=285, UOsm=400, PK=2.5 → 2850/1000 = 2.85
    r = calc_ttkg(10, 285, 400, 2.5)
    assert 2 <= r["ttkg"] <= 4
    assert "indeterminate" in r["interpretation"].lower()


def test_ttkg_formula():
    """Verify formula: (UK × POsm) / (UOsm × PK)"""
    uk, posm, uosm, pk = 30, 280, 350, 5.0
    expected = (uk * posm) / (uosm * pk)
    r = calc_ttkg(uk, posm, uosm, pk)
    assert abs(r["ttkg"] - round(expected, 2)) < 0.01


def test_ttkg_invalid_plasma_k():
    with pytest.raises(ValueError):
        calc_ttkg(30, 285, 350, 0)


def test_ttkg_invalid_urine_osm():
    with pytest.raises(ValueError):
        calc_ttkg(30, 285, 0, 4.0)


# --- Urine K/Cr Ratio ---

def test_k_cr_ratio_conservation():
    """Low K/Cr → appropriate conservation"""
    r = calc_urine_k_cr_ratio(10, 200)
    # 10/200 × 100 = 5 mEq/g
    assert r["urine_k_cr_ratio_meq_g"] == 5.0
    assert "conservation" in r["interpretation"].lower()


def test_k_cr_ratio_wasting():
    """High K/Cr → significant wasting"""
    r = calc_urine_k_cr_ratio(100, 20)
    # 100/20 × 100 = 500 mEq/g
    assert r["urine_k_cr_ratio_meq_g"] == 500.0
    assert "wasting" in r["interpretation"].lower()


def test_k_cr_ratio_indeterminate():
    r = calc_urine_k_cr_ratio(50, 50)
    # 50/50 × 100 = 100 mEq/g
    assert r["urine_k_cr_ratio_meq_g"] == 100.0
    assert "indeterminate" in r["interpretation"].lower()


def test_k_cr_ratio_boundary():
    """Boundary at 13 mEq/g"""
    # Need UK/UCr × 100 = 13 → UK/UCr = 0.13
    r = calc_urine_k_cr_ratio(13, 100)
    assert r["urine_k_cr_ratio_meq_g"] == 13.0


# --- TTNaG ---

def test_ttnag_low():
    """Low TTNaG → effective Na reabsorption"""
    r = calc_ttna_gradient(10, 140, 400, 285)
    expected = (10 * 285) / (400 * 140)
    assert abs(r["ttnag"] - round(expected, 2)) < 0.01
    assert "reabsorption" in r["interpretation"].lower()


def test_ttnag_normal():
    r = calc_ttna_gradient(50, 140, 300, 285)
    # (50×285)/(300×140) = 14250/42000 = 0.339
    assert r["ttnag"] < 1


def test_ttnag_high():
    """High TTNaG → impaired reabsorption"""
    r = calc_ttna_gradient(100, 140, 300, 285)
    # (100×285)/(300×140) = 28500/42000 = 0.679
    # Still < 1, need higher values
    r = calc_ttna_gradient(200, 130, 300, 285)
    # (200×285)/(300×130) = 57000/39000 = 1.46
    assert r["ttnag"] > 1


# --- Full Assessment ---

def test_full_assessment_basic():
    r = full_potassium_assessment(5, 2.5, 285, 400)
    assert "ttkg" in r


def test_full_assessment_with_optional():
    r = full_potassium_assessment(5, 2.5, 285, 400,
                                   urine_cr=100, urine_na=20, plasma_na=140)
    assert "ttkg" in r
    assert "urine_k_cr_ratio" in r
    assert "ttnag" in r


def test_full_assessment_hypokalemia():
    r = full_potassium_assessment(5, 2.5, 285, 400, urine_cr=100)
    assert r["ttkg"]["clinical_context"] == "hypokalemia"
    assert "urine_k_cr_ratio" in r


# --- CLI ---

def test_cli_ttkg():
    assert main(["ttkg", "--urine-k", "30", "--plasma-osm", "285",
                  "--urine-osm", "350", "--plasma-k", "4.0"]) == 0


def test_cli_k_cr():
    assert main(["k-cr", "--urine-k", "25", "--urine-cr", "100"]) == 0


def test_cli_full():
    assert main(["full", "--urine-k", "5", "--plasma-k", "2.5",
                  "--plasma-osm", "285", "--urine-osm", "400"]) == 0
