import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Habits & Productivity",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS & BACKGROUND ---
def set_custom_theme(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .block-container {{
                background-color: rgba(10, 15, 30, 0.85); /* Slightly darker for better readability */
                padding-top: 2rem;
                padding-bottom: 2rem;
                border-radius: 10px;
                margin-top: 2rem;
            }}
            [data-testid="stSidebar"] {{
                background-color: rgba(10, 15, 30, 0.95) !important;
                border-right: 1px solid rgba(6, 182, 212, 0.2);
            }}
            [data-testid="stMetric"] {{
                background-color: rgba(15, 23, 42, 0.9); 
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(6, 182, 212, 0.4); 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }}
            h1, h2, h3, p, .stMarkdown, .stRadio label {{
                color: #e2e8f0 !important; 
            }}
            hr {{
                border-color: rgba(6, 182, 212, 0.3) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image not found. Ensure 'assets/background.jpg' exists.")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Loading data from the data folder
    daily_df = pd.read_csv("data/digital_habits_march2026.csv")
    monthly_df = pd.read_csv("data/parami_digital_summary_3years.csv")
    
    # Process dates for the heatmap
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    daily_df['Week Number'] = daily_df['date'].dt.isocalendar().week
    
    return daily_df, monthly_df

# --- HELPER TO STYLE PLOTLY CHARTS ---
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0")
    )
    return fig

# --- MAIN APP LOGIC ---
def main():
    set_custom_theme("assets/background.jpg")
    df_daily, df_monthly = load_data()
    
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("📱 Navigation")
    page = st.sidebar.radio(
        "Select a Page:",
        ["📖 Story Overview", "📊 Daily Behavior (EDA)", "📈 Academic Trends", "⚖️ Ethics & Limitations"]
    )
    
    st.sidebar.divider()
    
    # ==========================================
    # PAGE 1: STORY OVERVIEW
    # ==========================================
    if page == "📖 Story Overview":
        st.title("📖 My 3-Year Digital Journey")
        st.markdown("A macro-level look at how my productivity and screen time have evolved throughout my university career.")
        
        # 1. LINE CHART: 3-Year Growth Story
        fig_line = px.line(
            df_monthly, 
            x="semester", 
            y="avg_productivity_score", 
            markers=True,
            title="Long-Term Productivity Growth (3 Years)",
            labels={"semester": "Academic Semester", "avg_productivity_score": "Avg Productivity (1-10)"},
            color_discrete_sequence=["#06b6d4"] # Cyan accent
        )
        st.plotly_chart(style_chart(fig_line), use_container_width=True)
        
        st.info("💡 Insight: Notice how productivity dips during the summer breaks but generally trends upward as coursework becomes more demanding in Year 3.")

    # ==========================================
    # PAGE 2: DAILY BEHAVIOR (EDA)
    # ==========================================
    elif page == "📊 Daily Behavior (EDA)":
        st.title("📊 Exploratory Data Analysis: March 2026")
        st.markdown("A micro-level look at daily habits. Use the filters below to explore the data.")
        
        # Filters
        st.sidebar.header("🔍 Filter Daily Data")
        selected_days = st.sidebar.multiselect("Select Day Type:", options=df_daily['weekday_type'].unique(), default=df_daily['weekday_type'].unique())
        max_stress = st.sidebar.slider("Maximum Stress Level:", min_value=1, max_value=10, value=10)
        
        filtered_df = df_daily[(df_daily['weekday_type'].isin(selected_days)) & (df_daily['stress_level'] <= max_stress)]
        
        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Screen Time", f"{filtered_df['total_screen_time_hours'].mean():.1f} hrs")
        c2.metric("Avg Study Hours", f"{filtered_df['study_hours'].mean():.1f} hrs")
        c3.metric("Avg Productivity", f"{filtered_df['productivity_score'].mean():.1f} / 10")
        c4.metric("Avg Stress", f"{filtered_df['stress_level'].mean():.1f} / 10")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 2. SCATTER PLOT: Study vs Productivity
            fig_scatter = px.scatter(
                filtered_df, 
                x="study_hours", 
                y="productivity_score",
                color="weekday_type",
                size="caffeine_intake_cups",
                title="Relationship: Study Hours vs. Productivity",
                labels={"study_hours": "Study Hours", "productivity_score": "Productivity Score (1-10)"},
                color_discrete_sequence=["#3b82f6", "#a855f7"] # Blue and Purple
            )
            st.plotly_chart(style_chart(fig_scatter), use_container_width=True)

        with col2:
            # 3. HEATMAP: Daily Patterns (Calendar Style)
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            fig_heat = px.density_heatmap(
                filtered_df, 
                x="day_of_week", 
                y="Week Number", 
                z="total_screen_time_hours",
                histfunc="avg",
                title="Calendar Heatmap: Screen Time Intensity",
                category_orders={"day_of_week": day_order},
                color_continuous_scale="Teal"
            )
            # Invert Y axis so Week 1 is at the top like a calendar
            fig_heat.update_yaxes(autorange="reversed")
            st.plotly_chart(style_chart(fig_heat), use_container_width=True)

    # ==========================================
    # PAGE 3: ACADEMIC TRENDS
    # ==========================================
    elif page == "📈 Academic Trends":
        st.title("📈 Academic Workload vs Digital Distractions")
        st.markdown("Comparing focused academic time against social media usage over the past 3 years.")
        
        # 4. GROUPED BAR CHART: Social Media vs Study
        fig_bar = px.bar(
            df_monthly, 
            x="semester", 
            y=["avg_study_hours", "avg_social_media_hours"],
            barmode="group",
            title="The Trade-off: Study Time vs. Social Media",
            labels={"value": "Average Hours per Day", "variable": "Activity Type", "semester": "Semester"},
            color_discrete_map={"avg_study_hours": "#06b6d4", "avg_social_media_hours": "#64748b"}
        )
        # Clean up the legend names
        newnames = {'avg_study_hours':'Study Hours', 'avg_social_media_hours': 'Social Media'}
        fig_bar.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        
        st.plotly_chart(style_chart(fig_bar), use_container_width=True)

    # ==========================================
    # PAGE 4: ETHICS & LIMITATIONS
    # ==========================================
    elif page == "⚖️ Ethics & Limitations":
        st.title("⚖️ Ethical Considerations")
        st.markdown("""
        ### 1. The Trap of Self-Reporting
        Metrics like 'productivity' and 'stress' are subjective. A highly productive day spent brainstorming offline might incorrectly appear as a "low data" day on this dashboard.
        
        ### 2. Correlation vs. Causation
        The scatter plots reveal relationships (e.g., high caffeine and high stress), but they do not prove causation. Does caffeine cause stress, or do stressful deadlines cause an increase in caffeine consumption?
        
        ### 3. Data Privacy
        Behavioral tracking contains sensitive metadata. This dashboard utilizes aggregated summaries to protect personal privacy while still communicating meaningful data science insights.
        """)

if __name__ == "__main__":
    main()
