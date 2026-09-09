# ============================================================
# SEASONAL AGRICULTURE PERFORMANCE ANALYSIS
# Complete VS Code Project
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import f_oneway, kruskal


# ============================================================
# 1. SETTINGS
# ============================================================

pd.set_option("display.max_columns", None)
pd.set_option(
    "display.float_format",
    lambda x: f"{x:,.2f}"
)

# Close any previously open figures
plt.close("all")

# Create graph folder
os.makedirs("graphs", exist_ok=True)

print("=" * 70)
print("SEASONAL AGRICULTURE PERFORMANCE ANALYSIS")
print("=" * 70)


# ============================================================
# 2. LOAD DATASET
# ============================================================

# YOUR ACTUAL CSV FILE NAME
file_path = r"seasonal_agriculture_performance_dataset.csv"

try:
    df = pd.read_csv(file_path)

    print("\nDataset loaded successfully!")

except FileNotFoundError:
    print("\nERROR: Dataset not found!")
    print("Make sure this CSV file is in the same folder as the Python file:")
    print(file_path)
    raise


# ============================================================
# 3. BASIC INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("1. DATASET INFORMATION")
print("=" * 70)

print("\nDataset Shape:", df.shape)

print("Number of Rows:", len(df))

print("Number of Columns:", len(df.columns))

print("\nColumn Names:")

for column in df.columns:
    print("-", column)


# ============================================================
# 4. FIRST FIVE ROWS
# ============================================================

print("\nFirst 5 Rows:")

print(df.head())


# ============================================================
# 5. DATA TYPES
# ============================================================

print("\nData Types:")

print(df.dtypes)


# ============================================================
# 6. DUPLICATE CHECK
# ============================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_count)


# ============================================================
# 7. MISSING VALUE CHECK
# ============================================================

print("\nMissing Values:")

missing_values = df.isnull().sum()

missing_values = missing_values[
    missing_values > 0
]

if len(missing_values) > 0:
    print(missing_values)
else:
    print("No missing values found.")


# ============================================================
# 8. UNIQUE VALUES
# ============================================================

print("\nUnique Values:")

important_columns = [
    "Season",
    "Crop",
    "State",
    "Irrigation_Method"
]

for column in important_columns:

    if column in df.columns:

        print(
            f"\n{column}:"
        )

        print(
            "Number of unique values:",
            df[column].nunique()
        )

        print(
            "Values:",
            df[column].dropna().unique().tolist()
        )


# ============================================================
# 9. DATA CLEANING
# ============================================================

print("\n" + "=" * 70)
print("2. DATA CLEANING")
print("=" * 70)

df_clean = df.copy()


# ------------------------------------------------------------
# Convert important numeric columns to numeric
# ------------------------------------------------------------

numeric_columns = [
    "Farm_Area_Hectares",
    "Rainfall_mm",
    "Avg_Temperature_C",
    "Humidity_pct",
    "Sunlight_Hours_Day",
    "Soil_pH",
    "Soil_Moisture_pct",
    "Nitrogen_kg_ha",
    "Phosphorus_kg_ha",
    "Potassium_kg_ha",
    "Fertilizer_kg_ha",
    "Pesticide_Litre_ha",
    "Seed_Quality_Score",
    "Yield_Tonnes_Ha",
    "Production_Tonnes",
    "Market_Price_INR_Tonne",
    "Total_Cost_INR",
    "Revenue_INR",
    "Profit_INR",
    "Water_Used_m3",
    "Water_Efficiency_t_per_1000m3",
    "Disease_Pest_Risk_pct"
]


for column in numeric_columns:

    if column in df_clean.columns:

        df_clean[column] = pd.to_numeric(
            df_clean[column],
            errors="coerce"
        )


# ------------------------------------------------------------
# Fill missing numeric values
# First use season-wise median
# ------------------------------------------------------------

columns_to_fill = [
    "Rainfall_mm",
    "Soil_Moisture_pct",
    "Yield_Tonnes_Ha"
]


for column in columns_to_fill:

    if column in df_clean.columns:

        df_clean[column] = (
            df_clean
            .groupby("Season")[column]
            .transform(
                lambda x: x.fillna(
                    x.median()
                )
            )
        )


# ------------------------------------------------------------
# Fill any remaining numeric missing values
# with overall median
# ------------------------------------------------------------

for column in numeric_columns:

    if column in df_clean.columns:

        if df_clean[column].isnull().sum() > 0:

            df_clean[column] = (
                df_clean[column]
                .fillna(
                    df_clean[column].median()
                )
            )


# ------------------------------------------------------------
# Remove duplicate rows
# ------------------------------------------------------------

before_duplicates = len(df_clean)

df_clean = df_clean.drop_duplicates()

after_duplicates = len(df_clean)

removed_duplicates = (
    before_duplicates -
    after_duplicates
)


# ------------------------------------------------------------
# Update dataframe
# ------------------------------------------------------------

df = df_clean.copy()


print(
    "\nRows before duplicate removal:",
    before_duplicates
)

print(
    "Rows after duplicate removal:",
    after_duplicates
)

print(
    "Duplicate rows removed:",
    removed_duplicates
)

print(
    "Total missing values after cleaning:",
    int(df.isnull().sum().sum())
)


# ============================================================
# 10. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("3. DESCRIPTIVE STATISTICS")
print("=" * 70)

print(
    df.describe().T
)


# ============================================================
# 11. SEASON ORDER
# ============================================================

season_order = [
    "Kharif",
    "Rabi",
    "Zaid"
]


# ============================================================
# 12. SEASON COUNTS
# ============================================================

print("\n" + "=" * 70)
print("4. SEASON DISTRIBUTION")
print("=" * 70)

season_counts = (
    df["Season"]
    .value_counts()
    .reindex(season_order)
    .fillna(0)
)

print(
    "\nNumber of records by season:"
)

print(season_counts)


# ============================================================
# FUNCTION TO SAVE GRAPH
# ============================================================

def save_graph(fig, filename):

    path = os.path.join(
        "graphs",
        filename
    )

    fig.tight_layout()

    fig.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"Graph saved: {path}"
    )

    plt.show()

    plt.close(fig)


# ============================================================
# GRAPH 1
# NUMBER OF RECORDS BY SEASON
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    season_counts.index,
    season_counts.values
)

ax.set_title(
    "Number of Records by Season"
)

ax.set_xlabel(
    "Season"
)

ax.set_ylabel(
    "Number of Farms"
)

save_graph(
    fig,
    "01_number_of_records_by_season.png"
)


# ============================================================
# 13. SEASONAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("5. SEASONAL PERFORMANCE ANALYSIS")
print("=" * 70)

season_summary = (
    df.groupby("Season")
    .agg(

        Farms=(
            "Farm_ID",
            "count"
        ),

        Avg_Yield=(
            "Yield_Tonnes_Ha",
            "mean"
        ),

        Avg_Production=(
            "Production_Tonnes",
            "mean"
        ),

        Avg_Revenue=(
            "Revenue_INR",
            "mean"
        ),

        Avg_Cost=(
            "Total_Cost_INR",
            "mean"
        ),

        Avg_Profit=(
            "Profit_INR",
            "mean"
        ),

        Avg_Water=(
            "Water_Used_m3",
            "mean"
        ),

        Avg_Water_Efficiency=(
            "Water_Efficiency_t_per_1000m3",
            "mean"
        ),

        Avg_Rainfall=(
            "Rainfall_mm",
            "mean"
        ),

        Avg_Temperature=(
            "Avg_Temperature_C",
            "mean"
        ),

        Avg_Humidity=(
            "Humidity_pct",
            "mean"
        ),

        Avg_Pest_Risk=(
            "Disease_Pest_Risk_pct",
            "mean"
        )
    )
    .reindex(season_order)
)


print(
    "\nSeasonal Performance Summary:"
)

print(
    season_summary
)


# ============================================================
# GRAPH 2
# AVERAGE YIELD BY SEASON
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    season_order,
    season_summary["Avg_Yield"].values
)

ax.set_title(
    "Average Yield Across Seasons"
)

ax.set_xlabel(
    "Season"
)

ax.set_ylabel(
    "Average Yield (Tonnes/Ha)"
)

save_graph(
    fig,
    "02_average_yield_by_season.png"
)


# ============================================================
# GRAPH 3
# AVERAGE PROFIT BY SEASON
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    season_order,
    season_summary["Avg_Profit"].values
)

ax.set_title(
    "Average Profit Across Seasons"
)

ax.set_xlabel(
    "Season"
)

ax.set_ylabel(
    "Average Profit (INR)"
)

save_graph(
    fig,
    "03_average_profit_by_season.png"
)


# ============================================================
# 14. ENVIRONMENTAL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("6. ENVIRONMENTAL ANALYSIS")
print("=" * 70)

environmental_columns = [
    "Rainfall_mm",
    "Avg_Temperature_C",
    "Humidity_pct",
    "Sunlight_Hours_Day",
    "Soil_Moisture_pct"
]

environmental = (
    df.groupby("Season")[
        environmental_columns
    ]
    .mean()
    .reindex(season_order)
)

print(
    "\nEnvironmental Conditions:"
)

print(environmental)


# ============================================================
# GRAPH 4
# RAINFALL BOX PLOT
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

rainfall_data = []

rainfall_labels = []

for season in season_order:

    values = (
        df.loc[
            df["Season"] == season,
            "Rainfall_mm"
        ]
        .dropna()
        .values
    )

    if len(values) > 0:

        rainfall_data.append(values)

        rainfall_labels.append(
            season
        )


if len(rainfall_data) > 0:

    ax.boxplot(
        rainfall_data
    )

    # Version-independent label setting
    ax.set_xticks(
        range(
            1,
            len(rainfall_labels) + 1
        )
    )

    ax.set_xticklabels(
        rainfall_labels
    )

    ax.set_title(
        "Rainfall Across Seasons"
    )

    ax.set_xlabel(
        "Season"
    )

    ax.set_ylabel(
        "Rainfall (mm)"
    )

    save_graph(
        fig,
        "04_rainfall_by_season.png"
    )

else:

    print(
        "No rainfall data available."
    )

    plt.close(fig)


# ============================================================
# GRAPH 5
# TEMPERATURE BOX PLOT
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

temperature_data = []

temperature_labels = []

for season in season_order:

    values = (
        df.loc[
            df["Season"] == season,
            "Avg_Temperature_C"
        ]
        .dropna()
        .values
    )

    if len(values) > 0:

        temperature_data.append(values)

        temperature_labels.append(
            season
        )


if len(temperature_data) > 0:

    ax.boxplot(
        temperature_data
    )

    ax.set_xticks(
        range(
            1,
            len(temperature_labels) + 1
        )
    )

    ax.set_xticklabels(
        temperature_labels
    )

    ax.set_title(
        "Average Temperature Across Seasons"
    )

    ax.set_xlabel(
        "Season"
    )

    ax.set_ylabel(
        "Temperature (°C)"
    )

    save_graph(
        fig,
        "05_temperature_by_season.png"
    )

else:

    print(
        "No temperature data available."
    )

    plt.close(fig)


# ============================================================
# GRAPH 6
# HUMIDITY BOX PLOT
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

humidity_data = []

humidity_labels = []

for season in season_order:

    values = (
        df.loc[
            df["Season"] == season,
            "Humidity_pct"
        ]
        .dropna()
        .values
    )

    if len(values) > 0:

        humidity_data.append(values)

        humidity_labels.append(
            season
        )


if len(humidity_data) > 0:

    ax.boxplot(
        humidity_data
    )

    ax.set_xticks(
        range(
            1,
            len(humidity_labels) + 1
        )
    )

    ax.set_xticklabels(
        humidity_labels
    )

    ax.set_title(
        "Humidity Across Seasons"
    )

    ax.set_xlabel(
        "Season"
    )

    ax.set_ylabel(
        "Humidity (%)"
    )

    save_graph(
        fig,
        "06_humidity_by_season.png"
    )

else:

    print(
        "No humidity data available."
    )

    plt.close(fig)


# ============================================================
# 15. RESOURCE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("7. RESOURCE USAGE ANALYSIS")
print("=" * 70)

resource_columns = [
    "Water_Used_m3",
    "Water_Efficiency_t_per_1000m3",
    "Fertilizer_kg_ha",
    "Pesticide_Litre_ha"
]

resources = (
    df.groupby("Season")[
        resource_columns
    ]
    .mean()
    .reindex(season_order)
)

print(
    "\nResource Usage:"
)

print(resources)


# ============================================================
# GRAPH 7
# WATER USAGE
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    season_order,
    resources["Water_Used_m3"].values
)

ax.set_title(
    "Average Water Usage by Season"
)

ax.set_xlabel(
    "Season"
)

ax.set_ylabel(
    "Water Used (m³)"
)

save_graph(
    fig,
    "07_water_usage_by_season.png"
)


# ============================================================
# GRAPH 8
# WATER EFFICIENCY
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    season_order,
    resources[
        "Water_Efficiency_t_per_1000m3"
    ].values
)

ax.set_title(
    "Average Water Efficiency by Season"
)

ax.set_xlabel(
    "Season"
)

ax.set_ylabel(
    "Tonnes per 1,000 m³"
)

save_graph(
    fig,
    "08_water_efficiency_by_season.png"
)


# ============================================================
# 16. CROP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("8. CROP-WISE ANALYSIS")
print("=" * 70)

crop_season = (
    df.groupby(
        [
            "Season",
            "Crop"
        ]
    )[
        "Yield_Tonnes_Ha"
    ]
    .mean()
    .reset_index()
)

crop_pivot = (
    crop_season
    .pivot(
        index="Crop",
        columns="Season",
        values="Yield_Tonnes_Ha"
    )
    .reindex(
        columns=season_order
    )
)

print(
    "\nAverage Crop Yield by Season:"
)

print(
    crop_pivot.round(2)
)


# ============================================================
# GRAPH 9
# CROP YIELD BY SEASON
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 6)
)

crops = crop_pivot.index.tolist()

x = np.arange(
    len(crops)
)

number_of_seasons = len(
    season_order
)

width = (
    0.8 /
    number_of_seasons
)


for i, season in enumerate(
    season_order
):

    if season in crop_pivot.columns:

        values = (
            crop_pivot[season]
            .fillna(0)
            .values
        )

        positions = (
            x +
            (
                i -
                (
                    number_of_seasons - 1
                ) / 2
            ) * width
        )

        ax.bar(
            positions,
            values,
            width=width,
            label=season
        )


ax.set_title(
    "Average Crop Yield by Season"
)

ax.set_xlabel(
    "Crop"
)

ax.set_ylabel(
    "Average Yield (Tonnes/Ha)"
)

ax.set_xticks(
    x
)

ax.set_xticklabels(
    crops,
    rotation=35,
    ha="right"
)

ax.legend(
    title="Season"
)

save_graph(
    fig,
    "09_crop_yield_by_season.png"
)


# ============================================================
# 17. BEST AND WORST CROPS
# ============================================================

print(
    "\nBest Performing Crop in Each Season:"
)

best_crop = crop_season.loc[
    crop_season
    .groupby("Season")[
        "Yield_Tonnes_Ha"
    ]
    .idxmax()
    .values
]

print(
    best_crop.sort_values(
        "Season"
    )
)


print(
    "\nWorst Performing Crop in Each Season:"
)

worst_crop = crop_season.loc[
    crop_season
    .groupby("Season")[
        "Yield_Tonnes_Ha"
    ]
    .idxmin()
    .values
]

print(
    worst_crop.sort_values(
        "Season"
    )
)


# ============================================================
# 18. IRRIGATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("9. IRRIGATION ANALYSIS")
print("=" * 70)

irrigation_summary = (
    df.groupby(
        [
            "Season",
            "Irrigation_Method"
        ]
    )[
        "Yield_Tonnes_Ha"
    ]
    .mean()
    .reset_index()
)

irrigation_pivot = (
    irrigation_summary
    .pivot(
        index="Irrigation_Method",
        columns="Season",
        values="Yield_Tonnes_Ha"
    )
    .reindex(
        columns=season_order
    )
)

print(
    "\nAverage Yield by Irrigation Method:"
)

print(
    irrigation_pivot.round(2)
)


# ============================================================
# GRAPH 10
# IRRIGATION METHOD VS YIELD
# ============================================================

fig, ax = plt.subplots(
    figsize=(10, 6)
)

methods = irrigation_pivot.index.tolist()

x = np.arange(
    len(methods)
)

number_of_seasons = len(
    season_order
)

width = (
    0.8 /
    number_of_seasons
)


for i, season in enumerate(
    season_order
):

    if season in irrigation_pivot.columns:

        values = (
            irrigation_pivot[season]
            .fillna(0)
            .values
        )

        positions = (
            x +
            (
                i -
                (
                    number_of_seasons - 1
                ) / 2
            ) * width
        )

        ax.bar(
            positions,
            values,
            width=width,
            label=season
        )


ax.set_title(
    "Average Yield by Irrigation Method and Season"
)

ax.set_xlabel(
    "Irrigation Method"
)

ax.set_ylabel(
    "Average Yield (Tonnes/Ha)"
)

ax.set_xticks(
    x
)

ax.set_xticklabels(
    methods,
    rotation=0
)

ax.legend(
    title="Season"
)

save_graph(
    fig,
    "10_irrigation_method_vs_yield.png"
)


# ============================================================
# 19. FERTILIZER VS YIELD
# ============================================================

print("\n" + "=" * 70)
print("10. FERTILIZER VS YIELD")
print("=" * 70)


# ============================================================
# GRAPH 11
# FERTILIZER VS YIELD
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

for season in season_order:

    group = df[
        df["Season"] == season
    ]

    ax.scatter(
        group["Fertilizer_kg_ha"],
        group["Yield_Tonnes_Ha"],
        label=season,
        alpha=0.6
    )


ax.set_title(
    "Fertilizer Usage vs Yield"
)

ax.set_xlabel(
    "Fertilizer (kg/ha)"
)

ax.set_ylabel(
    "Yield (Tonnes/Ha)"
)

ax.legend(
    title="Season"
)

save_graph(
    fig,
    "11_fertilizer_vs_yield.png"
)


# ============================================================
# 20. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("11. CORRELATION ANALYSIS")
print("=" * 70)

corr_cols = [
    "Yield_Tonnes_Ha",
    "Water_Efficiency_t_per_1000m3",
    "Production_Tonnes",
    "Profit_INR",
    "Revenue_INR",
    "Water_Used_m3",
    "Rainfall_mm",
    "Avg_Temperature_C",
    "Humidity_pct",
    "Fertilizer_kg_ha",
    "Seed_Quality_Score",
    "Disease_Pest_Risk_pct"
]

correlation_matrix = (
    df[corr_cols]
    .corr()
)

yield_corr = (
    correlation_matrix[
        "Yield_Tonnes_Ha"
    ]
    .sort_values(
        ascending=False
    )
)

print(
    "\nCorrelation with Yield:"
)

print(
    yield_corr
)


# ============================================================
# GRAPH 12
# CORRELATION MATRIX
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 8)
)

matrix_values = (
    correlation_matrix.values
)

image = ax.imshow(
    matrix_values,
    aspect="auto"
)

fig.colorbar(
    image,
    ax=ax
)

ax.set_xticks(
    range(
        len(corr_cols)
    )
)

ax.set_xticklabels(
    corr_cols,
    rotation=90
)

ax.set_yticks(
    range(
        len(corr_cols)
    )
)

ax.set_yticklabels(
    corr_cols
)


for i in range(
    len(corr_cols)
):

    for j in range(
        len(corr_cols)
    ):

        ax.text(
            j,
            i,
            f"{matrix_values[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=7
        )


ax.set_title(
    "Correlation Matrix of Key Variables"
)

save_graph(
    fig,
    "12_correlation_matrix.png"
)


# ============================================================
# 21. STATISTICAL TESTING
# ============================================================

print("\n" + "=" * 70)
print("12. STATISTICAL TESTING")
print("=" * 70)

yield_groups = []

profit_groups = []

for season in season_order:

    yield_values = (
        df.loc[
            df["Season"] == season,
            "Yield_Tonnes_Ha"
        ]
        .dropna()
        .values
    )

    profit_values = (
        df.loc[
            df["Season"] == season,
            "Profit_INR"
        ]
        .dropna()
        .values
    )

    if len(yield_values) > 0:
        yield_groups.append(
            yield_values
        )

    if len(profit_values) > 0:
        profit_groups.append(
            profit_values
        )


# ------------------------------------------------------------
# ANOVA
# ------------------------------------------------------------

if len(yield_groups) >= 2:

    yield_anova = f_oneway(
        *yield_groups
    )

    print(
        "\nOne-Way ANOVA for Yield:"
    )

    print(
        f"F-statistic = "
        f"{yield_anova.statistic:.3f}"
    )

    print(
        f"p-value = "
        f"{yield_anova.pvalue:.6f}"
    )

else:

    yield_anova = None

    print(
        "\nANOVA could not be performed."
    )


# ------------------------------------------------------------
# KRUSKAL-WALLIS
# ------------------------------------------------------------

if len(profit_groups) >= 2:

    profit_kruskal = kruskal(
        *profit_groups
    )

    print(
        "\nKruskal-Wallis Test for Profit:"
    )

    print(
        f"H-statistic = "
        f"{profit_kruskal.statistic:.3f}"
    )

    print(
        f"p-value = "
        f"{profit_kruskal.pvalue:.6e}"
    )

else:

    profit_kruskal = None

    print(
        "\nKruskal-Wallis test could not be performed."
    )


# ============================================================
# 22. STATISTICAL INTERPRETATION
# ============================================================

print(
    "\nStatistical Interpretation:"
)

if yield_anova is not None:

    if yield_anova.pvalue < 0.05:

        print(
            "Yield differences between seasons "
            "are statistically significant."
        )

    else:

        print(
            "Yield differences between seasons "
            "are not statistically significant."
        )


if profit_kruskal is not None:

    if profit_kruskal.pvalue < 0.05:

        print(
            "Profit differences between seasons "
            "are statistically significant."
        )

    else:

        print(
            "Profit differences between seasons "
            "are not statistically significant."
        )


# ============================================================
# 23. STATE-WISE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("13. STATE-WISE ANALYSIS")
print("=" * 70)

state_summary = (
    df.groupby("State")
    .agg(

        Farms=(
            "Farm_ID",
            "count"
        ),

        Avg_Yield=(
            "Yield_Tonnes_Ha",
            "mean"
        ),

        Avg_Profit=(
            "Profit_INR",
            "mean"
        )
    )
    .sort_values(
        "Avg_Yield",
        ascending=False
    )
)

print(
    "\nState-wise Performance:"
)

print(
    state_summary
)


# ============================================================
# GRAPH 13
# TOP 8 STATES BY YIELD
# ============================================================

top_states = (
    state_summary
    .head(8)
    .sort_values(
        "Avg_Yield"
    )
)

fig, ax = plt.subplots(
    figsize=(10, 6)
)

ax.barh(
    top_states.index,
    top_states["Avg_Yield"].values
)

ax.set_title(
    "Average Yield by Top States"
)

ax.set_xlabel(
    "Average Yield (Tonnes/Ha)"
)

ax.set_ylabel(
    "State"
)

save_graph(
    fig,
    "13_top_states_by_yield.png"
)


# ============================================================
# 24. PROFITABILITY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("14. PROFITABILITY ANALYSIS")
print("=" * 70)

df["Profitable"] = (
    df["Profit_INR"] > 0
)

profit_status = (
    df.groupby("Season")[
        "Profitable"
    ]
    .mean()
    .reindex(season_order)
    .fillna(0)
    * 100
)

print(
    "\nPercentage of Profitable Records:"
)

print(
    profit_status.round(2)
)


# ============================================================
# GRAPH 14
# PROFITABLE FARMS
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    season_order,
    profit_status.values
)

ax.set_title(
    "Percentage of Profitable Records by Season"
)

ax.set_xlabel(
    "Season"
)

ax.set_ylabel(
    "Profitable Records (%)"
)

ax.set_ylim(
    0,
    100
)

save_graph(
    fig,
    "14_profitable_farms_by_season.png"
)


# ============================================================
# 25. OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("15. OUTLIER ANALYSIS")
print("=" * 70)

Q1 = df[
    "Profit_INR"
].quantile(
    0.25
)

Q3 = df[
    "Profit_INR"
].quantile(
    0.75
)

IQR = Q3 - Q1

lower_limit = (
    Q1 -
    1.5 * IQR
)

upper_limit = (
    Q3 +
    1.5 * IQR
)

profit_outliers = df[
    (
        df["Profit_INR"] <
        lower_limit
    )
    |
    (
        df["Profit_INR"] >
        upper_limit
    )
]

print(
    "\nQ1:",
    round(Q1, 2)
)

print(
    "Q3:",
    round(Q3, 2)
)

print(
    "IQR:",
    round(IQR, 2)
)

print(
    "Lower Limit:",
    round(lower_limit, 2)
)

print(
    "Upper Limit:",
    round(upper_limit, 2)
)

print(
    "Number of Profit Outliers:",
    len(profit_outliers)
)


# ============================================================
# 26. FINAL SCORECARD
# ============================================================

print("\n" + "=" * 70)
print("16. FINAL SEASONAL SCORECARD")
print("=" * 70)

scorecard = (
    df.groupby("Season")
    .agg({

        "Yield_Tonnes_Ha": "mean",

        "Profit_INR": "mean",

        "Revenue_INR": "mean",

        "Total_Cost_INR": "mean",

        "Water_Used_m3": "mean",

        "Water_Efficiency_t_per_1000m3": "mean",

        "Rainfall_mm": "mean",

        "Avg_Temperature_C": "mean",

        "Disease_Pest_Risk_pct": "mean"
    })
    .reindex(season_order)
)

print(
    scorecard.round(2)
)


# ============================================================
# 27. AUTOMATIC KEY FINDINGS
# ============================================================

print("\n" + "=" * 70)
print("17. KEY FINDINGS")
print("=" * 70)

best_yield_season = (
    season_summary[
        "Avg_Yield"
    ].idxmax()
)

best_profit_season = (
    season_summary[
        "Avg_Profit"
    ].idxmax()
)

lowest_profit_season = (
    season_summary[
        "Avg_Profit"
    ].idxmin()
)

best_efficiency_season = (
    season_summary[
        "Avg_Water_Efficiency"
    ].idxmax()
)

lowest_efficiency_season = (
    season_summary[
        "Avg_Water_Efficiency"
    ].idxmin()
)

highest_rainfall_season = (
    season_summary[
        "Avg_Rainfall"
    ].idxmax()
)


print(
    f"\n1. Highest average yield: "
    f"{best_yield_season}"
)

print(
    f"2. Highest average profit: "
    f"{best_profit_season}"
)

print(
    f"3. Lowest average profit: "
    f"{lowest_profit_season}"
)

print(
    f"4. Highest water efficiency: "
    f"{best_efficiency_season}"
)

print(
    f"5. Lowest water efficiency: "
    f"{lowest_efficiency_season}"
)

print(
    f"6. Highest average rainfall: "
    f"{highest_rainfall_season}"
)


# ============================================================
# 28. BEST CROP BY SEASON
# ============================================================

print("\n" + "=" * 70)
print("18. BEST CROP BY SEASON")
print("=" * 70)

for _, row in (
    best_crop
    .sort_values("Season")
    .iterrows()
):

    print(
        f"{row['Season']}: "
        f"{row['Crop']} - "
        f"{row['Yield_Tonnes_Ha']:.2f} Tonnes/Ha"
    )


# ============================================================
# 29. WORST CROP BY SEASON
# ============================================================

print("\n" + "=" * 70)
print("19. WORST CROP BY SEASON")
print("=" * 70)

for _, row in (
    worst_crop
    .sort_values("Season")
    .iterrows()
):

    print(
        f"{row['Season']}: "
        f"{row['Crop']} - "
        f"{row['Yield_Tonnes_Ha']:.2f} Tonnes/Ha"
    )


# ============================================================
# 30. RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 70)
print("20. RECOMMENDATIONS")
print("=" * 70)

print(
    f"""
1. Crop Selection:
   Select crops based on their historical performance
   in each season.

2. Seasonal Planning:
   Give special attention to the {best_yield_season}
   season because it has the highest average yield.

3. Profit Improvement:
   Study the farming conditions associated with
   {best_profit_season}, which has the highest average profit.

4. Low-Profit Season:
   Improve cost control, crop selection and resource
   management during {lowest_profit_season}.

5. Water Management:
   Improve irrigation practices in seasons with lower
   water-use efficiency.

6. Fertilizer Management:
   Apply fertilizer according to crop requirements
   and soil conditions.

7. Environmental Monitoring:
   Monitor rainfall, temperature, humidity and soil
   moisture before and during crop cultivation.

8. Pest Management:
   Regular monitoring of disease and pest risk can
   help reduce potential crop losses.
"""
)


# ============================================================
# 31. FINAL CONCLUSION
# ============================================================

print("\n" + "=" * 70)
print("21. FINAL CONCLUSION")
print("=" * 70)

print(
    f"""
The Seasonal Agriculture Performance Analysis examined
agricultural data across Kharif, Rabi and Zaid seasons.

The study analyzed crop yield, production, revenue,
cost, profit, rainfall, temperature, humidity, soil
moisture, irrigation, water usage, fertilizer usage,
water efficiency and disease/pest risk.

The analysis identified {best_yield_season} as the season
with the highest average yield and {best_profit_season}
as the season with the highest average profit.

The study also compared different crops, irrigation
methods and states to identify variations in agricultural
performance.

Correlation analysis was used to understand relationships
between yield and important agricultural variables.

ANOVA was used to test seasonal differences in yield,
while the Kruskal-Wallis test was used to examine
differences in profit distributions.

Overall, the project demonstrates that data analytics
can help farmers and agricultural planners make better
decisions regarding crop selection, seasonal planning,
water management, fertilizer usage and profitability.

The findings can support more efficient, productive and
sustainable agricultural practices.
"""
)


# ============================================================
# 32. EXPORT CLEANED DATA
# ============================================================

df.to_csv(
    "cleaned_seasonal_agriculture_dataset.csv",
    index=False
)

print(
    "\nCreated: cleaned_seasonal_agriculture_dataset.csv"
)


# ============================================================
# 33. EXPORT SEASONAL SUMMARY
# ============================================================

season_summary.to_csv(
    "seasonal_summary.csv"
)

print(
    "Created: seasonal_summary.csv"
)


# ============================================================
# 34. EXPORT SCORECARD
# ============================================================

scorecard.to_csv(
    "seasonal_scorecard.csv"
)

print(
    "Created: seasonal_scorecard.csv"
)


# ============================================================
# 35. EXPORT CORRELATION RESULTS
# ============================================================

yield_corr.to_csv(
    "yield_correlations.csv"
)

print(
    "Created: yield_correlations.csv"
)


# ============================================================
# 36. EXPORT BEST CROP
# ============================================================

best_crop.to_csv(
    "best_crop_by_season.csv",
    index=False
)

print(
    "Created: best_crop_by_season.csv"
)


# ============================================================
# 37. EXPORT WORST CROP
# ============================================================

worst_crop.to_csv(
    "worst_crop_by_season.csv",
    index=False
)

print(
    "Created: worst_crop_by_season.csv"
)


# ============================================================
# 38. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    """
14 graphs have been created and saved in:

graphs/

Graph files:

01_number_of_records_by_season.png
02_average_yield_by_season.png
03_average_profit_by_season.png
04_rainfall_by_season.png
05_temperature_by_season.png
06_humidity_by_season.png
07_water_usage_by_season.png
08_water_efficiency_by_season.png
09_crop_yield_by_season.png
10_irrigation_method_vs_yield.png
11_fertilizer_vs_yield.png
12_correlation_matrix.png
13_top_states_by_yield.png
14_profitable_farms_by_season.png

Analysis files:

cleaned_seasonal_agriculture_dataset.csv
seasonal_summary.csv
seasonal_scorecard.csv
yield_correlations.csv
best_crop_by_season.csv
worst_crop_by_season.csv

============================================================
DONE!
============================================================
"""
)