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
import math
import sys
from typing import Dict, Any


def calc_ttkg(urine_k: float, plasma_osm: float, urine_osm: float,
              plasma_k: float, urine_na: float = None) -> Dict[str, Any]:
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

    measurements = {"urine_k": urine_k, "plasma_osm": plasma_osm,
                    "urine_osm": urine_osm, "plasma_k": plasma_k}
    if urine_na is not None:
        measurements["urine_na"] = urine_na
    for name, value in measurements.items():
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if urine_na is not None and urine_na < 0:
        raise ValueError("Urine sodium cannot be negative")

    ttkg = (urine_k * plasma_osm) / (urine_osm * plasma_k)
    limitations = [
        "TTKG is a historical estimate with disputed physiological validity "
        "(medullary urea recycling); do not use alone for clinical decisions."
    ]
    if urine_osm < plasma_osm:
        limitations.append("Urine osmolality is below plasma osmolality.")
    if urine_na is None:
        limitations.append("Urine sodium was not supplied; distal sodium delivery cannot be assessed.")
    elif urine_na < 25:
        limitations.append("Urine sodium below 25 mEq/L invalidates the traditional TTKG assumptions.")
    assumptions_met = urine_osm >= plasma_osm and urine_na is not None and urine_na >= 25

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

    # Historical categories are retained for educational backward compatibility.
    # Neither the estimate nor an apparently met prerequisite establishes aldosterone function.
    aldosterone_status = "TTKG alone cannot establish aldosterone status"
    if not assumptions_met:
        recommendation = (
            "TTKG prerequisites are unverified or unmet. Do not apply its historical "
            "interpretation clinically; consider urine K/creatinine and the full evaluation."
        )
    else:
        recommendation += " TTKG has disputed clinical validity; corroborate independently."

    return {
        "ttkg": round(ttkg, 2),
        "assumptions_met": assumptions_met,
        "limitations": limitations,
        "plasma_k": plasma_k,
        "urine_k": urine_k,
        "plasma_osm": plasma_osm,
        "urine_osm": urine_osm,
        "clinical_context": context,
        "interpretation": interpretation,
        "aldosterone_status": aldosterone_status,
        "possible_etiology": etiology,
        "recommendation": recommendation,
        "normal_range": "No validated universal normal range",
    }


def calc_urine_k_cr_ratio(urine_k: float, urine_cr: float) -> Dict[str, Any]:
    """
    Urine K/Creatinine ratio.

    Useful when urine osmolality not available.

    Spot urine K/Cr (mEq/g creatinine):
        <13: Suggests renal potassium conservation in hypokalemia
        >13: Suggests possible renal potassium wasting in hypokalemia
        (At 13: Threshold value; clinical context required)
        13 mEq/g is approximately 1.5 mEq/mmol creatinine.

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

    if not math.isfinite(urine_k) or not math.isfinite(urine_cr):
        raise ValueError("Urine potassium and creatinine must be finite")

    # Ratio in mEq/mg (× 100 to get mEq/g)
    ratio_meq_mg = urine_k / urine_cr
    ratio_meq_g = ratio_meq_mg * 100.0

    if ratio_meq_g < 13:
        interpretation = "Appropriate renal K conservation"
        recommendation = "Low K/Cr ratio suggests kidneys are conserving K appropriately."
    elif ratio_meq_g == 13:
        interpretation = "At threshold"
        recommendation = "At the conventional 13 mEq/g threshold; interpret in clinical context."
    else:
        interpretation = "Possible renal K wasting"
        recommendation = ("Above 13 mEq/g may indicate renal potassium loss during hypokalemia; "
                          "interpret with medication use and acid-base status.")

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

    if urine_na < 0:
        raise ValueError("Urine sodium cannot be negative")
    if not all(math.isfinite(v) for v in (urine_na, plasma_na, urine_osm, plasma_osm)):
        raise ValueError("Sodium and osmolality values must be finite")

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
        "limitation": "TTNaG is not a validated stand-alone clinical diagnostic test.",
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
        "ttkg": calc_ttkg(urine_k, plasma_osm, urine_osm, plasma_k, urine_na=urine_na),
    }

    if urine_cr is not None:
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
    p_ttkg.add_argument("--urine-na", type=float, default=None, help="Optional urine Na (mEq/L) to check TTKG assumptions")

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

    # Audit (enterprise supervisor)
    p_audit = sub.add_parser("audit", help="Run enterprise supervisor audit task")
    p_audit.add_argument("--task-id", type=str, required=True, help="Task identifier")
    p_audit.add_argument("--target-id", type=str, default="SPECIMEN-001", help="Target identifier")
    p_audit.add_argument("--primary-metric", type=float, default=10.0, help="Primary metric value")
    p_audit.add_argument("--secondary-metric", type=float, default=5.0, help="Secondary metric value")
    p_audit.add_argument("--status-descriptor", type=str, default="NOMINAL", help="Status descriptor")
    p_audit.add_argument("--critical", action="store_true", help="Flag as critical")

    # Chat (enterprise supervisor)
    p_chat = sub.add_parser("chat", help="Query the enterprise supervisor chat")
    p_chat.add_argument("query", nargs="+", help="Query string")

    # Verify audit trail
    p_verify = sub.add_parser("verify-audit", help="Verify HMAC-SHA256 audit trail integrity")

    args = parser.parse_args(argv)

    if args.command == "ttkg":
        result = calc_ttkg(args.urine_k, args.plasma_osm, args.urine_osm, args.plasma_k, urine_na=args.urine_na)
    elif args.command == "k-cr":
        result = calc_urine_k_cr_ratio(args.urine_k, args.urine_cr)
    elif args.command == "ttnag":
        result = calc_ttna_gradient(args.urine_na, args.plasma_na, args.urine_osm, args.plasma_osm)
    elif args.command == "full":
        result = full_potassium_assessment(args.urine_k, args.plasma_k,
                                            args.plasma_osm, args.urine_osm,
                                            args.urine_cr, args.urine_na, args.plasma_na)
    elif args.command == "audit":
        from agents.models import SystemTaskPayload
        from agents.supervisor import SystemSupervisor
        supervisor = SystemSupervisor(model_provider="mock")
        payload = SystemTaskPayload(
            task_id=args.task_id,
            target_identifier=args.target_id,
            primary_metric=args.primary_metric,
            secondary_metric=args.secondary_metric,
            status_descriptor=args.status_descriptor,
            is_critical_flag=args.critical,
        )
        dossier = supervisor.process_task(payload)
        result = dossier.to_dict()
    elif args.command == "chat":
        from agents.supervisor import SystemSupervisor
        supervisor = SystemSupervisor(model_provider="mock")
        query = " ".join(args.query)
        response = supervisor.query_supervisory_chat(query)
        result = {"response": response}
    elif args.command == "verify-audit":
        from agents.base import AuditLogger
        result = {"audit_integrity_verified": AuditLogger.verify_integrity()}
    else:
        parser.print_help()
        return 1

    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
