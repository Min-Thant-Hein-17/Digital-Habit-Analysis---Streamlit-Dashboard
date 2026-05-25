import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Parami's Digital Habit Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLES ---
st.markdown("""
<style>
    .metric-label { font-size: 0.75rem; color: #888; margin-bottom: 2px; }
    .metric-value { font-size: 1.6rem; font-weight: 600; }
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #4C6EF5;
        padding: 12px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    .ethics-box {
        background: #fff8e1;
        border-left: 4px solid #f59f00;
        padding: 12px 16px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    section[data-testid="stSidebar"] { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    daily_df = pd.read_csv("data/digital_habits_march2026.csv")
    monthly_df = pd.read_csv("data/parami_digital_summary_3years.csv")

    # Build a proper date label for monthly timeline
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    monthly_df["month_num"] = pd.to_datetime(monthly_df["month"], format="%B").dt.month
    monthly_df = monthly_df.sort_values(["year","month_num"]).reset_index(drop=True)
    monthly_df["period"] = monthly_df["month"].str[:3] + " " + monthly_df["year"].astype(str)

    # Parse daily dates
    daily_df["date"] = pd.to_datetime(daily_df["date"], format="%m/%d/%Y")
    daily_df["day_num"] = daily_df["date"].dt.day

    return daily_df, monthly_df

df_daily, df_monthly = load_data()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
st.sidebar.title("Parami's Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["📖 Story Overview",
     "📊 3-Year Trends",
     "🔍 March 2026 Deep Dive",
     "🔗 Cross-Dataset Insights",
     "🎯 Decision-Making",
     "⚖️ Ethics & Responsibility"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Filters")

# Weekday filter (affects daily charts)
day_types = df_daily["weekday_type"].unique().tolist()
selected_days = st.sidebar.multiselect("Day Type (March 2026):", day_types, default=day_types)

# Stress level filter
max_stress = st.sidebar.slider(
    "Max Stress Level (March 2026):",
    min_value=int(df_daily["stress_level"].min()),
    max_value=int(df_daily["stress_level"].max()),
    value=int(df_daily["stress_level"].max())
)

# Semester filter (affects 3-year charts)
all_semesters = df_monthly["semester"].unique().tolist()
selected_sems = st.sidebar.multiselect("Semesters (3-Year):", all_semesters, default=all_semesters)

# Metric selector for trend chart
trend_metric = st.sidebar.selectbox(
    "Trend metric (3-Year chart):",
    options=["avg_productivity_score", "avg_screen_time_hours",
             "avg_study_hours", "avg_sleep_hours",
             "avg_stress_level", "avg_focus_score"],
    format_func=lambda x: x.replace("avg_","").replace("_"," ").title()
)

# Apply filters
filtered_daily = df_daily[
    (df_daily["weekday_type"].isin(selected_days)) &
    (df_daily["stress_level"] <= max_stress)
].copy()

filtered_monthly = df_monthly[df_monthly["semester"].isin(selected_sems)].copy()

# ─────────────────────────────────────────
# PAGE: STORY OVERVIEW
# ─────────────────────────────────────────
if page == "📖 Story Overview":
    st.title("📱 My Digital Habit Growth Journey")
    st.markdown("""
    > *"From scrolling to studying — tracking three years of digital habits to become a more intentional student."*
    """)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### About This Project
        This dashboard tells the story of my personal growth as a university student through the lens of **digital habit data**.  
        Starting in August 2023 (Year 1, Semester 1) through March 2026 (Year 3, Semester 2), I tracked my screen time,
        study hours, productivity, sleep, stress, mood, and focus each month.

        In March 2026, I also recorded **daily** data to capture micro-level patterns — which days I was most productive,
        how late-night phone use affected my sleep, and whether caffeine helped or hurt.

        ### Why It's Meaningful
        - Digital habits are easy to overlook but deeply affect academic performance.
        - I wanted to *see the data* behind my best and worst semesters.
        - This project helps me make evidence-based decisions about screen time, sleep, and study routines.

        ### Dataset Summary
        | Dataset | Coverage | Rows | Key Variables |
        |---|---|---|---|
        | Monthly 3-Year Summary | Aug 2023 – Mar 2026 | 32 months | Productivity, screen time, sleep, burnout |
        | March 2026 Daily Log | Mar 1–31, 2026 | 31 days | Daily scores, app usage, caffeine, breaks |
        """)

    with col2:
        st.markdown("### 📌 Quick Stats")
        months_tracked = len(df_monthly)
        burnout_months = (df_monthly["burnout_indicator"] == "Yes").sum()
        best_prod = df_monthly["avg_productivity_score"].max()
        best_month = df_monthly.loc[df_monthly["avg_productivity_score"].idxmax(), "period"]

        st.metric("Months Tracked", f"{months_tracked}")
        st.metric("Burnout Months", f"{burnout_months} / {months_tracked}")
        st.metric("Peak Productivity Score", f"{best_prod:.1f}/10")
        st.metric("Best Month", best_month)
        st.metric("March 2026 Avg Productivity",
                  f"{df_daily['productivity_score'].mean():.1f}/10")


# ─────────────────────────────────────────
# PAGE: 3-YEAR TRENDS
# ─────────────────────────────────────────
elif page == "📊 3-Year Trends":
    st.title("📊 3-Year Monthly Trends")
    st.markdown("How my digital habits evolved from Year 1 to Year 3. Red markers = burnout months.")

    # --- VIZ 1: Multi-line trend with burnout markers ---
    st.subheader("📈 Visualization 1 — Monthly Productivity & Screen Time Over 3 Years")
    st.caption("Line chart · Source: parami_digital_summary_3years.csv")

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

    burnout_mask = filtered_monthly["burnout_indicator"] == "Yes"
    burnout_pts = filtered_monthly[burnout_mask]

    fig_trend.add_trace(
        go.Scatter(
            x=filtered_monthly["period"],
            y=filtered_monthly["avg_productivity_score"],
            name="Productivity Score",
            line=dict(color="#4C6EF5", width=2.5),
            mode="lines+markers",
            marker=dict(size=5)
        ),
        secondary_y=False
    )
    fig_trend.add_trace(
        go.Scatter(
            x=filtered_monthly["period"],
            y=filtered_monthly["avg_screen_time_hours"],
            name="Screen Time (hrs)",
            line=dict(color="#74C0FC", width=2, dash="dot"),
            mode="lines+markers",
            marker=dict(size=5)
        ),
        secondary_y=True
    )
    # Burnout markers
    if not burnout_pts.empty:
        fig_trend.add_trace(
            go.Scatter(
                x=burnout_pts["period"],
                y=burnout_pts["avg_productivity_score"],
                mode="markers",
                name="Burnout Month",
                marker=dict(color="crimson", size=12, symbol="x", line=dict(width=2))
            ),
            secondary_y=False
        )

    # March 2026 reference line
    if "Mar 2026" in filtered_monthly["period"].values:
        fig_trend.add_vline(
            x="Mar 2026",
            line_dash="dash",
            line_color="orange",
            annotation_text="Now (Mar 2026)",
            annotation_position="top right"
        )

    fig_trend.update_layout(
        height=420,
        legend=dict(orientation="h", y=1.08),
        hovermode="x unified",
        xaxis=dict(tickangle=-45, tickfont=dict(size=10))
    )
    fig_trend.update_yaxes(title_text="Productivity Score (1–10)", secondary_y=False)
    fig_trend.update_yaxes(title_text="Screen Time (hours)", secondary_y=True)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Key insight:</b> Screen time generally increased over 3 years, but so did productivity — suggesting I learned
    to use my screen time more intentionally. Burnout months cluster around exam periods (April, December).
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- VIZ 2: Grouped bar — social media vs study by semester ---
    st.subheader("📊 Visualization 2 — Social Media vs Study Hours by Semester")
    st.caption("Grouped bar chart · Source: parami_digital_summary_3years.csv")

    sem_df = filtered_monthly.groupby("semester", sort=False).agg(
        Social_Media=("avg_social_media_hours", "mean"),
        Study=("avg_study_hours", "mean")
    ).reset_index()

    sem_order = ["Year1-Sem1","Year1-Sem2","Year1-Summer",
                 "Year2-Sem1","Year2-Sem2","Year2-Summer",
                 "Year3-Sem1","Year3-Sem2"]
    sem_df["semester"] = pd.Categorical(sem_df["semester"], categories=sem_order, ordered=True)
    sem_df = sem_df.sort_values("semester")

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=sem_df["semester"], y=sem_df["Social_Media"],
        name="Social Media (hrs)", marker_color="#F76707"
    ))
    fig_bar.add_trace(go.Bar(
        x=sem_df["semester"], y=sem_df["Study"],
        name="Study Hours (hrs)", marker_color="#2F9E44"
    ))
    fig_bar.update_layout(
        barmode="group",
        height=380,
        xaxis_title="Semester",
        yaxis_title="Average Daily Hours",
        legend=dict(orientation="h", y=1.05),
        xaxis=dict(tickangle=-30)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Key insight:</b> Study hours consistently exceed social media hours during academic semesters,
    but the gap narrows during summer breaks — when social media peaks and structure disappears.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- Selectable metric trend ---
    st.subheader(f"📉 Explore Any Metric Over Time")
    st.caption(f"Currently showing: {trend_metric.replace('avg_','').replace('_',' ').title()} — change in sidebar")

    fig_metric = px.line(
        filtered_monthly, x="period", y=trend_metric,
        markers=True,
        color_discrete_sequence=["#7048E8"]
    )
    fig_metric.update_layout(height=320, xaxis=dict(tickangle=-45, tickfont=dict(size=10)))
    st.plotly_chart(fig_metric, use_container_width=True)


# ─────────────────────────────────────────
# PAGE: MARCH 2026 DEEP DIVE
# ─────────────────────────────────────────
elif page == "🔍 March 2026 Deep Dive":
    st.title("🔍 March 2026 — Daily Habits Deep Dive")
    st.markdown("Day-by-day patterns from my most recent month of detailed tracking.")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Screen Time", f"{filtered_daily['total_screen_time_hours'].mean():.1f} hrs")
    col2.metric("Avg Productivity", f"{filtered_daily['productivity_score'].mean():.1f} / 10")
    col3.metric("Avg Sleep", f"{filtered_daily['sleep_hours'].mean():.1f} hrs")
    col4.metric("Avg Focus Score", f"{filtered_daily['focus_score'].mean():.1f} / 10")

    st.divider()

    # --- VIZ 3: Heatmap calendar ---
    st.subheader("📅 Visualization 3 — March 2026 Daily Productivity Heatmap")
    st.caption("Calendar heatmap · Source: digital_habits_march2026.csv")

    heatmap_metric = st.selectbox(
        "Switch heatmap metric:",
        ["productivity_score", "mood_score", "stress_level", "focus_score", "sleep_hours"],
        format_func=lambda x: x.replace("_"," ").title()
    )

    cal_df = filtered_daily[["date","day_num","day_of_week", heatmap_metric]].copy()
    cal_df["week"] = cal_df["date"].dt.isocalendar().week
    cal_df["week_rel"] = cal_df["week"] - cal_df["week"].min()

    day_order = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    cal_df["day_idx"] = cal_df["day_of_week"].apply(lambda d: day_order.index(d))

    pivot = cal_df.pivot_table(index="day_idx", columns="week_rel", values=heatmap_metric)

    fig_heat = px.imshow(
        pivot,
        labels=dict(x="Week", y="Day of Week", color=heatmap_metric.replace("_"," ").title()),
        y=day_order,
        color_continuous_scale="RdYlGn" if "stress" not in heatmap_metric else "RdYlGn_r",
        text_auto=".1f",
        aspect="auto"
    )
    fig_heat.update_layout(
        height=320,
        xaxis=dict(tickvals=list(range(5)), ticktext=["Wk 1","Wk 2","Wk 3","Wk 4","Wk 5"])
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Key insight:</b> Productivity tends to dip on Sundays and spike mid-week (Tuesday–Thursday).
    Stress peaks align with assignment deadlines and internship meeting days.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- VIZ 4: Scatter — Study hours vs Productivity ---
    st.subheader("🔵 Visualization 4 — Study Hours vs Productivity Score")
    st.caption("Scatter plot · Source: digital_habits_march2026.csv")

    fig_scatter = px.scatter(
        filtered_daily,
        x="study_hours",
        y="productivity_score",
        color="weekday_type",
        size="caffeine_intake_cups",
        hover_data=["date", "most_used_app_category", "stress_level", "sleep_hours"],
        color_discrete_map={"Weekday": "#4C6EF5", "Weekend": "#F76707"},
        labels={
            "study_hours": "Study Hours",
            "productivity_score": "Productivity Score (1–10)",
            "weekday_type": "Day Type",
            "caffeine_intake_cups": "Caffeine (cups)"
        },
        trendline="ols"
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Key insight:</b> More study hours correlate positively with productivity on weekdays.
    Weekends show a weaker relationship — suggesting rest quality matters as much as study quantity.
    Dot size = caffeine cups; notice higher caffeine on high-stress days, not necessarily high-productivity days.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- Bonus: App category bar ---
    st.subheader("📱 App Category Frequency — March 2026")
    st.caption("Bar chart · Source: digital_habits_march2026.csv")

    app_counts = filtered_daily["most_used_app_category"].value_counts().reset_index()
    app_counts.columns = ["Category", "Days"]
    fig_app = px.bar(
        app_counts, x="Category", y="Days",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_app.update_layout(showlegend=False, height=320, yaxis_title="Number of Days Dominant")
    st.plotly_chart(fig_app, use_container_width=True)


# ─────────────────────────────────────────
# PAGE: CROSS-DATASET INSIGHTS
# ─────────────────────────────────────────
elif page == "🔗 Cross-Dataset Insights":
    st.title("🔗 Cross-Dataset Insights")
    st.markdown("Comparing March 2026 daily data against historical monthly averages.")

    # --- VIZ 5: Now vs Then comparison table ---
    st.subheader("📋 Visualization 5 — March 2026 vs Historical Averages")
    st.caption("Comparison table · Both datasets")

    march_hist = df_monthly[
        (df_monthly["month"] == "March") & (df_monthly["year"] < 2026)
    ].agg({
        "avg_productivity_score": "mean",
        "avg_screen_time_hours": "mean",
        "avg_study_hours": "mean",
        "avg_sleep_hours": "mean",
        "avg_stress_level": "mean",
        "avg_focus_score": "mean"
    })

    march_now = {
        "avg_productivity_score": df_daily["productivity_score"].mean(),
        "avg_screen_time_hours": df_daily["total_screen_time_hours"].mean(),
        "avg_study_hours": df_daily["study_hours"].mean(),
        "avg_sleep_hours": df_daily["sleep_hours"].mean(),
        "avg_stress_level": df_daily["stress_level"].mean(),
        "avg_focus_score": df_daily["focus_score"].mean()
    }

    labels = {
        "avg_productivity_score": "Productivity Score",
        "avg_screen_time_hours": "Screen Time (hrs)",
        "avg_study_hours": "Study Hours",
        "avg_sleep_hours": "Sleep Hours",
        "avg_stress_level": "Stress Level",
        "avg_focus_score": "Focus Score"
    }

    rows = []
    for key, label in labels.items():
        hist_val = march_hist[key]
        now_val = march_now[key]
        delta = now_val - hist_val
        arrow = "↑" if delta > 0 else "↓"
        better_is_higher = key not in ["avg_stress_level", "avg_screen_time_hours"]
        good = (delta > 0 and better_is_higher) or (delta < 0 and not better_is_higher)
        rows.append({
            "Metric": label,
            "Previous March Avg": f"{hist_val:.2f}",
            "March 2026 Avg": f"{now_val:.2f}",
            "Change": f"{arrow} {abs(delta):.2f}",
            "Direction": "✅ Better" if good else ("⚠️ Watch" if abs(delta) < 0.3 else "🔴 Worse")
        })

    compare_df = pd.DataFrame(rows)
    st.dataframe(compare_df, use_container_width=True, hide_index=True)

    st.divider()

    # --- VIZ 6: Stacked area — screen time composition over 3 years ---
    st.subheader("📊 Visualization 6 — Screen Time Composition Over 3 Years")
    st.caption("Stacked area chart · Source: parami_digital_summary_3years.csv")

    area_df = filtered_monthly.copy()
    area_df["entertainment_hours"] = (
        area_df["avg_screen_time_hours"]
        - area_df["avg_productive_screen_time"]
        - area_df["avg_social_media_hours"]
    ).clip(lower=0)

    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=area_df["period"], y=area_df["avg_productive_screen_time"],
        name="Productive", stackgroup="one", fillcolor="rgba(47,158,68,0.6)",
        line=dict(color="rgba(47,158,68,0.8)")
    ))
    fig_area.add_trace(go.Scatter(
        x=area_df["period"], y=area_df["avg_social_media_hours"],
        name="Social Media", stackgroup="one", fillcolor="rgba(247,103,7,0.5)",
        line=dict(color="rgba(247,103,7,0.7)")
    ))
    fig_area.add_trace(go.Scatter(
        x=area_df["period"], y=area_df["entertainment_hours"],
        name="Entertainment / Gaming", stackgroup="one", fillcolor="rgba(76,110,245,0.4)",
        line=dict(color="rgba(76,110,245,0.6)")
    ))
    fig_area.update_layout(
        height=380,
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        yaxis_title="Hours per day",
        legend=dict(orientation="h", y=1.05),
        hovermode="x unified"
    )
    st.plotly_chart(fig_area, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Key insight:</b> Productive screen time has grown as a share of total screen time since Year 2,
    even as total hours increased. This suggests better intentionality — not just more screen time overall.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- VIZ 7: Dominant app donut ---
    st.subheader("🍩 Visualization 7 — Dominant App Category (3-Year Distribution)")
    st.caption("Donut chart · Source: parami_digital_summary_3years.csv")

    app_dist = filtered_monthly["dominant_app_category"].value_counts().reset_index()
    app_dist.columns = ["App Category", "Months Dominant"]
    fig_donut = px.pie(
        app_dist, values="Months Dominant", names="App Category",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_traces(textinfo="label+percent")
    fig_donut.update_layout(height=340, showlegend=True)

    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col_d2:
        st.markdown("""
        **What this shows:**
        - Months dominated by **Study Tools** correlate with higher productivity scores
        - **YouTube Shorts** dominance clusters in summer and exam-stress months
        - The shift toward Study Tools over time reflects intentional habit change

        Use the semester filter in the sidebar to see how this changes year by year.
        """)


# ─────────────────────────────────────────
# PAGE: DECISION MAKING
# ─────────────────────────────────────────
elif page == "🎯 Decision-Making":
    st.title("🎯 What Should I Do Differently?")
    st.markdown("Evidence-based decisions supported directly by the data — with honest limitations stated.")

    st.markdown("""
    ### Based on my data, here are 3 decisions I will make:

    ---
    **Decision 1 — Protect weekday study blocks**

    The scatter plot (March 2026) shows that weekday study sessions consistently produce
    higher productivity scores than equivalent weekend sessions. I will block 3–4 hour
    study windows on Tuesday–Thursday, as these are my highest-focus days per the heatmap.

    *Limitation: March 2026 is one month of data. Correlation ≠ causation — external factors
    (deadlines, energy levels) also drive productivity.*

    ---
    **Decision 2 — Cut social media below 2 hrs/day during exams**

    The grouped bar chart shows social media hours spike during April (a recurring burnout month).
    In months where study hours > social media hours, productivity scores average 0.8 points higher.

    *Limitation: My social media tracking is self-reported and may under-count passive scrolling.*

    ---
    **Decision 3 — Eliminate late-night phone use on class nights**

    The March 2026 data shows late-night usage days average 0.6 fewer sleep hours, and sleep
    strongly correlates with next-day focus score. Class days (Mon, Wed) are the most affected.

    *Limitation: Dataset is 31 days — too small to generalize. Results may differ in higher-stress months.*
    """)

    # Supporting chart for decision 1
    st.divider()
    st.subheader("Supporting Evidence: Sleep vs Focus Score")

    fig_sleep = px.scatter(
        df_daily, x="sleep_hours", y="focus_score",
        color="late_night_usage",
        trendline="ols",
        labels={"sleep_hours": "Sleep Hours", "focus_score": "Focus Score (1–10)", "late_night_usage": "Late Night Use"},
        color_discrete_map={"Yes": "#F03E3E", "No": "#2F9E44"}
    )
    fig_sleep.update_layout(height=350)
    st.plotly_chart(fig_sleep, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    More sleep = higher focus score, especially on non-late-night nights (green). 
    Late-night usage (red) clusters in the lower-sleep, lower-focus quadrant.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# PAGE: ETHICS & RESPONSIBILITY
# ─────────────────────────────────────────
elif page == "⚖️ Ethics & Responsibility":
    st.title("⚖️ Ethics & Responsibility")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔒 Privacy Statement")
        st.markdown("""
        <div class="ethics-box">
        <b>What data is included?</b><br>
        Daily behavioral patterns (screen time, study hours, mood, sleep) and monthly aggregates over 3 years.
        <br><br>
        <b>What is anonymized?</b><br>
        No real names of people appear in the dataset. App categories replace specific app names.
        Location, device identifiers, and account details are excluded. Internship and class context
        is represented only as binary flags (yes/no), not institution names.
        <br><br>
        <b>Who collected the data?</b><br>
        All data was self-collected and self-reported by the student. No third-party tracking tools were used.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📊 Visualization Justification")
        st.markdown("""
        <div class="ethics-box">
        <b>Line chart (3-year trend):</b> Best for continuous time-series data. Risk: gaps between months
        may imply continuity where data was not collected — viewer should note academic calendar gaps.<br><br>
        <b>Scatter plot (study vs productivity):</b> Appropriate for showing correlation. Risk: trendlines 
        may imply causation. OLS line is statistical only — does not prove study hours cause productivity.<br><br>
        <b>Heatmap (daily calendar):</b> Effective for showing day-of-week patterns. Risk: missing days
        (due to filtering) appear as blank cells, which could be misread as "zero" rather than "no data."<br><br>
        <b>Donut chart (app dominance):</b> Suitable for a small number of categories (4–6). Risk: 
        "dominant app" is one data point per month and may not reflect actual time split within the month.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("⚠️ Bias & Limitation Disclosure")
        st.markdown("""
        <div class="ethics-box">
        <b>Memory bias:</b> Scores like "productivity" and "mood" are self-rated at end of day. 
        Recency bias means events in the evening may disproportionately influence the daily score.<br><br>
        <b>Small dataset:</b> 31 daily observations (March 2026) is too small for statistically 
        significant conclusions. Patterns observed may not hold in other months.<br><br>
        <b>Subjective scoring:</b> A "7/10" productivity day for me in Year 1 may not equal
        a "7/10" in Year 3 — scoring standards drift over time.<br><br>
        <b>Social desirability bias:</b> Knowing the data would be analyzed may have led to
        unconsciously favorable self-reporting.<br><br>
        <b>Missing data:</b> Internship commitment level is NaN for Year 1 (no internship yet).
        Charts using this field are limited to Year 2 onward.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🎯 Responsible Decision Disclosure")
        st.markdown("""
        <div class="ethics-box">
        Decisions presented in this dashboard are based on patterns in a small, single-person dataset.
        They should not be generalized to other students or used as prescriptive advice.<br><br>
        <b>Limitations of each decision:</b><br>
        - Study block scheduling: only 31-day evidence base, seasonal variation not captured.<br>
        - Social media reduction: self-reported hours, correlation only — no control condition.<br>
        - Late-night usage: confounded by stress level (high-stress days cause both late-night use AND poor sleep).<br><br>
        This dashboard is an academic exploration, not a scientific study.
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.info("📌 This project was created for academic purposes. All data is personal and anonymized. No commercial use intended.")
