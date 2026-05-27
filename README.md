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

> Note: Both datasets are self-collected and self-reported. No real names, device identifiers, or location data are included.

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

I am a Year 2 university student, and this project is about my own digital habits. I chose this topic because it is something I deal with every day — spending too much time on my phone, feeling tired, and sometimes not being productive even when I studied for many hours. I wanted to understand why that happens.

I started tracking my habits from August 2023, when I first entered university. Every month, I recorded things like how many hours I used my screen, how many hours I studied, how well I slept, and how stressed I felt. I gave myself a score from 1 to 10 for productivity, mood, and focus each month. In March 2026, I also tracked these things every single day, so I could see more detailed patterns.

When I look back at my Year 1 data, I can see that I used to spend a lot of time on social media and entertainment without much structure. I did not really think about how my phone habits were affecting my studies. Now in Year 2, I feel like I am more aware of what I do on my phone and why. But I was not sure if my habits had actually improved, or if I just felt that way. That is why I built this dashboard — to check the data and find out the real answer.

This project helped me tell my growth story using actual numbers instead of just feelings. I think it is important to look at our own behavior honestly, even when the data shows things we do not want to see.

---

### 2. Key Findings

#### Finding 1 — My productivity slowly improved every year

When I look at my monthly average productivity scores across all three years, I can see a clear upward trend. In 2023, my average was **5.16 out of 10**. In 2024 it went up to **5.64**, then **6.02** in 2025, and **6.70** in 2026. This made me feel good because it means my habits are actually getting better over time, not just in my imagination. My best month was **February 2026 with 7.2/10**, and my worst month was **July 2024 with only 4.0/10**, which was during summer break when I had no schedule at all.

#### Finding 2 — I experienced burnout 5 times in 3 years

Out of 32 months that I tracked, **5 months were burnout months**. These were months when my stress was very high, my sleep was less, and my productivity dropped. Looking at when these happened, most of them were during exam periods or right after semester ended. This tells me that I struggle most when there is too much pressure at the same time, or when I suddenly have no structure at all.

#### Finding 3 — I spent a lot of time on screens, but it changed over time

My average daily screen time over 3 years was **9.43 hours**, which is quite high. But what changed is what I was doing during that screen time. In Year 1, a big portion was social media and entertainment. By Year 2 and 3, I started using my screen more for study tools and productive apps. Social media averaged **3.01 hours per day** and study hours averaged **3.18 hours per day** across all months. So studying slightly won over social media overall, but the gap was small.

#### Finding 4 — Using my phone late at night made me sleep less

In March 2026, I used my phone late at night on **15 out of 31 days**. On those nights, I only slept **6.28 hours on average**. But on nights when I did not use my phone late, I slept **7.01 hours** — that is about 43 minutes more. I did not realise the difference was so clear until I looked at the data. Less sleep also meant lower focus score the next day, so this is a habit I really need to fix.

#### Finding 5 — Studying more helped, but not as much as I expected

I thought that the more hours I studied, the more productive I would feel. The data shows this is true, but only weakly (correlation = 0.28). This surprised me. It means that just sitting down to study is not enough — the quality of my sleep, my stress level, and what apps I was using also played a big role in how productive I actually felt that day.

#### Finding 6 — I was slightly more productive on weekends

In March 2026, my average productivity on weekends was **5.78/10**, which is a little higher than weekdays at **5.41/10**. I think this is because on weekends I can choose when to study, so I study when I feel ready. On weekdays I sometimes have to study even when I am tired from class. This was an interesting finding that I did not expect.

---

### 3. Decision-Making Explanation

After looking at my data, I came up with three things I want to change about my habits. I tried to be honest about what the data actually shows, and also about where the data is not strong enough to be fully sure.

#### Decision 1 — Stop using my phone late at night before school days

The data shows that on nights I used my phone late, I slept 43 minutes less than on nights I did not. Less sleep = lower focus score the next day. So I want to put my phone down by 10:30 PM on Sunday, Monday, Tuesday, and Wednesday nights, because those nights affect the next morning the most.

I know this decision has a limitation though. I only have 31 days of data, which is not a lot. Also, it is possible that on stressful days I both sleep badly AND use my phone more — so the phone might not be the main reason for poor sleep. But even so, trying this change costs nothing, so it is worth doing.

#### Decision 2 — Study for at least 3 hours on Tuesday and Thursday

From my March 2026 data, days with more than 3 study hours tended to have higher productivity scores. Tuesday and Thursday were also my highest focus days based on the heatmap. So I want to protect those days and not let other things get in the way of studying.

The limitation here is that correlation does not mean causation. I might have studied more on days I already felt motivated — not the other way around. And this is only one month of data, so I cannot be 100% sure this pattern would hold in other months.

#### Decision 3 — Use social media less than 2 hours a day during exam months

My 3-year data shows that social media hours go up a lot in April, which is also when I had the most burnout. In months where I studied more than I used social media, my productivity was higher. So I want to set a 2-hour daily limit on social media during exam season using my phone's screen time settings.

The honest limitation is that I estimated my social media hours myself — I did not track them automatically. So the numbers might not be perfectly accurate. Also, sometimes I use social media to relax when I am stressed, so cutting it completely might not feel good. I just want to reduce it, not stop it entirely.

---

### 4. Ethical Discussion

#### Privacy

All the data in this project is my own. I collected it myself by filling in a spreadsheet every day or every month. I did not use any app to track me automatically, and I did not include any information about other people. There are no real names, no school names, and no app names in the dataset — only categories like "Study Tools" or "Social Media." This way, even if someone sees my data, they cannot identify me or anyone else from it.

#### Bias and Honest Limitations

The biggest problem with my dataset is that everything is self-reported. When I give myself a "7 out of 10" for productivity, that is just my own feeling at the end of the day. I might give myself a higher score if something good happened in the evening, even if the rest of the day was bad. This is called memory bias or recency bias.

Another issue is that my idea of what a "7/10" day means probably changed between Year 1 and Year 3. In Year 1, a day where I studied 2 hours felt very productive. Now in Year 2, I expect more from myself. So comparing my scores across years might not be perfectly fair.

My daily dataset only has 31 days. That is too small to make strong conclusions. The patterns I found are interesting, but they might look different in a different month or a different semester.

I also have to admit that because I knew this data would be shown to my professor and classmates, I might have unconsciously recorded slightly better scores than the truth. I tried to be honest, but I cannot be completely sure.

#### Why I Chose Each Chart

I chose simple charts — bar charts, line charts, and donut charts — because my audience includes classmates and a professor who may not be familiar with complex visualizations. I wanted everyone to understand the charts without needing an explanation.

I did not use the charts to exaggerate my results. For example, I did not start the Y-axis at a high number to make improvements look bigger than they are. I also wrote captions below each chart to explain what it shows in plain language.

One risk with my comparison table is that the arrows (up or down) might make small differences look more important than they really are. I tried to address this by marking very small differences as "Watch" instead of labeling them as clearly better or worse.

#### Final Note

This project is a personal learning exercise. The findings only apply to me and my situation. I would not tell other students to follow the same decisions just because they worked for me in one month of data. Data can tell us interesting things, but we should always be careful about how much we trust it, especially when the dataset is small and self-reported.

---

## Live Dashboard

The dashboard is publicly deployed and accessible at:

🔗 **[https://digital-habit-analysis---app-dashboard.streamlit.app/](https://digital-habit-analysis---app-dashboard.streamlit.app/)**

No installation required. Open the link in any browser to explore the interactive dashboard, apply filters, and navigate between sections.
