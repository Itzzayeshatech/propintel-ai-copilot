from typing import List


class ExplainabilityService:
    """
    Explainability Engine - Final Stage of the Underwriting Pipeline.

    Produces TWO outputs:
    1. simplified  - 3 risk factors, 1 stress line, 1 decision rationale.
                     Readable by non-technical judges, compliance officers, borrowers.
    2. audit_trace - triggered rules, reasoning chain, compliance verdict.
                     Readable by RBI auditors, internal risk committees.
    """

    # ── Simplified output ─────────────────────────────────────────────────────
    @staticmethod
    def generate_simplified_output(
        base: dict,
        stressed: dict,
        decision: str,
        risk_level: str,
        triggered_rules: List[str]
    ) -> dict:

        # 1. Top-3 Risk Factors (ordered by materiality)
        factors = []

        # LTV is the primary collateral risk signal
        if stressed["stress_ltv"] > 85:
            factors.append(f"Stress LTV at {stressed['stress_ltv']:.1f}% - exceeds 85% safety floor")
        elif stressed["stress_ltv"] > 75:
            factors.append(f"Stress LTV at {stressed['stress_ltv']:.1f}% - within caution zone (75-85%)")

        # Property value erosion
        drop = stressed.get("property_value_drop_pct", 0)
        if drop > 0:
            factors.append(
                f"Collateral value erodes by {drop:.0f}% under active stress scenarios"
            )

        # Liquidity of micro-market
        if stressed["liquidity_score"] < 0.45:
            factors.append(
                f"Low market liquidity ({stressed['liquidity_score']:.2f}) - asset recovery risk elevated"
            )
        elif stressed["liquidity_score"] < 0.65:
            factors.append(
                f"Moderate market liquidity ({stressed['liquidity_score']:.2f}) - liquidation timeline extended"
            )

        # Policy rule violations (credit, DTI)
        if triggered_rules:
            factors.append(f"{len(triggered_rules)} policy violation(s): {triggered_rules[0]}")

        if not factors:
            factors.append("Standard risk profile - no material flags identified")

        factors = factors[:3]  # cap at 3

        # 2. Stress Impact Summary (1 line)
        ltv_delta = stressed["stress_ltv"] - base["base_ltv"]
        mpv = base["market_property_value"] / 1e7  # convert to crore
        spv = stressed["stressed_property_value"] / 1e7
        stress_summary = (
            f"Market stress compresses collateral from INR {mpv:.2f}Cr to INR {spv:.2f}Cr, "
            f"pushing LTV up by {ltv_delta:+.1f}%."
        )

        # 3. Decision Rationale (1 line)
        rationale_map = {
            "REJECT":      "Rejected - stressed collateral cover insufficient to protect NBFC principal.",
            "CONDITIONAL": "Conditionally approved - risk premium and additional documentation required.",
            "APPROVE":     "Approved - collateral cover remains adequate under all modelled stress scenarios.",
        }
        rationale = rationale_map.get(decision, "Decision pending further review.")

        return {
            "key_risk_factors":     factors,
            "stress_impact_summary": stress_summary,
            "decision_rationale":   rationale,
        }

    # ── Audit trace ───────────────────────────────────────────────────────────
    @staticmethod
    def generate_audit_trace(
        triggered_rules: List[str],
        risk_level: str,
        stress_summary: str
    ) -> dict:

        reasoning_chain = [
            f"Stage 1 - Valuation: Asset valued using micro-market price index.",
            f"Stage 2 - Stress: Macro-economic scenarios applied; collateral value re-computed.",
            f"Stage 3 - Risk: Portfolio risk classified as '{risk_level}' based on stressed LTV and liquidity.",
            f"Stage 4 - ROI: Net yield calculated after segment-adjusted default probability.",
            f"Stage 5 - Decision: Final recommendation issued.",
            f"Stress note: {stress_summary}",
        ]

        if triggered_rules:
            for r in triggered_rules:
                reasoning_chain.append(f"Policy flag: {r}")

        compliance_map = {
            "HIGH":   "FAILED - Mandatory review required before disbursement.",
            "MEDIUM": "CONDITIONAL - Risk committee sign-off required.",
            "LOW":    "PASSED - Proceed with standard disbursement workflow.",
        }

        return {
            "triggered_rules":      triggered_rules,
            "risk_reasoning_chain": reasoning_chain,
            "compliance_check":     compliance_map.get(risk_level, "REVIEW REQUIRED"),
        }
