#!/usr/bin/env python3
"""
Transtubular Potassium Gradient (TTKG) Calculator

Real implementations for:
- TTKG = (UK × POsm) / (UOsm × PK)
- Interpretation for hypo- and hyperkalemia
- Aldosterone assessment
- Urine K/Cr ratio
- Transtubular Na gradient (TTNaG)

References: West ML et al. (NEJM 1986), Kamel KS et al. (Kidney Int 2002)
Stdlib only.
"""

import argparse
import json
import sys
from typing import Dict, Any


def calc_ttkg(urine_k: float, plasma_osm: float, urine_osm: float,
              plasma_k: float) -> Dict[str, Any]:
    """
    Transtubular Potassium Gradient (TTKG).

    TTKG = (UK × POsm) / (UOsm × PK)

    Interpretation depends on clinical context:

    In HYPOKALEMIA (K < 3.5):
        TTKG < 2: Appropriate renal K conservation (extrarenal loss)
        TTKG > 4: Inappropriate renal K wasting (renal cause)

    In HYPERKALEMIA (K > 5.0):
        TTKG < 6: Inappropriate K retention (hypoaldosteronism, K-sparing diuretics)
        TTKG > 10: Appropriate renal K excretion (extrarenal cause)

    Normal TTKG: 8-9

    Args:
        urine_k: Urine potassium (mEq/L)
        plasma_osm: Plasma osmolality (mOsm/kg)
        urine_osm: Urine osmolality (mOsm/kg)
        plasma_k: Plasma/serum potassium (mEq/L)

    Returns:
        Dict with TTKG and interpretation
    """
    if plasma_k <= 0:
        raise ValueError("Plasma potassium must be positive")
    if urine_osm <= 0:
        raise ValueError("Urine osmolality must be positive")
    if urine_k < 0:
        raise ValueError("Urine potassium cannot be negative")
    if plasma_osm <= 0:
        raise ValueError("Plasma osmolality must be positive")

    ttkg = (urine_k * plasma_osm) / (urine_osm * plasma_k)

    # Determine clinical context
    if plasma_k < 3.5:
        context = "hypokalemia"
        if ttkg < 2:
            interpretation = "Appropriate renal K conservation"
            aldosterone_status = "Appropriate aldosterone response"
            etiology = "Extrarenal K loss (GI losses, poor intake, transcellular shift)"
            recommendation = ("Kidneys are appropriately conserving potassium. "
                              "Look for GI losses (vomiting, diarrhea), poor intake, or redistribution.")
        elif ttkg <= 4:
            interpretation = "Indeterminate"
            aldosterone_status = "Uncertain"
            etiology = "Mixed or early renal K wasting"
            recommendation = "Borderline TTKG. Correlate with clinical context and repeat labs."
        else:
            interpretation = "Inappropriate renal K wasting"
            aldosterone_status = "Excessive or inappropriate aldosterone effect"
            etiology = ("Renal K wasting: hyperaldosteronism, Bartter/Gitelman syndrome, "
                        "Mg deficiency, amphotericin B, renal tubular acidosis")
            recommendation = ("Kidneys are inappropriately wasting potassium. "
                              "Evaluate for hyperaldosteronism, diuretics, RTA, or Mg deficiency.")

    elif plasma_k > 5.0:
        context = "hyperkalemia"
        if ttkg < 6:
            interpretation = "Inappropriate K retention"
            aldosterone_status = "Deficient or blocked aldosterone"
            etiology = ("Hypoaldosteronism (Addison's, type 4 RTA), "
                        "K-sparing diuretics, ACE inhibitors/ARBs, "
                        "NSAIDs, trimethoprim, pentamidine")
            recommendation = ("Kidneys are not excreting potassium adequately. "
                              "Evaluate for hypoaldosteronism, medications blocking RAAS, or CKD.")
        elif ttkg <= 10:
            interpretation = "Indeterminate"
            aldosterone_status = "Partial response"
            etiology = "Mixed factors"
            recommendation = "Borderline response. Correlate with renal function and medications."
        else:
            interpretation = "Appropriate renal K excretion"
            aldosterone_status = "Normal aldosterone response"
            etiology = "Extrarenal K load (intake, tissue breakdown, transcellular shift)"
            recommendation = ("Kidneys are appropriately excreting potassium. "
                              "Look for extrarenal causes: dietary excess, rhabdomyolysis, "
                              "tumor lysis, acidosis, medications.")

    else:
        context = "normokalemia"
        interpretation = "Normal potassium level"
        aldosterone_status = "Cannot assess from TTKG in normokalemia"
        etiology = "N/A"
        recommendation = "Potassium is within normal range. TTKG interpretation requires hypo- or hyperkalemia."

    return {
        "ttkg": round(ttkg, 2),
        "plasma_k": plasma_k,
        "urine_k": urine_k,
        "plasma_osm": plasma_osm,
        "urine_osm": urine_osm,
        "clinical_context": context,
        "interpretation": interpretation,
        "aldosterone_status": aldosterone_status,
        "possible_etiology": etiology,
        "recommendation": recommendation,
        "normal_range": "8-9 (in steady state)",
    }


def calc_urine_k_cr_ratio(urine_k: float, urine_cr: float) -> Dict[str, Any]:
    """
    Urine K/Creatinine ratio.

    Useful when urine osmolality not available.

    UK/UCr (mEq/mg):
        < 13 mEq/g (or < 1.5 mEq/mmol): Appropriate K conservation
        > 200 mEq/g (or > 23 mEq/mmol): Significant K wasting

    Args:
        urine_k: Urine potassium (mEq/L)
        urine_cr: Urine creatinine (mg/dL)

    Returns:
        Dict with K/Cr ratio and interpretation
    """
    if urine_cr <= 0:
        raise ValueError("Urine creatinine must be positive")
    if urine_k < 0:
        raise ValueError("Urine potassium cannot be negative")

    # Ratio in mEq/mg (× 100 to get mEq/g)
    ratio_meq_mg = urine_k / urine_cr
    ratio_meq_g = ratio_meq_mg * 100.0

    if ratio_meq_g < 13:
        interpretation = "Appropriate renal K conservation"
        recommendation = "Low K/Cr ratio suggests kidneys are conserving K appropriately."
    elif ratio_meq_g <= 200:
        interpretation = "Indeterminate"
        recommendation = "Borderline ratio. Correlate with clinical context."
    else:
        interpretation = "Significant renal K wasting"
        recommendation = "High K/Cr ratio suggests inappropriate renal K loss."

    return {
        "urine_k_cr_ratio_meq_g": round(ratio_meq_g, 1),
        "urine_k_cr_ratio_meq_mg": round(ratio_meq_mg, 4),
        "urine_k": urine_k,
        "urine_cr": urine_cr,
        "interpretation": interpretation,
        "recommendation": recommendation,
    }


def calc_ttna_gradient(urine_na: float, plasma_na: float,
                        urine_osm: float, plasma_osm: float) -> Dict[str, Any]:
    """
    Transtubular Sodium Gradient (TTNaG).

    TTNaG = (UNa × POsm) / (UOsm × PNa)

    Similar concept to TTKG but for sodium.
    Low TTNaG (< 1): Effective Na reabsorption (volume depletion)
    High TTNaG (> 3): Impaired Na reabsorption

    Args:
        urine_na: Urine sodium (mEq/L)
        plasma_na: Plasma sodium (mEq/L)
        urine_osm: Urine osmolality (mOsm/kg)
        plasma_osm: Plasma osmolality (mOsm/kg)

    Returns:
        Dict with TTNaG and interpretation
    """
    if plasma_na <= 0:
        raise ValueError("Plasma sodium must be positive")
    if urine_osm <= 0:
        raise ValueError("Urine osmolality must be positive")
    if plasma_osm <= 0:
        raise ValueError("Plasma osmolality must be positive")

    ttnag = (urine_na * plasma_osm) / (urine_osm * plasma_na)

    if ttnag < 1:
        interpretation = "Effective Na reabsorption"
        recommendation = "Low TTNaG suggests volume depletion with appropriate Na conservation."
    elif ttnag <= 3:
        interpretation = "Normal Na handling"
        recommendation = "TTNaG within normal range."
    else:
        interpretation = "Impaired Na reabsorption"
        recommendation = "High TTNaG suggests impaired tubular Na reabsorption (ATN, diuretics)."

    return {
        "ttnag": round(ttnag, 2),
        "urine_na": urine_na,
        "plasma_na": plasma_na,
        "urine_osm": urine_osm,
        "plasma_osm": plasma_osm,
        "interpretation": interpretation,
        "recommendation": recommendation,
    }


def full_potassium_assessment(urine_k: float, plasma_k: float,
                               plasma_osm: float, urine_osm: float,
                               urine_cr: float = None,
                               urine_na: float = None,
                               plasma_na: float = None) -> Dict[str, Any]:
    """
    Complete potassium handling assessment.
    """
    result = {
        "ttkg": calc_ttkg(urine_k, plasma_osm, urine_osm, plasma_k),
    }

    if urine_cr is not None and urine_cr > 0:
        result["urine_k_cr_ratio"] = calc_urine_k_cr_ratio(urine_k, urine_cr)

    if (urine_na is not None and plasma_na is not None and
            plasma_na > 0 and urine_osm > 0 and plasma_osm > 0):
        result["ttnag"] = calc_ttna_gradient(urine_na, plasma_na, urine_osm, plasma_osm)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ttkg-calculator",
        description="Transtubular Potassium Gradient (TTKG) Calculator"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # TTKG
    p_ttkg = sub.add_parser("ttkg", help="Calculate TTKG")
    p_ttkg.add_argument("--urine-k", type=float, required=True, help="Urine K (mEq/L)")
    p_ttkg.add_argument("--plasma-osm", type=float, required=True, help="Plasma Osm (mOsm/kg)")
    p_ttkg.add_argument("--urine-osm", type=float, required=True, help="Urine Osm (mOsm/kg)")
    p_ttkg.add_argument("--plasma-k", type=float, required=True, help="Plasma K (mEq/L)")

    # Urine K/Cr ratio
    p_kcr = sub.add_parser("k-cr", help="Urine K/Cr ratio")
    p_kcr.add_argument("--urine-k", type=float, required=True, help="Urine K (mEq/L)")
    p_kcr.add_argument("--urine-cr", type=float, required=True, help="Urine Cr (mg/dL)")

    # TTNaG
    p_na = sub.add_parser("ttnag", help="Transtubular Na gradient")
    p_na.add_argument("--urine-na", type=float, required=True, help="Urine Na (mEq/L)")
    p_na.add_argument("--plasma-na", type=float, required=True, help="Plasma Na (mEq/L)")
    p_na.add_argument("--urine-osm", type=float, required=True, help="Urine Osm (mOsm/kg)")
    p_na.add_argument("--plasma-osm", type=float, required=True, help="Plasma Osm (mOsm/kg)")

    # Full assessment
    p_full = sub.add_parser("full", help="Full K assessment")
    p_full.add_argument("--urine-k", type=float, required=True, help="Urine K (mEq/L)")
    p_full.add_argument("--plasma-k", type=float, required=True, help="Plasma K (mEq/L)")
    p_full.add_argument("--plasma-osm", type=float, required=True, help="Plasma Osm (mOsm/kg)")
    p_full.add_argument("--urine-osm", type=float, required=True, help="Urine Osm (mOsm/kg)")
    p_full.add_argument("--urine-cr", type=float, default=None, help="Urine Cr (mg/dL)")
    p_full.add_argument("--urine-na", type=float, default=None, help="Urine Na (mEq/L)")
    p_full.add_argument("--plasma-na", type=float, default=None, help="Plasma Na (mEq/L)")

    args = parser.parse_args(argv)

    if args.command == "ttkg":
        result = calc_ttkg(args.urine_k, args.plasma_osm, args.urine_osm, args.plasma_k)
    elif args.command == "k-cr":
        result = calc_urine_k_cr_ratio(args.urine_k, args.urine_cr)
    elif args.command == "ttnag":
        result = calc_ttna_gradient(args.urine_na, args.plasma_na, args.urine_osm, args.plasma_osm)
    elif args.command == "full":
        result = full_potassium_assessment(args.urine_k, args.plasma_k,
                                            args.plasma_osm, args.urine_osm,
                                            args.urine_cr, args.urine_na, args.plasma_na)
    else:
        parser.print_help()
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
