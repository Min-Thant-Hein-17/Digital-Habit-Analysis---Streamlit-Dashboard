# 📱 Digital Habit Analysis Dashboard

A personal data project exploring the relationship between screen time, study habits, and academic productivity across three years of university life.

---


## Project Overview

This project is an interactive Streamlit dashboard built to analyze my personal digital habits, screen time, and productivity metrics. The goal is to explore whether high screen time hinders academic performance, how weekends differ from weekdays, and to track long-term burnout trends over my university career.

## Project Motivation

As a junior data analyst, I wanted to apply my skills to real-world data that directly affects me. By understanding my own digital behaviors, I can make data-driven decisions to optimize my study routines, manage stress during internship meetings, and maintain a healthier work-life balance.

## Datasets

The analysis relies on two datasets:

| Dataset | Coverage | Rows | Key Variables |
|---|---|---|---|
| `digital_habits_march2026.csv` | March 1–31, 2026 | 31 days | Screen time, study hours, productivity, sleep, stress, mood, app category, caffeine, late-night usage |
| `parami_digital_summary_3years.csv` | Aug 2023 – Mar 2026 | 32 months | Monthly averages for all core metrics, burnout indicator, dominant app category, semester label |

> ⚠️ Both datasets are self-collected and self-reported. No real names, device identifiers, or location data are included.

## Dashboard Features

- **Interactive Filtering** — Slice data by day type (Weekday/Weekend) and stress level using the sidebar
- **Metric Cards** — Quick summaries of average focus, sleep, screen time, and productivity
- **7 Visualizations** — Line charts, bar charts, scatter plots, heatmaps, donut charts, stacked area charts, and comparison tables
- **Cross-Dataset Insights** — Compares March 2026 daily behavior against the 3-year historical baseline
- **Decision-Making Section** — Evidence-based personal commitments supported by data
- **Ethics & Responsibility Section** — Transparent discussion of bias, privacy, and visualization limitations

## Technologies Used

- **Python** — Data processing and logic
- **Streamlit** — Web application framework
- **Pandas** — Data manipulation
- **Plotly** — Interactive data visualization

---

## Report

### 1. Story Description

This project tells the story of my personal growth as a university student through the lens of digital habit data. The story spans three academic years — from August 2023, when I was a first-year student adjusting to university life, through March 2026, when I was managing coursework alongside an internship as a third-year student.

During this period, I noticed that my relationship with my phone and laptop had changed significantly. In my first year, I spent long hours on social media and entertainment apps without much structure. By my third year, I had shifted toward using my screen time more intentionally — study tools, academic resources, and productivity apps began to dominate. But the question I could never fully answer was: **did those changes actually make me more productive, or was I just telling myself a story?**

To answer this, I began tracking my digital habits monthly using a personal spreadsheet, recording average screen time, study hours, sleep, stress, mood, and focus. In March 2026, I went further and tracked these metrics daily, capturing 31 days of granular behavioral data.

The two datasets together allow me to compare my moment-to-moment behavior in March 2026 against the bigger picture of who I was as a first-year student — and to measure, in actual numbers, how much I have grown.

This project is part of a course final project that challenges students to transform a personal story into a data-driven, interactive dashboard that supports decision-making while demonstrating ethical data practices.

---

### 2. Key Findings

#### Finding 1 — My productivity has consistently improved year over year

Across 32 months of tracking, average monthly productivity rose from **5.16/10 in 2023** to **5.64/10 in 2024**, **6.02/10 in 2025**, and **6.70/10 in 2026**. This steady improvement suggests that habit changes over my university career have had a measurable positive effect. My best single month was **February 2026 (7.2/10)**, and my worst was **July 2024 (4.0/10)** — a summer break month with no academic structure.

#### Finding 2 — Burnout clusters around exam and transition periods

Of the 32 months tracked, **5 were flagged as burnout months**. These months did not occur randomly — they concentrated around April (end-of-semester exam periods) and during the transition from semester to summer break. Burnout months consistently showed elevated stress, reduced sleep, and below-average productivity, confirming that workload spikes and schedule disruptions are the strongest predictors of burnout in my data.

#### Finding 3 — Screen time grew, but so did productive screen time

Average daily screen time across the full 3-year period was **9.43 hours**. Rather than falling over time, screen time remained high — but its composition changed. Social media averaged **3.01 hours/day** across all months, while study hours averaged **3.18 hours/day**. By Year 3, productive screen time had grown as a proportion of total screen time, meaning more hours were being spent on study tools and academic apps rather than passive entertainment.

#### Finding 4 — In March 2026, late-night phone use measurably reduced sleep

During March 2026 (31 days of daily tracking), I used my phone late at night on **15 out of 31 days**. On late-night usage days, I averaged **6.28 hours of sleep**. On days without late-night usage, I averaged **7.01 hours** — a difference of 43 minutes per night. Given that sleep quality was one of the strongest predictors of next-day focus score in the daily dataset, this is a concrete and actionable finding.

#### Finding 5 — Study hours and productivity are positively correlated, but weakly

A correlation analysis of March 2026 daily data found a positive relationship between daily study hours and productivity score (r = 0.28). While the direction is as expected — more studying tends to mean higher productivity — the relatively weak correlation suggests that study hours alone do not determine how productive a day feels. Sleep quality, stress level, and app category all appear to play important moderating roles.

#### Finding 6 — Weekends were slightly more productive in March 2026

Counterintuitively, my weekend productivity average in March 2026 (**5.78/10**) was slightly higher than my weekday average (**5.41/10**). This likely reflects the flexibility of weekend schedules — no fixed class times or internship commitments meant I could study during my peak energy hours. However, the difference is small and may not hold across other months.

---

### 3. Decision-Making Explanation

Based on the patterns observed across both datasets, I identified three evidence-based decisions to implement going forward. Each decision is grounded in specific findings from the data, and each comes with an honest acknowledgment of its limitations.

#### Decision 1 — Eliminate late-night phone use on class and internship nights

**Evidence:** On days without late-night phone use, I averaged 43 more minutes of sleep per night (7.01 vs 6.28 hours). Sleep quality was positively correlated with focus score in the March 2026 daily data. Monday and Wednesday nights (before class days) showed the highest frequency of late-night usage.

**Action:** I will set a phone-down rule at 10:30 PM on Sunday, Monday, Tuesday, and Wednesday nights — the four evenings that most directly affect the next morning's focus.

**Limitation:** This finding is based on 31 days of self-reported data. The relationship between late-night usage and sleep may be confounded by stress — high-stress days may cause both poor sleep and late-night scrolling, meaning the phone itself may not be the root cause. A longer tracking period across multiple months would strengthen this conclusion.

#### Decision 2 — Protect weekday structured study blocks of at least 3 hours

**Evidence:** The scatter plot of March 2026 data showed that weekday days with 3 or more study hours clustered toward higher productivity scores. The 3-year trend also showed that months dominated by Study Tools (rather than social media apps) had higher average productivity scores.

**Action:** I will block 3-hour study windows on Tuesday and Thursday afternoons — the days that showed the highest focus scores in the March 2026 heatmap — and treat these blocks as non-negotiable commitments.

**Limitation:** March 2026 covers only one month and one semester. Correlation between study hours and productivity does not establish causation — I may have studied more on days I already felt motivated, rather than studying causing the motivation. The correlation coefficient (r = 0.28) is modest, meaning other factors matter significantly.

#### Decision 3 — Reduce social media below 2 hours per day during exam months

**Evidence:** The grouped bar chart of the 3-year summary showed that social media hours spike during April — the same month that contains the most burnout flags in the dataset. In months where study hours significantly exceeded social media hours, average productivity scores were higher.

**Action:** In April 2026 (my next exam month), I will use a screen time app to set a hard 2-hour daily cap on social media, and review compliance weekly.

**Limitation:** Social media hours were self-estimated and tracked monthly — not measured automatically. This introduces the possibility of underreporting. Additionally, reducing social media during stressful exam periods may not be straightforward if social media also serves as a stress relief outlet. The data does not capture the quality or purpose of social media use, only the quantity.

---

### 4. Ethical Discussion

#### Privacy and Data Anonymization

All data in this project was self-collected through a personal spreadsheet over three years. No third-party tracking tools, phone analytics exports, or automated data collection systems were used. The dataset contains no real names, contact information, location data, device identifiers, or details about other people. Internship and academic institutions are referenced only through binary flags (Yes/No) or generic labels (e.g., "Internship day"), not by name or identifying detail.

App usage is recorded as categories (e.g., "Study Tools", "Social Media", "Entertainment") rather than specific app names, which reduces the risk of inferring sensitive behavioral patterns from brand-specific usage.

#### Bias and Limitations

**Memory and self-reporting bias** is the most significant limitation of this dataset. Scores such as "productivity score", "mood score", and "stress level" were assigned at the end of each day based on personal reflection. Research in psychology consistently shows that end-of-day self-assessments are influenced by the most recent events of the day (recency effect) and by the overall emotional tone of the day, rather than being a true average of hourly experience.

**Subjective score drift** is a related concern. A "7/10" productivity score in Year 1 may not represent the same standard as a "7/10" in Year 3. As my academic workload, complexity of tasks, and personal expectations changed over time, my internal benchmark for what constitutes a "productive" day likely shifted as well. This means year-over-year comparisons of raw scores should be interpreted cautiously.

**Small dataset size** limits statistical reliability. The March 2026 daily dataset contains only 31 observations. Patterns that appear meaningful in this dataset — such as the weekday vs. weekend productivity difference — may not hold across other months or contexts. No finding from this dataset should be presented as statistically significant in a scientific sense.

**Social desirability bias** may have affected self-reporting. Knowing that this data would be analyzed and presented publicly may have caused unconscious score inflation — reporting slightly higher productivity or slightly lower social media hours than was accurate.

#### Visualization Ethics

Each visualization in this dashboard was chosen to communicate a specific and honest insight, not to exaggerate findings. Key choices and their associated risks are disclosed below:

- **Line charts** are used for time-series data where continuity is real (monthly tracking was consistent across the 3-year period). Risk: viewers may assume data was collected daily rather than monthly.
- **Scatter plots with trendlines** use Ordinary Least Squares regression lines, which only describe statistical association. The chart captions explicitly state that correlation does not imply causation.
- **The comparison table** (March 2026 vs. historical averages) uses directional arrows (↑/↓) and color-coded status indicators. Risk: visual emphasis on "better" vs. "worse" could lead viewers to over-interpret small differences. Differences of less than 0.3 points on a 1–10 scale are labeled "Watch" rather than "Better" or "Worse" to reduce this risk.
- **The calendar heatmap** uses blank cells for days excluded by the sidebar filter. This could be misread as "zero" values rather than "filtered out." The chart caption addresses this explicitly.

#### Responsible Use of Findings

The decisions recommended in this dashboard are based on patterns in a single-person, self-reported dataset collected over a limited time period. They are intended as personal behavioral experiments, not prescriptions for others. The findings should not be generalized to other students or used to make claims about student productivity in general.

This project is an academic exploration. Its value lies in the process of applying data thinking to personal experience — not in producing scientifically validated conclusions.

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/digital-habit-dashboard.git
cd digital-habit-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py
```

**Folder structure required:**
```
project/
├── app.py
├── README.md
├── requirements.txt
└── data/
    ├── digital_habits_march2026.csv
    └── parami_digital_summary_3years.csv
```

**requirements.txt:**
```
streamlit
pandas
plotly
statsmodels
```
