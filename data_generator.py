"""
data_generator.py - Synthetic Data Generation for Starbucks Profitability Decline Investigation
DISCLAIMER: SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA. FOR ILLUSTRATIVE BUSINESS ANALYTICS ONLY.
"""

import numpy as np
import pandas as pd

# Constants for synthetic universe
QUARTERS = ["Q4-2023", "Q1-2024", "Q2-2024", "Q3-2024"]
REGIONS = ["Pacific Northwest", "Northeast", "Midwest", "South", "West Coast"]
STORE_FORMATS = ["Drive-Thru Suburban", "Urban High-Density", "Traditional Walk-In", "Kiosk / Travel Hub"]
PRODUCT_CATEGORIES = [
    "Cold Espresso & Refreshers",
    "Hot Espresso & Brewed",
    "Frappuccino & Blended",
    "Bakery & Warm Breakfast",
    "Packaged Coffee & Merch"
]
CHANNELS = ["In-Store POS", "Drive-Thru Window", "Mobile Order & Pay (MOP)", "3rd-Party Delivery"]

def generate_synthetic_dataset(seed: int = 42, num_stores: int = 120) -> pd.DataFrame:
    """
    Generates an internally consistent, synthetic store-quarter-product-channel level dataset
    that models a realistic 3-quarter profitability decline (Q4-2023 base -> Q1-2024 -> Q2-2024 -> Q3-2024).
    
    All relationships are mathematically consistent:
    - Net Revenue = Gross Revenue - Discounts
    - Total Cost = Ingredient COGS + Regular Labor + Overtime Labor + Waste/Spoilage + 3P Delivery Fees + Store Rent & Utilities + Local Marketing + Allocated Overhead
    - Operating Profit (EBIT) = Net Revenue - Total Cost
    - Operating Margin % = Operating Profit / Net Revenue * 100
    """
    rng = np.random.RandomState(seed)

    # Store master setup
    store_ids = [f"STR-{1000 + i}" for i in range(num_stores)]
    store_region_map = {sid: rng.choice(REGIONS) for sid in store_ids}
    store_format_map = {sid: rng.choice(STORE_FORMATS, p=[0.40, 0.30, 0.20, 0.10]) for sid in store_ids}
    
    # Store size baseline capacity multiplier
    format_volume_mult = {
        "Drive-Thru Suburban": 1.35,
        "Urban High-Density": 1.20,
        "Traditional Walk-In": 0.90,
        "Kiosk / Travel Hub": 0.65
    }

    # Product baselines: (base_price, base_ingredient_cogs, base_prep_time_sec)
    product_specs = {
        "Cold Espresso & Refreshers": {"price": 6.45, "cogs": 1.25, "prep_time": 68, "waste_rate": 0.052},
        "Hot Espresso & Brewed": {"price": 4.95, "cogs": 0.85, "prep_time": 38, "waste_rate": 0.025},
        "Frappuccino & Blended": {"price": 6.85, "cogs": 1.45, "prep_time": 75, "waste_rate": 0.058},
        "Bakery & Warm Breakfast": {"price": 4.80, "cogs": 1.60, "prep_time": 42, "waste_rate": 0.075},
        "Packaged Coffee & Merch": {"price": 14.50, "cogs": 6.20, "prep_time": 10, "waste_rate": 0.010}
    }

    # Quarterly macro & managerial intervention factors to create the 3-quarter profit decline
    quarter_dynamics = {
        "Q4-2023": {  # Baseline healthy quarter
            "vol_drift": 1.00,
            "price_drift": 1.00,
            "discount_rate": 0.040,      # 4% baseline promo
            "mix_cold_shift": 0.40,      # 40% cold
            "cogs_inflation": 1.00,      # base commodities
            "base_hourly_wage": 16.50,
            "overtime_ratio": 0.035,     # 3.5% OT hours
            "waste_multiplier": 1.00,
            "delivery_share": 0.08,      # 8% delivery
            "delivery_fee_rate": 0.18,   # 18% commission
            "rent_overhead_drift": 1.00
        },
        "Q1-2024": {  # Decline step 1: Mix shift to cold + slight commodity rise + early promo push
            "vol_drift": 0.995,
            "price_drift": 1.005,
            "discount_rate": 0.065,      # discounts jump to 6.5% (BOGO days)
            "mix_cold_shift": 0.45,      # cold drink share rises
            "cogs_inflation": 1.035,     # dairy & arabica spot inflation (+3.5%)
            "base_hourly_wage": 16.90,   # scheduled wage step (+2.4%)
            "overtime_ratio": 0.065,     # OT creeps to 6.5% due to drink complexity & peak line
            "waste_multiplier": 1.15,    # waste increases with cold foam / milk varieties
            "delivery_share": 0.11,      # delivery grows to 11%
            "delivery_fee_rate": 0.19,   # higher delivery fees / dynamic surcharges
            "rent_overhead_drift": 1.01
        },
        "Q2-2024": {  # Decline step 2: Escalating promos + severe overtime spike + food waste
            "vol_drift": 0.988,
            "price_drift": 1.010,
            "discount_rate": 0.095,      # discount rate surges to 9.5% ("50% off Tuesdays")
            "mix_cold_shift": 0.50,      # 50% cold drinks
            "cogs_inflation": 1.060,     # cogs +6.0%
            "base_hourly_wage": 17.20,
            "overtime_ratio": 0.098,     # OT spikes to 9.8%
            "waste_multiplier": 1.30,    # higher prep discards
            "delivery_share": 0.14,      # 14% delivery
            "delivery_fee_rate": 0.20,
            "rent_overhead_drift": 1.025
        },
        "Q3-2024": {  # Decline step 3: Severe margin contraction (trough quarter)
            "vol_drift": 0.982,
            "price_drift": 1.015,
            "discount_rate": 0.115,      # promo discounts hit 11.5%
            "mix_cold_shift": 0.54,      # 54% cold drink share
            "cogs_inflation": 1.085,     # cogs +8.5%
            "base_hourly_wage": 17.50,
            "overtime_ratio": 0.125,     # OT reaches 12.5% of total hours (1.5x pay rate)
            "waste_multiplier": 1.45,    # 45% waste surge
            "delivery_share": 0.17,      # 17% delivery
            "delivery_fee_rate": 0.21,
            "rent_overhead_drift": 1.04
        }
    }

    records = []

    for sid in store_ids:
        region = store_region_map[sid]
        fmt = store_format_map[sid]
        fmt_mult = format_volume_mult[fmt]
        
        # Base store fixed costs per quarter
        base_rent = rng.uniform(22000, 36000) * fmt_mult
        base_mktg = rng.uniform(4000, 7500)
        base_overhead = rng.uniform(8000, 14000) * (1.1 if fmt == "Urban High-Density" else 1.0)

        # Base quarterly transactions per store
        store_base_txns = rng.uniform(22000, 31000) * fmt_mult

        for q_idx, q_name in enumerate(QUARTERS):
            dyn = quarter_dynamics[q_name]
            
            # Quarter volume with store-level noise
            q_txns = store_base_txns * dyn["vol_drift"] * rng.uniform(0.97, 1.03)

            # Fixed store costs for quarter
            q_rent = base_rent * dyn["rent_overhead_drift"] * rng.uniform(0.99, 1.01)
            q_mktg = base_mktg * (1.0 + 0.08 * q_idx) * rng.uniform(0.97, 1.03) # promo ad spend increased
            q_overhead = base_overhead * dyn["rent_overhead_drift"]

            # Channel distribution for this store-quarter
            deliv_p = min(0.35, dyn["delivery_share"] * (1.3 if fmt == "Urban High-Density" else (1.1 if fmt == "Drive-Thru Suburban" else 0.7)))
            mop_p = 0.32 + 0.03 * q_idx if fmt in ["Urban High-Density", "Drive-Thru Suburban"] else 0.22
            dt_p = 0.42 if fmt == "Drive-Thru Suburban" else 0.0
            
            # Remaining goes to In-Store POS
            instore_p = max(0.10, 1.0 - (deliv_p + mop_p + dt_p))
            # Renormalize channels
            channel_probs = np.array([instore_p, dt_p, mop_p, deliv_p])
            channel_probs = channel_probs / channel_probs.sum()

            # Product mix shares for this quarter
            cold_p = dyn["mix_cold_shift"]
            hot_p = max(0.18, 0.32 - 0.04 * q_idx)
            frap_p = 0.12
            food_p = 0.18
            merch_p = max(0.02, 1.0 - (cold_p + hot_p + frap_p + food_p))
            prod_probs = np.array([cold_p, hot_p, frap_p, food_p, merch_p])
            prod_probs = prod_probs / prod_probs.sum()

            # Allocate volume across products and channels
            for p_idx, prod_cat in enumerate(PRODUCT_CATEGORIES):
                prod_spec = product_specs[prod_cat]
                cat_units = q_txns * prod_probs[p_idx] * rng.uniform(0.98, 1.02)
                
                # Channel breakdown
                for c_idx, ch_name in enumerate(CHANNELS):
                    ch_share = channel_probs[c_idx]
                    if ch_share <= 0.001:
                        continue
                    
                    units = int(cat_units * ch_share)
                    if units <= 0:
                        continue

                    # Gross list price with modest menu price adjustments
                    unit_gross_price = prod_spec["price"] * dyn["price_drift"] * rng.uniform(0.99, 1.01)
                    gross_revenue = units * unit_gross_price

                    # Promotional discount depth (escalated in Q1-Q3 2024)
                    # Mobile and Delivery channels see higher targeted app discounting
                    ch_disc_multiplier = 1.25 if ch_name in ["Mobile Order & Pay (MOP)", "3rd-Party Delivery"] else 0.85
                    cat_disc_multiplier = 1.30 if prod_cat in ["Cold Espresso & Refreshers", "Frappuccino & Blended"] else 0.90
                    eff_discount_rate = min(0.25, dyn["discount_rate"] * ch_disc_multiplier * cat_disc_multiplier * rng.uniform(0.92, 1.08))
                    discounts = gross_revenue * eff_discount_rate
                    net_revenue = gross_revenue - discounts

                    # Ingredient COGS
                    unit_ingredient_cogs = prod_spec["cogs"] * dyn["cogs_inflation"] * rng.uniform(0.98, 1.02)
                    ingredient_cost = units * unit_ingredient_cogs

                    # Prep labor requirement in hours
                    prep_sec_per_unit = prod_spec["prep_time"] * (1.10 if ch_name == "Mobile Order & Pay (MOP)" else 1.0) # custom mods higher on MOP
                    total_prep_hours = (units * prep_sec_per_unit) / 3600.0
                    # Store baseline staffing efficiency overhead
                    staffing_overhead_hours = units * 0.015
                    total_labor_hours = total_prep_hours + staffing_overhead_hours

                    # Split regular hours vs overtime hours
                    # Drive-Thru and MOP experience heavy peak overtime during morning rushes
                    store_ot_ratio = dyn["overtime_ratio"] * (1.20 if fmt == "Drive-Thru Suburban" else 1.0) * rng.uniform(0.92, 1.10)
                    store_ot_ratio = min(0.28, store_ot_ratio)
                    
                    ot_hours = total_labor_hours * store_ot_ratio
                    reg_hours = total_labor_hours - ot_hours

                    hourly_rate = dyn["base_hourly_wage"] * (1.08 if region in ["West Coast", "Northeast"] else 1.0)
                    reg_labor_cost = reg_hours * hourly_rate
                    ot_labor_cost = ot_hours * (hourly_rate * 1.50) # 1.5x overtime wage
                    total_labor_cost = reg_labor_cost + ot_labor_cost

                    # Waste & Spoilage (perishables, dairy milk options discard, cold foam trim)
                    cat_waste_rate = prod_spec["waste_rate"] * dyn["waste_multiplier"] * rng.uniform(0.93, 1.07)
                    waste_cost = ingredient_cost * cat_waste_rate

                    # 3rd-party delivery commission fees & packaging
                    if ch_name == "3rd-Party Delivery":
                        delivery_fees = gross_revenue * dyn["delivery_fee_rate"] * rng.uniform(0.97, 1.03)
                        packaging_fees = units * 0.42 # tamper-evident cup holders, cold bags, sealed labels
                    else:
                        delivery_fees = 0.0
                        packaging_fees = units * 0.08 # standard cup/sleeve

                    # Apportion fixed store occupancy & overhead by unit share
                    # (Each store has ~20 records per quarter: 5 cats x 4 channels)
                    alloc_factor = units / max(1.0, q_txns)
                    rent_cost = q_rent * alloc_factor
                    mktg_cost = q_mktg * alloc_factor
                    overhead_cost = q_overhead * alloc_factor

                    r_gross_rev = round(gross_revenue, 2)
                    r_discounts = round(discounts, 2)
                    r_net_rev = round(r_gross_rev - r_discounts, 2)

                    r_ing_cost = round(ingredient_cost, 2)
                    r_reg_labor = round(reg_labor_cost, 2)
                    r_ot_labor = round(ot_labor_cost, 2)
                    r_tot_labor = round(r_reg_labor + r_ot_labor, 2)
                    r_waste = round(waste_cost, 2)
                    r_deliv = round(delivery_fees, 2)
                    r_pack = round(packaging_fees, 2)
                    r_rent = round(rent_cost, 2)
                    r_mktg = round(mktg_cost, 2)
                    r_ovhd = round(overhead_cost, 2)

                    r_tot_cost = round(
                        r_ing_cost
                        + r_reg_labor
                        + r_ot_labor
                        + r_waste
                        + r_deliv
                        + r_pack
                        + r_rent
                        + r_mktg
                        + r_ovhd,
                        2
                    )

                    r_ebit = round(r_net_rev - r_tot_cost, 2)
                    r_margin_pct = round((r_ebit / r_net_rev * 100.0) if r_net_rev > 0 else 0.0, 2)

                    records.append({
                        "Quarter": q_name,
                        "Quarter_Index": q_idx,
                        "Store_ID": sid,
                        "Region": region,
                        "Store_Format": fmt,
                        "Product_Category": prod_cat,
                        "Channel": ch_name,
                        "Volume_Units": units,
                        "Gross_Price_Per_Unit": round(unit_gross_price, 2),
                        "Gross_Revenue": r_gross_rev,
                        "Discount_Amount": r_discounts,
                        "Discount_Rate_Pct": round(eff_discount_rate * 100.0, 2),
                        "Net_Revenue": r_net_rev,
                        "Ingredient_Cost": r_ing_cost,
                        "Regular_Labor_Hours": round(reg_hours, 2),
                        "Overtime_Labor_Hours": round(ot_hours, 2),
                        "Total_Labor_Hours": round(total_labor_hours, 2),
                        "Overtime_Pct": round(store_ot_ratio * 100.0, 2),
                        "Hourly_Wage_Rate": round(hourly_rate, 2),
                        "Regular_Labor_Cost": r_reg_labor,
                        "Overtime_Labor_Cost": r_ot_labor,
                        "Total_Labor_Cost": r_tot_labor,
                        "Waste_Cost": r_waste,
                        "Delivery_Fees": r_deliv,
                        "Packaging_Cost": r_pack,
                        "Rent_Cost": r_rent,
                        "Marketing_Cost": r_mktg,
                        "Overhead_Cost": r_ovhd,
                        "Total_Operating_Cost": r_tot_cost,
                        "Operating_Profit_EBIT": r_ebit,
                        "Operating_Margin_Pct": r_margin_pct,
                        "Data_Type": "SYNTHETIC_PROTOTYPE"
                    })

    df = pd.DataFrame(records)
    return df

def get_data_dictionary() -> pd.DataFrame:
    """Returns a structured metadata dataframe explaining every column."""
    dict_records = [
        {"Column": "Quarter", "Type": "Categorical", "Unit": "Quarter Label", "Description": "Fiscal quarter identifier (Q4-2023 baseline through Q3-2024 trough)."},
        {"Column": "Store_ID", "Type": "Identifier", "Unit": "ID String", "Description": "Synthetic retail store location identifier."},
        {"Column": "Region", "Type": "Categorical", "Unit": "Geography", "Description": "Regional operating division (Pacific Northwest, West Coast, Midwest, etc.)."},
        {"Column": "Store_Format", "Type": "Categorical", "Unit": "Format Type", "Description": "Store format (Drive-Thru Suburban, Urban High-Density, Traditional Walk-In, Kiosk)."},
        {"Column": "Product_Category", "Type": "Categorical", "Unit": "Category", "Description": "Beverage and food category (Cold Espresso & Refreshers, Hot Espresso, etc.)."},
        {"Column": "Channel", "Type": "Categorical", "Unit": "Fulfillment Channel", "Description": "Order fulfillment mode (In-Store POS, Drive-Thru Window, MOP, 3P Delivery)."},
        {"Column": "Volume_Units", "Type": "Integer", "Unit": "Items / Drinks", "Description": "Quantity of beverage or food items ordered and fulfilled."},
        {"Column": "Gross_Price_Per_Unit", "Type": "Float", "Unit": "$ USD / item", "Description": "Standard menu listing price before any discounts or promotions."},
        {"Column": "Gross_Revenue", "Type": "Float", "Unit": "$ USD", "Description": "Volume_Units * Gross_Price_Per_Unit."},
        {"Column": "Discount_Amount", "Type": "Float", "Unit": "$ USD", "Description": "Promotional discounts, BOGO coupons, member loyalty rewards applied."},
        {"Column": "Discount_Rate_Pct", "Type": "Float", "Unit": "%", "Description": "Effective discount depth as a percentage of gross sales."},
        {"Column": "Net_Revenue", "Type": "Float", "Unit": "$ USD", "Description": "Gross_Revenue - Discount_Amount. Recognized top-line revenue."},
        {"Column": "Ingredient_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Direct raw material COGS (coffee beans, milk varieties, syrups, inclusions)."},
        {"Column": "Regular_Labor_Hours", "Type": "Float", "Unit": "Hours", "Description": "Frontline barista and shift supervisor standard scheduled hours."},
        {"Column": "Overtime_Labor_Hours", "Type": "Float", "Unit": "Hours", "Description": "Unplanned overtime hours incurred during peak surges and staffing crunches."},
        {"Column": "Total_Labor_Hours", "Type": "Float", "Unit": "Hours", "Description": "Regular_Labor_Hours + Overtime_Labor_Hours."},
        {"Column": "Overtime_Pct", "Type": "Float", "Unit": "%", "Description": "Overtime_Labor_Hours / Total_Labor_Hours * 100."},
        {"Column": "Hourly_Wage_Rate", "Type": "Float", "Unit": "$ / hour", "Description": "Base regular hourly wage rate (varies by regional labor market)."},
        {"Column": "Regular_Labor_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Regular_Labor_Hours * Hourly_Wage_Rate."},
        {"Column": "Overtime_Labor_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Overtime_Labor_Hours * (Hourly_Wage_Rate * 1.50)."},
        {"Column": "Total_Labor_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Regular_Labor_Cost + Overtime_Labor_Cost."},
        {"Column": "Waste_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Perishable dairy spoilage, cold foam prep discard, and expired bakery waste."},
        {"Column": "Delivery_Fees", "Type": "Float", "Unit": "$ USD", "Description": "Commission fees paid to 3rd-party delivery aggregators (18-21%)."},
        {"Column": "Packaging_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Cups, cold drink domed lids, straws, bags, and delivery tamper tape."},
        {"Column": "Rent_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Store lease occupancy, property taxes, and CAM expenses allocated to unit."},
        {"Column": "Marketing_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Local store marketing, POP merchandising, and regional promotional campaigns."},
        {"Column": "Overhead_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Store utilities, POS software licensing, supervisory support allocation."},
        {"Column": "Total_Operating_Cost", "Type": "Float", "Unit": "$ USD", "Description": "Sum of all ingredient, labor, waste, delivery, packaging, rent, and overhead."},
        {"Column": "Operating_Profit_EBIT", "Type": "Float", "Unit": "$ USD", "Description": "Net_Revenue - Total_Operating_Cost. Core store operating income."},
        {"Column": "Operating_Margin_Pct", "Type": "Float", "Unit": "%", "Description": "Operating_Profit_EBIT / Net_Revenue * 100. Key profitability metric."},
        {"Column": "Data_Type", "Type": "String", "Unit": "Flag", "Description": "Always 'SYNTHETIC_PROTOTYPE' to ensure clear prototype provenance."}
    ]
    return pd.DataFrame(dict_records)
