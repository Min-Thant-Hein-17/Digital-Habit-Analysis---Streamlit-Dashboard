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
                background-color: rgba(10, 15, 30, 0.85); 
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
    daily_df = pd.read_csv("data/digital_habits_march2026.csv")
    monthly_df = pd.read_csv("data/parami_digital_summary_3years.csv")
    
    # Ensure days of the week are sorted logically for charts, not alphabetically
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily_df['day_of_week'] = pd.Categorical(daily_df['day_of_week'], categories=day_order, ordered=True)
    
    return daily_df, monthly_df

# --- HELPER TO STYLE PLOTLY CHARTS ---
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font_size=20 # Makes the simple titles stand out
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
        ["📖 Story Overview", "📊 Daily Habits (March)", "📈 Long-Term Trends", "⚖️ Ethics & Limitations"]
    )
    
    st.sidebar.divider()
    
    # ==========================================
    # PAGE 1: STORY OVERVIEW
    # ==========================================
    if page == "📖 Story Overview":
        st.title("📖 My 3-Year Digital Journey")
        st.markdown("A macro-level look at how my productivity has evolved since I started university.")
        
        # 1. LINE CHART: Simple and direct
        fig_line = px.line(
            df_monthly, 
            x="semester", 
            y="avg_productivity_score", 
            markers=True,
            title="How My Productivity Changed Over 3 Years",
            labels={"semester": "Academic Timeline", "avg_productivity_score": "Self-Rated Productivity (out of 10)"},
            color_discrete_sequence=["#06b6d4"] 
        )
        st.plotly_chart(style_chart(fig_line), use_container_width=True)
        
        st.info("💡 Insight: Notice the pattern! Productivity drops during summer breaks but climbs steadily as the coursework gets harder.")

    # ==========================================
    # PAGE 2: DAILY BEHAVIOR (EDA) - SIMPLIFIED
    # ==========================================
    elif page == "📊 Daily Habits (March)":
        st.title("📊 My Daily Habits (March 2026)")
        st.markdown("What does a typical day look like for me right now?")
        
        # Filters
        st.sidebar.header("🔍 Filter Data")
        selected_days = st.sidebar.multiselect("Select Day Type:", options=df_daily['weekday_type'].unique(), default=df_daily['weekday_type'].unique())
        
        filtered_df = df_daily[df_daily['weekday_type'].isin(selected_days)]
        
        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Screen Time", f"{filtered_df['total_screen_time_hours'].mean():.1f} hrs")
        c2.metric("Avg Study Hours", f"{filtered_df['study_hours'].mean():.1f} hrs")
        c3.metric("Avg Productivity", f"{filtered_df['productivity_score'].mean():.1f} / 10")
        c4.metric("Avg Stress", f"{filtered_df['stress_level'].mean():.1f} / 10")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 2. BAR CHART: Easy to read comparison across days
            # Grouping the data to get the average screen time per day
            avg_screen_time = filtered_df.groupby('day_of_week')['total_screen_time_hours'].mean().reset_index()
            
            fig_bar_days = px.bar(
                avg_screen_time, 
                x="day_of_week", 
                y="total_screen_time_hours",
                title="Which Days Do I Look at Screens the Most?",
                labels={"day_of_week": "", "total_screen_time_hours": "Average Hours"},
                color_discrete_sequence=["#3b82f6"]
            )
            st.plotly_chart(style_chart(fig_bar_days), use_container_width=True)

        with col2:
            # 3. DONUT CHART: Replaces the complex heatmap. Everyone understands proportions.
            app_usage = filtered_df['most_used_app_category'].value_counts().reset_index()
            app_usage.columns = ['App Category', 'Days as Most Used']
            
            fig_donut = px.pie(
                app_usage, 
                names="App Category", 
                values="Days as Most Used",
                hole=0.4, # Makes it a modern donut chart instead of a standard pie chart
                title="Where Does My Digital Time Go?",
                color_discrete_sequence=px.colors.sequential.Teal
            )
            # Make the labels simple and clean
            fig_donut.update_traces(textinfo='percent+label', showlegend=False)
            st.plotly_chart(style_chart(fig_donut), use_container_width=True)

    # ==========================================
    # PAGE 3: ACADEMIC TRENDS - CLEAR LEGENDS
    # ==========================================
    elif page == "📈 Long-Term Trends":
        st.title("📈 Academic Workload vs. Distractions")
        st.markdown("Comparing focused study time against social media scrolling over the past 3 years.")
        
        # 4. GROUPED BAR CHART: Clearer labels
        fig_bar_trends = px.bar(
            df_monthly, 
            x="semester", 
            y=["avg_study_hours", "avg_social_media_hours"],
            barmode="group",
            title="The Trade-off: Study Time vs. Social Media",
            labels={"value": "Hours per Day", "variable": "Activity Type", "semester": ""},
            color_discrete_map={"avg_study_hours": "#06b6d4", "avg_social_media_hours": "#64748b"}
        )
        # Clean up the legend names for the audience
        newnames = {'avg_study_hours':'Focused Study Time', 'avg_social_media_hours': 'Social Media & Scrolling'}
        fig_bar_trends.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        
        st.plotly_chart(style_chart(fig_bar_trends), use_container_width=True)

    # ==========================================
    # PAGE 4: ETHICS & LIMITATIONS
    # ==========================================
    elif page == "⚖️ Ethics & Limitations":
        st.title("⚖️ Ethical Considerations")
        st.markdown("""
        ### 1. The Trap of Self-Reporting
        Metrics like 'productivity' and 'stress' are subjective. A highly productive day spent brainstorming offline might incorrectly appear as a "lazy" day on this dashboard if screen time was low.
        
        ### 2. Correlation vs. Causation
        The charts show trends, but they don't prove causation. For example, does caffeine cause stress, or do stressful deadlines cause me to drink more caffeine?
        
        ### 3. Data Privacy
        Behavioral tracking contains sensitive metadata. This dashboard utilizes aggregated summaries to protect my privacy while still sharing meaningful insights.
        """)

if __name__ == "__main__":
    main()
