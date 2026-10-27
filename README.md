# ☕ Starbucks Profitability Decline Investigation
**Business Area:** Business Analytics / Financial & Operational FP&A  
**Company Prototype:** Starbucks (Illustrative prototype; synthetic data only)  
**Objective:** Explain a synthetic three-quarter profit decline by reconciling financial data and tracing cross-functional operational drivers.

---

> ⚠️ **SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA**  
> All financial metrics, store performance figures, product costs, and labor records in this application are fictional and programmatically generated for illustrative business analytics prototyping. This project does not scrape, access, or replicate proprietary Starbucks systems or real-world internal records.

---

## 🌟 Executive Summary

Between **Q4-2023** (healthy baseline) and **Q3-2024** (trough), store-level **Operating Profit (EBIT) plummeted 50.4%** (compressing margins by over **1,550 basis points**), despite transaction volumes remaining remarkably resilient (down only **1.8%**).

Through a rigorous mathematical **Profit Waterfall Bridge**, this investigation uncovers the cross-functional root causes:
1. **Promotional Discount Cannibalization (-$1.87M):** Aggressive marketing promotions ("50% Off Cold Drinks Tuesdays", "BOGO Afternoon Treats") eroded realized net prices.
2. **Third-Party Delivery Fee Drag (-$501K):** Channel shift toward DoorDash and UberEats at 18–21% commission rates plus specialty tamper-evident packaging.
3. **Barista Overtime Surge (-$267K):** Overtime climbed from 3.8% to 13.9% of hours worked due to complex cold beverage preparation bottlenecks, incurring 1.5x wage penalties.
4. **Perishable Waste & Cold Spoilage (-$131K):** Proliferation of 5+ non-dairy milk varieties and cold foam bases drove a 45% surge in store discard costs.
5. **Direct Commodity Cost Inflation (-$351K):** Spot arabica and dairy price increases.

---

## 🏗️ Repository Architecture (Root-Level Structure)

All application files, datasets, and configuration are intentionally located directly in the root directory without nested subfolders, ensuring zero path errors when deploying locally on Windows or publishing to **Streamlit Community Cloud** and **GitHub**:

| File | Purpose |
| :--- | :--- |
| `app.py` | Full-stack interactive Streamlit web dashboard featuring a dark navy interface with restrained purple accents, KPI cards, Plotly charts, and 8 analytical modules. |
| `data_generator.py` | Parametric synthetic data engine generating 6,860+ store-quarter-product-channel records with strict accounting identities (`Net Revenue = Gross - Discounts`, `EBIT = Net Revenue - Total Costs`). |
| `profit_bridge.py` | Mathematical variance decomposition engine isolating Price, Volume, Mix, Discounts, Overtime, Waste, Delivery, and Overhead variances with **$0.00 reconciliation discrepancy**. |
| `scenarios.py` | Turnaround recovery simulator, confidence interval estimator (95% CI), and prioritized executive Action Register. |
| `synthetic_starbucks_data.csv` | Ready-to-load pre-generated synthetic dataset. |
| `requirements.txt` | Core package dependencies (`streamlit`, `pandas`, `numpy`, `plotly`, `scikit-learn`, `statsmodels`). |
| `README.md` | Complete setup instructions, technical reference, and methodology explanation. |

---

## 💻 Quick Start & Windows Installation Guide

### Prerequisites
- Python 3.10 to 3.13 installed on Windows.
- PowerShell or Windows Command Prompt.

### 1. Open Terminal and Navigate to Directory
```powershell
cd C:\Users\DELL\.gemini\antigravity\scratch\starbucks_profitability_investigation
```

### 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# (Alternative for Command Prompt cmd.exe)
# .\venv\Scripts\activate.bat
```
*(If PowerShell blocks script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Launch the Interactive Web Application
```powershell
streamlit run app.py
```
The browser will automatically launch at `http://localhost:8501`.

---

## 📐 Mathematical Methodology: The Reconciled Profit Bridge

The core algorithm performs a variance decomposition between any chosen Baseline Quarter ($T_0$) and Comparison Quarter ($T_1$):

$$\Delta \text{EBIT} = \text{EBIT}_1 - \text{EBIT}_0$$

The total variance decomposes into distinct operational and commercial effects:

1. **Gross Menu Price Effect:**
   $$\Delta \text{Price} = \sum_i Q_{1,i} \times (P_{1,i}^{\text{gross}} - P_{0,i}^{\text{gross}})$$
2. **Promotional Discount Surge:**
   $$\Delta \text{Discount} = -(D_1 - D_0)$$
3. **Transaction Volume Variance:**
   $$\Delta \text{Volume} = (Q_1 - Q_0) \times \bar{m}_0$$
   *(where $\bar{m}_0$ is baseline average unit contribution margin across all menu items)*
4. **Product Mix Shift Variance:**
   $$\Delta \text{Mix} = \sum_i \left[ Q_{1,i} - (Q_1 \times s_{0,i}) \right] \times (m_{0,i} - \bar{m}_0)$$
5. **Ingredient Cost Inflation:**
   $$\Delta \text{COGS} = -\sum_i Q_{1,i} \times (c_{ing,1,i} - c_{ing,0,i})$$
6. **Regular Labor Rate & Scheduling Effect:**
   $$\Delta \text{Regular Labor} = -(\text{RegLaborCost}_1 - \text{RegLaborCost}_0)$$
7. **Barista Overtime Surge Penalty:**
   $$\Delta \text{Overtime} = -(\text{OTCost}_1 - \text{OTCost}_0) \quad (\text{penalizing 1.5}\times \text{ wage rates})$$
8. **Food & Cold Bar Waste / Spoilage:**
   $$\Delta \text{Waste} = -(\text{WasteCost}_1 - \text{WasteCost}_0)$$
9. **3P Delivery Commissions & Packaging:**
   $$\Delta \text{Delivery} = -(\text{DeliveryFees}_1 + \text{PackagingCost}_1 - (\text{DeliveryFees}_0 + \text{PackagingCost}_0))$$
10. **Store Rent, Marketing & Overhead:**
    $$\Delta \text{Fixed Overhead} = -(\text{FixedCost}_1 - \text{FixedCost}_0)$$

### Exact Accounting Closure
$$\Delta \text{EBIT}_{\text{observed}} \equiv \sum \text{Bridge Variance Drivers} \quad (\text{Discrepancy} = \$0.00)$$

---

## 💡 Manager Exploration Questions Built into the App

1. **"Why did operating margin collapse 1,550 bps even though volume only drifted 1.8%?"**
   - Explains the "top-line illusion": discounts masked underlying transaction profitability while preparation complexity surged.
2. **"Which store formats and channels are driving over 70% of margin leakage?"**
   - Identifies Drive-Thru Suburban stores as the primary overtime sink (46% of total company profit leakage) and 3P Delivery as having direct margins of only 13.4% vs 35.8% for In-Store POS.
3. **"What is the optimal recovery tradeoff: Cutting barista hours vs. rationalizing promo discounts & waste?"**
   - Demonstrates that slashing core barista hours damages speed-of-service and causes customer churn, whereas rationalizing blanket BOGO discounts and deploying cold foam prep dispensers recovers +$1.33M quarterly with zero brand damage.

---

## 🚀 Recovery Scenario Simulator & Action Matrix

The application allows users to manipulate turnaround levers in real-time:
- **Overtime Reduction Target:** (Default: -45% via digital queue throttling & cold station prep staging).
- **Discount Rationalization:** (Default: -350 bps gross revenue via shift from blanket BOGO to personalized loyalty).
- **Cold Bar Waste Optimization:** (Default: -35% via automated milk dispensers and recipe standardization).
- **3P Delivery Fee Recoup:** (Default: +20% via menu markup parity and in-app pickup incentives).
- **Selective Modifier Pricing:** (Default: +2.0% on 3+ modifier cold foam additions).

**Projected Recovery:** Recovers **+$1.33M in quarterly EBIT** (+673 bps margin expansion), bringing operating margin back from 18.2% to 24.9%.

---

## 🔒 Safety, Model Limitations & Ethical Disclosures

- **Synthetic Prototype Only:** Not real Starbucks corporate data. Parametric distributions are calibrated for educational and prototype demonstration.
- **Human Review Safeguard:** High-impact operational changes (e.g. barista shift patterns, modifier pricing) require human cross-functional review (Operations, Legal, Finance) before field rollout.
- **No Autonomous Equipment Control:** The dashboard provides decision support analytics and does not interface with physical espresso machinery or point-of-sale hardware.
