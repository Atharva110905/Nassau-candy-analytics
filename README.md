# 🍬 Nassau Candy Analytics

> Exploratory Data Analysis, Profitability Dashboard & Executive Reporting for Nassau Candy Distributor (2024–2025)

---

## 📌 Project Overview

This project analyzes **10,194 orders** from Nassau Candy Distributor across a 24-month period (January 2024 – December 2025). It delivers end-to-end business intelligence across three deliverables: a research paper, an interactive Streamlit dashboard, and a government-ready executive summary.

**Business context:** Nassau Candy is a specialty confectionery wholesaler distributing 15 product SKUs across 3 divisions (Chocolate, Sugar, Other) and 4 US regions (Pacific, Atlantic, Interior, Gulf).

---

## 📁 Repository Structure

```
nassau-candy-analytics/
│
├── streamlit_dashboard.py        # Interactive Streamlit analytics dashboard
├── Nassau_Candy_Distributor.csv  # Source dataset (10,194 orders, 18 columns)
├── Nassau_Candy_Research_Paper.docx    # Full EDA research paper with insights & recommendations
├── Nassau_Candy_Executive_Summary.docx # Concise summary for government stakeholders
└── README.md
```

---

## 🚀 Running the Dashboard

### Prerequisites
```bash
pip install streamlit pandas plotly numpy
```

### Launch
```bash
streamlit run streamlit_dashboard.py
```

> Make sure `Nassau_Candy_Distributor.csv` is in the **same folder** as `streamlit_dashboard.py`.

### Dashboard Features
| Tab | Contents |
|-----|----------|
| 📦 Product Profitability | Gross margin %, profit per unit, full product breakdown |
| 🏭 Division Performance | Revenue vs profit by division, monthly trends, regional view |
| 📊 Pareto / Concentration | Revenue concentration chart, bubble chart, profit mix pie |
| ⚠️ Margin Risk Flags | Risk-flagged products, cost vs sales scatter, threshold line |

**Sidebar filters:** Date range, Division, Region, Ship Mode, Margin risk threshold, Product search

---

## 📊 Dataset Description

| Column | Description |
|--------|-------------|
| Row ID | Unique row identifier |
| Order ID | Order reference number |
| Order Date | Date of order (DD-MM-YYYY) |
| Ship Date | Date of shipment |
| Ship Mode | Shipping method |
| Customer ID | Unique customer identifier |
| Division | Product division (Chocolate / Sugar / Other) |
| Region | US geographic region |
| Product Name | Product SKU name |
| Sales | Gross revenue per order line ($) |
| Units | Units sold |
| Gross Profit | Profit after cost of goods ($) |
| Cost | Cost of goods sold ($) |

---

## 🔑 Key Findings

### Financial Highlights
| Metric | Value |
|--------|-------|
| Total Revenue | $141,783.63 |
| Total Gross Profit | $93,442.80 |
| Overall Gross Margin | **65.9%** |
| Total Units Sold | 38,654 |
| Total Orders | 10,194 |

### Top Insights

- 🍫 **Chocolate dominates** — 92.9% of revenue and 95.1% of gross profit come from the Chocolate division
- 📈 **490% revenue growth** from January 2024 ($2,094) to December 2025 ($12,338) with no margin compression
- 🏆 **Top 5 SKUs = ~93% of revenue** — all Wonka Bar variants (classic 80/20 concentration)
- 🚨 **Kazookles critical risk** — only 7.7% gross margin on $1,206 revenue; near-zero profit contribution
- 🌍 **Regional margins are uniform** — all 4 regions within 65.5–66.4%, confirming product mix (not region) drives margin differences
- 💎 **Hidden gems** — Everlasting Gobstopper (80% margin) and Hair Toffee (77.8%) are highly efficient but under-scaled

---

## 📋 Strategic Recommendations

| Priority | Action | Expected Outcome |
|----------|--------|-----------------|
| 🔴 Critical | Discontinue or reprice Kazookles | Eliminate 7.7% margin drag |
| 🟠 High | Scale Everlasting Gobstopper & Hair Toffee | +$5K–10K high-margin profit |
| 🟠 High | Diversify beyond Chocolate division | Reduce concentration risk |
| 🟡 Medium | Renegotiate costs for Fun Dip, Nerds, SweeTARTS | Push margins above 50% |
| 🟡 Medium | Gulf region customer acquisition | Close revenue gap vs. Pacific |
| 🟢 Low | Align inventory with Q4 seasonal peaks | Avoid Nov–Dec stockouts |

---

## 📄 Documents

| File | Description |
|------|-------------|
| `Nassau_Candy_Research_Paper.docx` | 10-section full EDA report with methodology, product/division/regional analysis, insights and recommendations |
| `Nassau_Candy_Executive_Summary.docx` | Concise 1-page brief for government and regulatory stakeholders; includes risk table and compliance note |

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly)

---

## 👤 Author

Project completed as part of a business analytics assignment covering EDA, live dashboarding, and executive communication.

---

*Data Period: 2024–2025 · 10,194 Orders · 15 Products · 3 Divisions · 4 Regions*
