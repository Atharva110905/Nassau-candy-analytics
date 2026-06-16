import json

def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source if isinstance(source, list) else [source]
    }

def md(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source if isinstance(source, list) else [source]
    }

cells = [

# ── Title
md("""# 🍬 Nassau Candy Distributor — Exploratory Data Analysis (EDA)
**Period:** January 2024 – December 2025  
**Dataset:** 10,194 Orders | 15 Products | 3 Divisions | 4 Regions  
**Author:** Nassau Candy Analytics Project  

---
### Notebook Structure
1. Environment Setup & Data Loading  
2. Data Overview & Quality Check  
3. Descriptive Statistics  
4. Sales & Profit Distribution  
5. Division-Level Analysis  
6. Product-Level Analysis  
7. Regional Analysis  
8. Time Series & Trend Analysis  
9. Correlation Analysis  
10. Pareto / Concentration Analysis  
11. Margin Risk Analysis  
12. Key Findings Summary  
---"""),

# ── 1. Setup
md("## 1. Environment Setup & Data Loading"),
code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Style
plt.rcParams.update({
    'figure.facecolor': '#0F0C29',
    'axes.facecolor':   '#1a1040',
    'axes.edgecolor':   '#444',
    'axes.labelcolor':  '#E8D5FF',
    'xtick.color':      '#C9B8E8',
    'ytick.color':      '#C9B8E8',
    'text.color':       '#E8D5FF',
    'grid.color':       '#2a2060',
    'grid.linestyle':   '--',
    'grid.alpha':       0.5,
    'font.family':      'DejaVu Sans',
    'axes.titlesize':   13,
    'axes.titleweight': 'bold',
    'axes.titlecolor':  '#FF6B9D',
})

PINK   = '#FF6B9D'
BLUE   = '#4FACFE'
YELLOW = '#FFBE0B'
GREEN  = '#7EFFA0'
PURPLE = '#C850C0'
COLORS = [PINK, BLUE, YELLOW, GREEN, PURPLE, '#FF9F43', '#A29BFE']

print("✅ Libraries loaded successfully")"""),

code("""# Load dataset
df = pd.read_csv('Nassau_Candy_Distributor.csv')

# Parse dates
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)

# Derived columns
df['Gross Margin (%)']  = (df['Gross Profit'] / df['Sales'] * 100).round(2)
df['Profit per Unit']   = (df['Gross Profit'] / df['Units']).round(3)
df['Month']             = df['Order Date'].dt.to_period('M').astype(str)
df['Quarter']           = 'Q' + df['Order Date'].dt.quarter.astype(str) + ' ' + df['Order Date'].dt.year.astype(str)
df['Year']              = df['Order Date'].dt.year

print(f"✅ Data loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
df.head()"""),

# ── 2. Overview
md("## 2. Data Overview & Quality Check"),
code("""print("=" * 50)
print("DATASET SHAPE")
print("=" * 50)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

print("\\n" + "=" * 50)
print("COLUMN DTYPES")
print("=" * 50)
print(df.dtypes)"""),

code("""print("=" * 50)
print("MISSING VALUES")
print("=" * 50)
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "✅ No missing values found!")

print("\\n" + "=" * 50)
print("DUPLICATE ROWS")
print("=" * 50)
dupes = df.duplicated().sum()
print(f"Duplicates: {dupes}" if dupes > 0 else "✅ No duplicate rows found!")"""),

code("""print("=" * 50)
print("UNIQUE VALUE COUNTS")
print("=" * 50)
for col in ['Division', 'Region', 'Ship Mode', 'Product Name']:
    print(f"\\n{col} ({df[col].nunique()} unique):")
    print(df[col].value_counts().to_string())"""),

code("""print("=" * 50)
print("DATE RANGE")
print("=" * 50)
print(f"Order Date : {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
print(f"Ship Date  : {df['Ship Date'].min().date()}  → {df['Ship Date'].max().date()}")
print(f"Period     : {df['Order Date'].dt.to_period('M').nunique()} months")"""),

# ── 3. Stats
md("## 3. Descriptive Statistics"),
code("""df[['Sales', 'Units', 'Gross Profit', 'Cost', 'Gross Margin (%)', 'Profit per Unit']].describe().round(2)"""),

code("""# KPI Summary
total_sales  = df['Sales'].sum()
total_profit = df['Gross Profit'].sum()
total_units  = df['Units'].sum()
overall_gm   = total_profit / total_sales * 100

print("=" * 45)
print("  📊  KEY PERFORMANCE INDICATORS")
print("=" * 45)
print(f"  💰  Total Revenue       : ${total_sales:>12,.2f}")
print(f"  📈  Total Gross Profit  : ${total_profit:>12,.2f}")
print(f"  🎯  Overall GM %        : {overall_gm:>13.1f}%")
print(f"  📦  Units Sold          : {total_units:>13,}")
print(f"  🧾  Total Orders        : {len(df):>13,}")
print(f"  🛍️  Unique Products     : {df['Product Name'].nunique():>13}")
print(f"  🏭  Divisions           : {df['Division'].nunique():>13}")
print(f"  🌍  Regions             : {df['Region'].nunique():>13}")
print("=" * 45)"""),

# ── 4. Distributions
md("## 4. Sales & Profit Distribution"),
code("""fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle('Distribution of Key Financial Metrics', fontsize=15, color=PINK, y=1.01)

metrics = [
    ('Sales',           'Revenue per Order ($)',    PINK),
    ('Gross Profit',    'Gross Profit per Order ($)', BLUE),
    ('Units',           'Units per Order',           YELLOW),
    ('Cost',            'Cost per Order ($)',         GREEN),
    ('Gross Margin (%)', 'Gross Margin (%)',          PURPLE),
    ('Profit per Unit', 'Profit per Unit ($)',        '#FF9F43'),
]

for ax, (col, label, color) in zip(axes.flat, metrics):
    ax.hist(df[col], bins=40, color=color, alpha=0.85, edgecolor='black', linewidth=0.3)
    ax.axvline(df[col].mean(),   color='white',  linestyle='--', linewidth=1.2, label=f'Mean: {df[col].mean():.2f}')
    ax.axvline(df[col].median(), color=YELLOW, linestyle=':',  linewidth=1.2, label=f'Median: {df[col].median():.2f}')
    ax.set_title(label)
    ax.set_xlabel(label, fontsize=9)
    ax.set_ylabel('Frequency', fontsize=9)
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('eda_distributions.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
print("\\n💡 Insight: Sales and profit distributions are right-skewed — most orders are small-to-medium, with a few high-value orders.")"""),

code("""# Boxplots by division
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Financial Metrics by Division (Boxplot)', fontsize=14, color=PINK)

div_colors = {'Chocolate': PINK, 'Other': BLUE, 'Sugar': YELLOW}

for ax, metric in zip(axes, ['Sales', 'Gross Profit', 'Gross Margin (%)']):
    data = [df[df['Division'] == d][metric].values for d in ['Chocolate', 'Other', 'Sugar']]
    bp = ax.boxplot(data, patch_artist=True, labels=['Chocolate', 'Other', 'Sugar'],
                    medianprops=dict(color='white', linewidth=2))
    for patch, color in zip(bp['boxes'], [PINK, BLUE, YELLOW]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title(metric)
    ax.set_ylabel(metric)

plt.tight_layout()
plt.savefig('eda_boxplots.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()"""),

# ── 5. Division
md("## 5. Division-Level Analysis"),
code("""div_agg = df.groupby('Division').agg(
    Revenue=('Sales', 'sum'),
    Gross_Profit=('Gross Profit', 'sum'),
    Units=('Units', 'sum'),
    Orders=('Row ID', 'count')
).reset_index()
div_agg['GM_%']         = (div_agg['Gross_Profit'] / div_agg['Revenue'] * 100).round(2)
div_agg['Rev_Share_%']  = (div_agg['Revenue'] / div_agg['Revenue'].sum() * 100).round(2)

print(div_agg.to_string(index=False))"""),

code("""fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Division Performance Overview', fontsize=14, color=PINK)

divs   = div_agg['Division'].tolist()
colors = [PINK, BLUE, YELLOW]

# Revenue bar
axes[0].bar(divs, div_agg['Revenue'], color=colors, alpha=0.85, edgecolor='black', linewidth=0.4)
for i, v in enumerate(div_agg['Revenue']):
    axes[0].text(i, v + 500, f'${v:,.0f}', ha='center', fontsize=9, color='white')
axes[0].set_title('Total Revenue by Division')
axes[0].set_ylabel('Revenue ($)')

# Gross Profit bar
axes[1].bar(divs, div_agg['Gross_Profit'], color=colors, alpha=0.85, edgecolor='black', linewidth=0.4)
for i, v in enumerate(div_agg['Gross_Profit']):
    axes[1].text(i, v + 300, f'${v:,.0f}', ha='center', fontsize=9, color='white')
axes[1].set_title('Total Gross Profit by Division')
axes[1].set_ylabel('Gross Profit ($)')

# GM% bar
axes[2].bar(divs, div_agg['GM_%'], color=colors, alpha=0.85, edgecolor='black', linewidth=0.4)
axes[2].axhline(y=50, color='red', linestyle='--', linewidth=1.2, label='50% threshold')
for i, v in enumerate(div_agg['GM_%']):
    axes[2].text(i, v + 0.5, f'{v:.1f}%', ha='center', fontsize=10, color='white', fontweight='bold')
axes[2].set_title('Gross Margin % by Division')
axes[2].set_ylabel('Gross Margin (%)')
axes[2].legend()

plt.tight_layout()
plt.savefig('eda_division.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
print("\\n💡 Insight: Chocolate contributes 92.9% of revenue. The Other division lags at 44.8% margin vs 67.4% for Chocolate.")"""),

code("""# Pie chart — revenue share
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Division Revenue & Profit Share', fontsize=14, color=PINK)

for ax, col, title in zip(axes, ['Revenue', 'Gross_Profit'], ['Revenue Share', 'Gross Profit Share']):
    wedges, texts, autotexts = ax.pie(
        div_agg[col], labels=div_agg['Division'], autopct='%1.1f%%',
        colors=colors, startangle=90,
        wedgeprops=dict(edgecolor='#0F0C29', linewidth=2),
        textprops=dict(color='white', fontsize=11)
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight('bold')
    ax.set_title(title)

plt.tight_layout()
plt.savefig('eda_division_pie.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()"""),

# ── 6. Product
md("## 6. Product-Level Analysis"),
code("""prod_agg = df.groupby(['Product Name', 'Division']).agg(
    Revenue=('Sales', 'sum'),
    Gross_Profit=('Gross Profit', 'sum'),
    Units=('Units', 'sum'),
    Orders=('Row ID', 'count')
).reset_index()
prod_agg['GM_%']            = (prod_agg['Gross_Profit'] / prod_agg['Revenue'] * 100).round(2)
prod_agg['Profit_per_Unit'] = (prod_agg['Gross_Profit'] / prod_agg['Units']).round(3)
prod_agg['Rev_Share_%']     = (prod_agg['Revenue'] / prod_agg['Revenue'].sum() * 100).round(2)

prod_agg.sort_values('Gross_Profit', ascending=False).reset_index(drop=True)"""),

code("""# Horizontal bar — Gross Margin %
prod_sorted = prod_agg.sort_values('GM_%', ascending=True)
bar_colors  = [PINK if d == 'Chocolate' else BLUE if d == 'Other' else YELLOW for d in prod_sorted['Division']]

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(prod_sorted['Product Name'], prod_sorted['GM_%'], color=bar_colors, alpha=0.85, edgecolor='black', linewidth=0.3)
ax.axvline(x=50, color='red', linestyle='--', linewidth=1.5, label='50% Risk Threshold')
ax.axvline(x=65.9, color=GREEN, linestyle=':', linewidth=1.5, label='Portfolio Average (65.9%)')
for bar, val in zip(bars, prod_sorted['GM_%']):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=9, color='white')
ax.set_xlabel('Gross Margin (%)')
ax.set_title('Gross Margin % by Product', color=PINK, fontsize=14)
ax.legend(fontsize=9)
from matplotlib.patches import Patch
legend_els = [Patch(facecolor=PINK, label='Chocolate'), Patch(facecolor=BLUE, label='Other'), Patch(facecolor=YELLOW, label='Sugar')]
ax.legend(handles=legend_els + ax.get_legend_handles_labels()[0][2:], fontsize=9)
plt.tight_layout()
plt.savefig('eda_product_gm.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
print("\\n🚨 Critical: Kazookles at 7.7% margin is far below every other product.")"""),

code("""# Top 10 by gross profit + Profit per unit
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Product Profitability Detail', fontsize=14, color=PINK)

top10 = prod_agg.sort_values('Gross_Profit', ascending=True).tail(10)
c1 = [PINK if d == 'Chocolate' else BLUE if d == 'Other' else YELLOW for d in top10['Division']]
axes[0].barh(top10['Product Name'], top10['Gross_Profit'], color=c1, alpha=0.85, edgecolor='black', linewidth=0.3)
for i, v in enumerate(top10['Gross_Profit']):
    axes[0].text(v + 100, i, f'${v:,.0f}', va='center', fontsize=9, color='white')
axes[0].set_title('Top 10 Products by Gross Profit')
axes[0].set_xlabel('Gross Profit ($)')

ppu = prod_agg.sort_values('Profit_per_Unit', ascending=False)
c2  = [PINK if d == 'Chocolate' else BLUE if d == 'Other' else YELLOW for d in ppu['Division']]
axes[1].bar(range(len(ppu)), ppu['Profit_per_Unit'], color=c2, alpha=0.85, edgecolor='black', linewidth=0.3)
axes[1].set_xticks(range(len(ppu)))
axes[1].set_xticklabels(ppu['Product Name'], rotation=35, ha='right', fontsize=8)
for i, v in enumerate(ppu['Profit_per_Unit']):
    axes[1].text(i, v + 0.1, f'${v:.2f}', ha='center', fontsize=8, color='white')
axes[1].set_title('Profit per Unit by Product')
axes[1].set_ylabel('Profit per Unit ($)')

plt.tight_layout()
plt.savefig('eda_product_detail.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()"""),

# ── 7. Regional
md("## 7. Regional Analysis"),
code("""region_agg = df.groupby('Region').agg(
    Revenue=('Sales', 'sum'),
    Gross_Profit=('Gross Profit', 'sum'),
    Units=('Units', 'sum'),
    Orders=('Row ID', 'count')
).reset_index()
region_agg['GM_%'] = (region_agg['Gross_Profit'] / region_agg['Revenue'] * 100).round(2)
print(region_agg.to_string(index=False))"""),

code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Regional Performance', fontsize=14, color=PINK)

reg_sorted = region_agg.sort_values('Revenue', ascending=False)
rc = [PINK, BLUE, YELLOW, GREEN]

x = range(len(reg_sorted))
w = 0.35
axes[0].bar([i - w/2 for i in x], reg_sorted['Revenue'],      width=w, color=PINK,  alpha=0.85, label='Revenue',      edgecolor='black', linewidth=0.3)
axes[0].bar([i + w/2 for i in x], reg_sorted['Gross_Profit'], width=w, color=BLUE,  alpha=0.85, label='Gross Profit', edgecolor='black', linewidth=0.3)
axes[0].set_xticks(x)
axes[0].set_xticklabels(reg_sorted['Region'])
axes[0].set_title('Revenue vs Gross Profit by Region')
axes[0].set_ylabel('Amount ($)')
axes[0].legend()

axes[1].bar(reg_sorted['Region'], reg_sorted['GM_%'], color=rc, alpha=0.85, edgecolor='black', linewidth=0.3)
axes[1].axhline(y=overall_gm, color=GREEN, linestyle='--', linewidth=1.5, label=f'Overall GM {overall_gm:.1f}%')
for i, v in enumerate(reg_sorted['GM_%']):
    axes[1].text(i, v + 0.2, f'{v:.1f}%', ha='center', fontsize=11, color='white', fontweight='bold')
axes[1].set_title('Gross Margin % by Region')
axes[1].set_ylabel('Gross Margin (%)')
axes[1].set_ylim(60, 70)
axes[1].legend()

plt.tight_layout()
plt.savefig('eda_regional.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
print("\\n💡 Insight: All regions within 65.5–66.4% margin — differences are product mix, not regional pricing.")"""),

# ── 8. Time Series
md("## 8. Time Series & Trend Analysis"),
code("""monthly = df.groupby('Month').agg(Revenue=('Sales','sum'), Profit=('Gross Profit','sum')).reset_index()
monthly['GM_%'] = (monthly['Profit'] / monthly['Revenue'] * 100).round(2)
monthly.head(10)"""),

code("""fig, axes = plt.subplots(3, 1, figsize=(16, 12))
fig.suptitle('Monthly Trend Analysis (2024–2025)', fontsize=15, color=PINK)

x = range(len(monthly))
xticks = list(x)
xlabels = monthly['Month'].tolist()

# Revenue
axes[0].plot(x, monthly['Revenue'], color=PINK, linewidth=2.5, marker='o', markersize=5, label='Revenue')
axes[0].fill_between(x, monthly['Revenue'], alpha=0.15, color=PINK)
axes[0].set_title('Monthly Revenue')
axes[0].set_ylabel('Revenue ($)')
axes[0].set_xticks(xticks)
axes[0].set_xticklabels(xlabels, rotation=45, ha='right', fontsize=8)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
axes[0].legend()

# Profit
axes[1].plot(x, monthly['Profit'], color=BLUE, linewidth=2.5, marker='s', markersize=5, label='Gross Profit')
axes[1].fill_between(x, monthly['Profit'], alpha=0.15, color=BLUE)
axes[1].set_title('Monthly Gross Profit')
axes[1].set_ylabel('Gross Profit ($)')
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(xlabels, rotation=45, ha='right', fontsize=8)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
axes[1].legend()

# GM%
axes[2].plot(x, monthly['GM_%'], color=YELLOW, linewidth=2.5, marker='^', markersize=5, label='GM %')
axes[2].axhline(y=65.9, color=GREEN, linestyle='--', linewidth=1.2, label='Average 65.9%')
axes[2].set_title('Monthly Gross Margin %')
axes[2].set_ylabel('Gross Margin (%)')
axes[2].set_xticks(xticks)
axes[2].set_xticklabels(xlabels, rotation=45, ha='right', fontsize=8)
axes[2].set_ylim(55, 75)
axes[2].legend()

plt.tight_layout()
plt.savefig('eda_timeseries.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
print("\\n💡 Insight: Clear Q4 peaks every year. Revenue grew ~490% from Jan 2024 to Dec 2025. Margins stayed stable throughout.")"""),

code("""# Year-over-year comparison
yearly = df.groupby('Year').agg(Revenue=('Sales','sum'), Profit=('Gross Profit','sum'), Orders=('Row ID','count')).reset_index()
yearly['GM_%'] = (yearly['Profit'] / yearly['Revenue'] * 100).round(2)
print("Year-over-Year Comparison:")
print(yearly.to_string(index=False))
rev_growth = (yearly.iloc[1]['Revenue'] - yearly.iloc[0]['Revenue']) / yearly.iloc[0]['Revenue'] * 100
print(f"\\nRevenue Growth YoY: {rev_growth:.1f}%")"""),

code("""# Quarterly heatmap — revenue
qtr = df.groupby(['Quarter'])['Sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(14, 4))
ax.bar(qtr['Quarter'], qtr['Sales'], color=PINK, alpha=0.85, edgecolor='black', linewidth=0.3)
ax.set_title('Quarterly Revenue Trend', color=PINK, fontsize=13)
ax.set_xlabel('Quarter')
ax.set_ylabel('Revenue ($)')
ax.set_xticklabels(qtr['Quarter'], rotation=30, ha='right', fontsize=9)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
plt.tight_layout()
plt.savefig('eda_quarterly.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()"""),

# ── 9. Correlation
md("## 9. Correlation Analysis"),
code("""numeric_cols = ['Sales', 'Units', 'Gross Profit', 'Cost', 'Gross Margin (%)', 'Profit per Unit']
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True

sns.heatmap(
    corr, mask=mask, annot=True, fmt='.2f', cmap='RdPu',
    linewidths=0.5, linecolor='#0F0C29',
    annot_kws={'size': 11, 'weight': 'bold'},
    cbar_kws={'shrink': 0.8},
    ax=ax
)
ax.set_title('Correlation Matrix — Financial Metrics', color=PINK, fontsize=13, pad=15)
ax.set_facecolor('#1a1040')
plt.tight_layout()
plt.savefig('eda_correlation.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
print("\\n💡 Key correlations:")
print(f"  Sales ↔ Gross Profit  : {corr.loc['Sales','Gross Profit']:.2f}  (very strong — expected)")
print(f"  Units ↔ Sales         : {corr.loc['Units','Sales']:.2f}")
print(f"  GM % ↔ Profit/Unit    : {corr.loc['Gross Margin (%)','Profit per Unit']:.2f}")"""),

code("""# Scatter: Sales vs Gross Profit colored by division
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Scatter Analysis', fontsize=14, color=PINK)

div_color_map = {'Chocolate': PINK, 'Other': BLUE, 'Sugar': YELLOW}
for div in df['Division'].unique():
    sub = df[df['Division'] == div]
    axes[0].scatter(sub['Sales'], sub['Gross Profit'], alpha=0.4, s=15,
                    color=div_color_map[div], label=div)
axes[0].set_title('Sales vs Gross Profit (by Division)')
axes[0].set_xlabel('Sales ($)')
axes[0].set_ylabel('Gross Profit ($)')
axes[0].legend()

# Units vs Profit per Unit
axes[1].scatter(df['Units'], df['Profit per Unit'], alpha=0.4, s=15, color=PURPLE)
axes[1].set_title('Units vs Profit per Unit')
axes[1].set_xlabel('Units per Order')
axes[1].set_ylabel('Profit per Unit ($)')

plt.tight_layout()
plt.savefig('eda_scatter.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()"""),

# ── 10. Pareto
md("## 10. Pareto / Concentration Analysis"),
code("""pareto = prod_agg.sort_values('Revenue', ascending=False).reset_index(drop=True)
pareto['Cumulative_Rev_%'] = (pareto['Revenue'].cumsum() / pareto['Revenue'].sum() * 100).round(2)
pareto['Cumulative_Prof_%'] = (pareto['Gross_Profit'].cumsum() / pareto['Gross_Profit'].sum() * 100).round(2)

print("Pareto Table:")
print(pareto[['Product Name', 'Division', 'Revenue', 'Rev_Share_%', 'Cumulative_Rev_%']].to_string(index=False))"""),

code("""fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()

bar_c = [PINK if d == 'Chocolate' else BLUE if d == 'Other' else YELLOW for d in pareto['Division']]
ax1.bar(pareto['Product Name'], pareto['Rev_Share_%'], color=bar_c, alpha=0.85, edgecolor='black', linewidth=0.3)
ax2.plot(pareto['Product Name'], pareto['Cumulative_Rev_%'], color='white', marker='o', linewidth=2.5, markersize=6, label='Cumulative %')
ax2.axhline(y=80, color='red', linestyle='--', linewidth=1.5, label='80% Line')

ax1.set_title('Pareto Chart — Revenue Concentration by Product', color=PINK, fontsize=13)
ax1.set_xlabel('Product')
ax1.set_ylabel('Revenue Share (%)', color=PINK)
ax2.set_ylabel('Cumulative Revenue (%)', color='white')
ax1.set_xticklabels(pareto['Product Name'], rotation=35, ha='right', fontsize=8)
ax2.set_ylim(0, 110)
ax2.legend(loc='center right')

from matplotlib.patches import Patch
legend_els = [Patch(facecolor=PINK, label='Chocolate'), Patch(facecolor=BLUE, label='Other'), Patch(facecolor=YELLOW, label='Sugar')]
ax1.legend(handles=legend_els, loc='upper right')

plt.tight_layout()
plt.savefig('eda_pareto.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()
top5_share = pareto.head(5)['Rev_Share_%'].sum()
print(f"\\n💡 Top 5 products = {top5_share:.1f}% of total revenue (all Wonka Bars)")"""),

# ── 11. Margin Risk
md("## 11. Margin Risk Analysis"),
code("""threshold = 50
risk = prod_agg[prod_agg['GM_%'] < threshold].sort_values('GM_%')

print(f"Products BELOW {threshold}% Gross Margin Threshold:")
print("=" * 65)
for _, row in risk.iterrows():
    level = "🔴 CRITICAL" if row['GM_%'] < 20 else "🟠 HIGH" if row['GM_%'] < 40 else "🟡 MEDIUM"
    print(f"  {level:15s}  {row['Product Name']:35s}  GM: {row['GM_%']:.1f}%")"""),

code("""# Risk flag chart
all_sorted = prod_agg.sort_values('GM_%', ascending=True)
risk_colors = ['#E24B4A' if v < threshold else PINK for v in all_sorted['GM_%']]

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(all_sorted['Product Name'], all_sorted['GM_%'], color=risk_colors, alpha=0.85, edgecolor='black', linewidth=0.3)
ax.axvline(x=threshold, color='red', linestyle='--', linewidth=2, label=f'Risk Threshold {threshold}%')
ax.axvline(x=65.9,      color=GREEN, linestyle=':', linewidth=1.5, label='Portfolio Average 65.9%')
for bar, val in zip(bars, all_sorted['GM_%']):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=9,
            color='white', fontweight='bold')
ax.set_xlabel('Gross Margin (%)')
ax.set_title('Margin Risk Flag — All Products', color=PINK, fontsize=13)
ax.legend()
plt.tight_layout()
plt.savefig('eda_margin_risk.png', dpi=150, bbox_inches='tight', facecolor='#0F0C29')
plt.show()"""),

# ── 12. Summary
md("""## 12. Key Findings Summary

| # | Finding | Impact |
|---|---------|--------|
| 1 | Overall gross margin of **65.9%** — strong portfolio health | ✅ Positive |
| 2 | **Chocolate division = 92.9% of revenue** — extreme concentration | ⚠️ Risk |
| 3 | Top 5 Wonka Bar SKUs account for **~93% of revenue** | ⚠️ Concentration |
| 4 | **Kazookles: 7.7% margin** — near-zero profitability | 🔴 Critical |
| 5 | Everlasting Gobstopper **(80% margin)** — untapped high-value product | ✅ Opportunity |
| 6 | All 4 regions within **65.5–66.4% margin band** — uniform execution | ✅ Positive |
| 7 | Revenue grew **490%** from Jan 2024 to Dec 2025 | ✅ Strong growth |
| 8 | Clear **Q4 seasonal peaks** (Sep, Nov, Dec) every year | 📅 Planning signal |
| 9 | Sugar division has **66.6% margin** but only **$427 revenue** | ✅ Scale opportunity |
| 10 | Gulf region has lowest revenue at **$22,247** vs Pacific **$46,301** | 📈 Expansion target |

---
### Strategic Actions
1. 🔴 **Immediately** review / discontinue Kazookles  
2. 📈 Scale Everlasting Gobstopper and Hair Toffee distribution  
3. 🌍 Invest in Gulf region customer acquisition  
4. 📦 Build Q4 inventory buffer for peak season  
5. 🏭 Diversify beyond Chocolate to reduce concentration risk  

---
*EDA completed | Nassau Candy Distributor | 2024–2025*"""),

]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"}
    },
    "cells": cells
}

with open('/mnt/user-data/outputs/Nassau_Candy_EDA.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("✅ EDA Notebook created successfully!")