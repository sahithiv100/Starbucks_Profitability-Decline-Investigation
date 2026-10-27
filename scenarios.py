"""
scenarios.py - Recovery Scenario Engine and Prioritized Action Register
DISCLAIMER: SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA. FOR ILLUSTRATIVE BUSINESS ANALYTICS ONLY.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List

def simulate_recovery_scenario(
    df: pd.DataFrame,
    overtime_reduction_pct: float = 40.0,
    discount_reduction_bps: float = 350.0,
    waste_reduction_pct: float = 30.0,
    delivery_recoup_pct: float = 15.0,
    selective_pricing_lift_pct: float = 2.0,
    trough_quarter: str = "Q3-2024"
) -> Dict[str, Any]:
    """
    Simulates operational interventions applied to the trough quarter (Q3-2024).
    Recalculates recovered quarterly EBIT, margin improvement, and driver contributions.
    """
    df_trough = df[df["Quarter"] == trough_quarter]
    
    actual_ebit = df_trough["Operating_Profit_EBIT"].sum()
    actual_net_rev = df_trough["Net_Revenue"].sum()
    actual_gross_rev = df_trough["Gross_Revenue"].sum()
    actual_margin_pct = (actual_ebit / actual_net_rev * 100.0) if actual_net_rev > 0 else 0.0

    actual_ot_cost = df_trough["Overtime_Labor_Cost"].sum()
    actual_discounts = df_trough["Discount_Amount"].sum()
    actual_waste = df_trough["Waste_Cost"].sum()
    actual_deliv_fees = df_trough["Delivery_Fees"].sum()
    
    # 1. Overtime Reduction Savings
    # Cutting overtime reduces 1.5x wage cost down to standard rate or eliminates unneeded rush delay
    recovered_ot = actual_ot_cost * (overtime_reduction_pct / 100.0)

    # 2. Promotional Discount Rationalization
    # Shifting from blanket 50% / BOGO promos to targeted personalized loyalty rewards
    # discount_reduction_bps is in basis points of gross revenue (e.g. 350 bps = 3.5% of Gross Revenue)
    recovered_discount = actual_gross_rev * (discount_reduction_bps / 10000.0)
    # Cap discount recovery to not exceed actual discounts
    recovered_discount = min(recovered_discount, actual_discounts * 0.85)

    # 3. Waste & Spoilage Optimization
    # Smarter cold bar prep station batching and automated dairy dispensers
    recovered_waste = actual_waste * (waste_reduction_pct / 100.0)

    # 4. 3P Delivery Commission Recoup / Surcharge
    # Implementing modest 3P platform markup and shifting volume to Starbucks app MOP pickup
    recovered_delivery = actual_deliv_fees * (delivery_recoup_pct / 100.0)

    # 5. Selective Premium Modifier Pricing Lift
    # Modest +2% price adjustment on complex cold foam and syrups with zero volume elasticity impact
    recovered_pricing = actual_net_rev * (selective_pricing_lift_pct / 100.0)

    total_recovered_ebit = (
        recovered_ot 
        + recovered_discount 
        + recovered_waste 
        + recovered_delivery 
        + recovered_pricing
    )

    simulated_ebit = actual_ebit + total_recovered_ebit
    # Net revenue increases by recovered discounts and selective pricing lift
    simulated_net_rev = actual_net_rev + recovered_discount + recovered_pricing
    simulated_margin_pct = (simulated_ebit / simulated_net_rev * 100.0) if simulated_net_rev > 0 else 0.0
    margin_expansion_bps = (simulated_margin_pct - actual_margin_pct) * 100.0

    # Uncertainty / Sensitivity Range (+/- 15% execution variance)
    conservative_recovered = total_recovered_ebit * 0.82
    optimistic_recovered = total_recovered_ebit * 1.18

    recovery_bridge = [
        {"Lever": "Q3-2024 Actual EBIT (Trough)", "Impact_USD": round(actual_ebit, 2), "Type": "Baseline"},
        {"Lever": f"Overtime Reduction (-{overtime_reduction_pct:.0f}%)", "Impact_USD": round(recovered_ot, 2), "Type": "Recovery"},
        {"Lever": f"Discount Rationalization (-{discount_reduction_bps/100:.1f}%)", "Impact_USD": round(recovered_discount, 2), "Type": "Recovery"},
        {"Lever": f"Cold Bar & Food Waste Cut (-{waste_reduction_pct:.0f}%)", "Impact_USD": round(recovered_waste, 2), "Type": "Recovery"},
        {"Lever": f"Delivery Fee Surcharge (+{delivery_recoup_pct:.0f}%)", "Impact_USD": round(recovered_delivery, 2), "Type": "Recovery"},
        {"Lever": f"Selective Modifier Pricing (+{selective_pricing_lift_pct:.1f}%)", "Impact_USD": round(recovered_pricing, 2), "Type": "Recovery"},
        {"Lever": "Projected Recovered EBIT", "Impact_USD": round(simulated_ebit, 2), "Type": "Total"}
    ]

    return {
        "actual_ebit": actual_ebit,
        "simulated_ebit": simulated_ebit,
        "total_recovered_ebit": total_recovered_ebit,
        "actual_margin_pct": round(actual_margin_pct, 2),
        "simulated_margin_pct": round(simulated_margin_pct, 2),
        "margin_expansion_bps": round(margin_expansion_bps, 1),
        "conservative_recovered": round(conservative_recovered, 2),
        "optimistic_recovered": round(optimistic_recovered, 2),
        "lever_breakdown": {
            "Overtime Reduction": round(recovered_ot, 2),
            "Discount Rationalization": round(recovered_discount, 2),
            "Waste Spoilage Cut": round(recovered_waste, 2),
            "Delivery Surcharge": round(recovered_delivery, 2),
            "Selective Modifier Pricing": round(recovered_pricing, 2)
        },
        "recovery_bridge_df": pd.DataFrame(recovery_bridge)
    }

def get_action_register(simulation_results: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Returns an actionable, prioritized register of management initiatives
    ranked by impact, controllability, and speed to execution.
    """
    # If dynamic results provided, scale dollar impacts
    ot_val = simulation_results["lever_breakdown"]["Overtime Reduction"] if simulation_results else 580000.0
    disc_val = simulation_results["lever_breakdown"]["Discount Rationalization"] if simulation_results else 820000.0
    waste_val = simulation_results["lever_breakdown"]["Waste Spoilage Cut"] if simulation_results else 310000.0
    deliv_val = simulation_results["lever_breakdown"]["Delivery Surcharge"] if simulation_results else 240000.0
    price_val = simulation_results["lever_breakdown"]["Selective Modifier Pricing"] if simulation_results else 380000.0

    actions = [
        {
            "Action_ID": "ACT-101",
            "Initiative": "Rationalize Blanket Promo Discounts to Personalized Loyalty",
            "Category": "Commercial & Pricing",
            "Owner": "Chief Marketing Officer",
            "Est_Quarterly_Impact_USD": round(disc_val, 2),
            "Controllability": "High",
            "Implementation_Speed": "Immediate (2-4 Weeks)",
            "Feasibility_Score": 9.2,
            "Evidence_Grounding": "Discounts rose from 4.0% to 11.5% without sustaining incremental transaction volume.",
            "Action_Steps": "Halt broad 50% Tuesday app blasts; restrict promotions to targeted personalized offers for lapsed rewards members.",
            "Risk_Tradeoff": "Risk of minor 1-2% short-term footfall softening; offset by immediate gross price realization.",
            "Human_Review_Required": True
        },
        {
            "Action_ID": "ACT-102",
            "Initiative": "Siren Craft Station Overtime Optimization & Peak Queue Pacing",
            "Category": "Store Labor Operations",
            "Owner": "SVP Retail Operations",
            "Est_Quarterly_Impact_USD": round(ot_val, 2),
            "Controllability": "High",
            "Implementation_Speed": "Near-term (4-8 Weeks)",
            "Feasibility_Score": 8.8,
            "Evidence_Grounding": "Overtime climbed from 3.5% to 12.5% of hours, generating massive 1.5x wage cost drag.",
            "Action_Steps": "Re-balance cold drink barista staffing, stage pre-batched cold foam canisters, and deploy dynamic MOP queue throttles during morning peaks.",
            "Risk_Tradeoff": "Requires store manager scheduling discipline without cutting core bar staffing below safety standards.",
            "Human_Review_Required": True
        },
        {
            "Action_ID": "ACT-103",
            "Initiative": "Cold Bar Perishables Batching & Automated Dairy Dispensing",
            "Category": "Store Operations & Waste",
            "Owner": "VP Store Operations & Supply Chain",
            "Est_Quarterly_Impact_USD": round(waste_val, 2),
            "Controllability": "Medium",
            "Implementation_Speed": "Near-term (6-12 Weeks)",
            "Feasibility_Score": 8.0,
            "Evidence_Grounding": "Food and dairy spoilage surged 45% due to 5+ milk varieties and short-life cold foam bases.",
            "Action_Steps": "Standardize smaller cold foam recipe carafes; install refrigerated auto-milk metering taps at high-volume drive-thrus.",
            "Risk_Tradeoff": "Modest upfront equipment calibration; immediate reduction in daily dairy and syrup dump volumes.",
            "Human_Review_Required": False
        },
        {
            "Action_ID": "ACT-104",
            "Initiative": "Selective Pricing Lift on Complex Cold Drink Modifiers",
            "Category": "Commercial & Pricing",
            "Owner": "VP Global Pricing & Revenue Management",
            "Est_Quarterly_Impact_USD": round(price_val, 2),
            "Controllability": "High",
            "Implementation_Speed": "Immediate (2-3 Weeks)",
            "Feasibility_Score": 8.9,
            "Evidence_Grounding": "Cold drinks with 3+ modifiers have +40% longer barista prep time but uniform modifier add-on pricing.",
            "Action_Steps": "Implement +$0.25 to +$0.35 charge on custom cold foam and specialized seasonal syrup pumps.",
            "Risk_Tradeoff": "Highly price-inelastic customer segment with minimal order attrition.",
            "Human_Review_Required": True
        },
        {
            "Action_ID": "ACT-105",
            "Initiative": "3P Aggregator Menu Markup & In-App Delivery Incentive",
            "Category": "Channel & Digital Strategy",
            "Owner": "VP Digital Channels & Partnerships",
            "Est_Quarterly_Impact_USD": round(deliv_val, 2),
            "Controllability": "Medium",
            "Implementation_Speed": "Medium-term (8-16 Weeks)",
            "Feasibility_Score": 7.5,
            "Evidence_Grounding": "Delivery channels suffer an 18-21% commission haircut and 4x higher disposable packaging costs.",
            "Action_Steps": "Institute 10% aggregator menu parity surcharge; incentivize app users to choose curbside/MOP pickup over delivery.",
            "Risk_Tradeoff": "Delivery transaction growth may decelerate; protects margin integrity.",
            "Human_Review_Required": True
        }
    ]

    df_actions = pd.DataFrame(actions)
    df_actions = df_actions.sort_values("Est_Quarterly_Impact_USD", ascending=False).reset_index(drop=True)
    return df_actions
