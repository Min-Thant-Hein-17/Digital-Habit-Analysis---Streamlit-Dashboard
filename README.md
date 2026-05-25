# Digital-Habit-Analysis---Streamlit-Dashboard

# 📱 Digital Habit Analysis Dashboard

## Project Overview
This project is an interactive Streamlit dashboard built to analyze my personal digital habits, screen time, and productivity metrics. The goal is to explore whether high screen time hinders academic performance, how weekends differ from weekdays, and to track long-term burnout trends over my university career.

## Project Motivation
As a junior data analyst, I wanted to apply my skills to real-world data that directly affects me. By understanding my own digital behaviors, I can make data-driven decisions to optimize my study routines, manage stress during internship meetings, and maintain a healthier work-life balance.

## Datasets
The analysis relies on two datasets:
1. **Daily Behavior (March 2026):** Micro-level data capturing daily screen time, sleep, stress, app usage, and caffeine intake.
2. **3-Year Summary:** Macro-level data tracking monthly averages across different academic semesters and summer breaks.

## Dashboard Features
* **Interactive Filtering:** Slice data by day of the week and self-reported stress levels using a sidebar menu.
* **Metric Cards:** Quick summaries of average focus, sleep, and screen time based on the active filters.
* **Exploratory Visualizations:** * Scatter plots mapping correlation between screen time and productivity.
  * Bar charts breaking down dominant application usage.
* **Ethics Section:** A transparent discussion on self-reporting bias, data privacy, and the limits of correlation vs. causation.

## Technologies Used
* **Python** (Data processing and logic)
* **Streamlit** (Web application framework)
* **Pandas** (Data manipulation)
* **Plotly / Matplotlib / Seaborn** (Data visualization)
* **Ngrok** (Local deployment and secure tunneling)

## Installation & Setup
This project utilizes standard Python virtual environments (`venv`) to prevent package dependency conflicts.

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/your-username/digital-habit-analysis.git](https://github.com/your-username/digital-habit-analysis.git)
   cd digital-habit-analysis
