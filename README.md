# Seasonal Agriculture Performance Analysis

## 📌 Project Overview

This project analyzes agricultural performance across different farming seasons using data analytics and visualization. The analysis focuses on crop yield, production, revenue, profit, environmental conditions, irrigation, water usage, fertilizer usage, and disease/pest risk.

The project compares **Kharif, Rabi, and Zaid** seasons to identify patterns and provide useful recommendations for better agricultural planning.

---

## 🎯 Problem Statement

Agricultural performance varies due to seasonal, environmental, resource, and economic factors. Farmers and agricultural planners need data-driven insights to understand which seasons, crops, irrigation methods, and resource-management practices provide better yield and profitability.

This project uses historical agriculture data to analyze these factors and support better farming decisions.

---

## 👥 End Users

* Farmers
* Agricultural planners
* Agricultural researchers
* Government agriculture departments
* Data analysts
* Students and researchers

---

## 🛠️ Technologies Used

* **Python**
* **Pandas** – Data cleaning and analysis
* **NumPy** – Numerical operations
* **Matplotlib** – Data visualization
* **SciPy** – Statistical analysis
* **CSV Dataset**
* **Visual Studio Code**

---

## 📊 Dataset

The project uses:

`seasonal_agriculture_performance_dataset (3).csv`

The dataset contains agricultural information such as:

* Farm details
* Season
* Crop
* State
* Farm area
* Rainfall
* Temperature
* Humidity
* Sunlight
* Soil conditions
* Fertilizer usage
* Pesticide usage
* Seed quality
* Yield
* Production
* Market price
* Cost
* Revenue
* Profit
* Water usage
* Water efficiency
* Disease and pest risk

---

## 🔍 Analysis Performed

The project performs:

1. Dataset loading and inspection
2. Missing-value analysis
3. Duplicate detection and removal
4. Data cleaning
5. Descriptive statistical analysis
6. Seasonal performance comparison
7. Environmental analysis
8. Resource usage analysis
9. Crop-wise yield analysis
10. Irrigation method comparison
11. Fertilizer and yield analysis
12. Correlation analysis
13. Statistical hypothesis testing
14. State-wise performance analysis
15. Profitability analysis

---

## 📈 Graphs Generated

The project generates exactly **14 graphs**:

1. Number of Records by Season
2. Average Yield by Season
3. Average Profit by Season
4. Rainfall by Season
5. Temperature by Season
6. Humidity by Season
7. Water Usage by Season
8. Water Efficiency by Season
9. Crop Yield by Season
10. Irrigation Method vs Yield
11. Fertilizer Usage vs Yield
12. Correlation Matrix
13. Top States by Yield
14. Profitable Farms by Season

All graphs are saved inside the:

`graphs/`

folder.

---

## 📁 Project Structure

```text
Seasonal_Agriculture_Project/
│
├── agriculture_analysis.py
│
├── seasonal_agriculture_performance_dataset (3).csv
│
├── cleaned_seasonal_agriculture_dataset.csv
├── seasonal_summary.csv
├── seasonal_scorecard.csv
├── yield_correlations.csv
├── best_crop_by_season.csv
├── worst_crop_by_season.csv
│
└── graphs/
    ├── 01_number_of_records_by_season.png
    ├── 02_average_yield_by_season.png
    ├── 03_average_profit_by_season.png
    ├── 04_rainfall_by_season.png
    ├── 05_temperature_by_season.png
    ├── 06_humidity_by_season.png
    ├── 07_water_usage_by_season.png
    ├── 08_water_efficiency_by_season.png
    ├── 09_crop_yield_by_season.png
    ├── 10_irrigation_method_vs_yield.png
    ├── 11_fertilizer_vs_yield.png
    ├── 12_correlation_matrix.png
    ├── 13_top_states_by_yield.png
    └── 14_profitable_farms_by_season.png
```

---

## ▶️ How to Run

### Step 1: Install Python

Make sure Python is installed on your computer.

### Step 2: Open the project in VS Code

Open the project folder in Visual Studio Code.

### Step 3: Install required libraries

Open the VS Code terminal and run:

```bash
pip install pandas numpy matplotlib scipy
```

### Step 4: Run the Python program

```bash
python agriculture_analysis.py
```

---

## 📂 Output

After successful execution, the program creates:

* Cleaned dataset
* Seasonal summary
* Seasonal scorecard
* Yield correlation results
* Best crop results
* Worst crop results
* 14 individual graph images

The graphs are automatically stored in the `graphs` folder.

---

## 💡 Key Findings

The analysis compares the three major seasons—**Kharif, Rabi, and Zaid**—based on yield, profit, environmental conditions, resource consumption, and profitability.

It also identifies the best-performing crops, irrigation methods, and states based on the available dataset.

---

## 💡 Recommendations

* Select crops according to seasonal performance.
* Improve irrigation and water-use efficiency.
* Monitor rainfall, temperature, humidity, and soil moisture.
* Optimize fertilizer application according to crop requirements.
* Monitor disease and pest risks.
* Focus on reducing unnecessary production costs.
* Use historical data to improve seasonal crop planning.

---

## 🚀 Future Scope

* Develop a machine-learning model for yield prediction.
* Add real-time weather data.
* Develop a web-based agriculture dashboard.
* Predict crop profitability before cultivation.
* Provide automated crop recommendations.
* Integrate IoT sensors for soil and irrigation monitoring.

---

## 🏁 Conclusion

This project demonstrates how Python-based data analytics can be used to understand agricultural performance across different seasons. By analyzing yield, profit, environmental conditions, irrigation, water usage, fertilizer, and pest risk, the project provides data-driven insights that can support better crop selection, resource management, profitability, and sustainable agricultural planning.

---

## 👨‍💻 Project Type

**Data Analytics / Agriculture / Python Project**
