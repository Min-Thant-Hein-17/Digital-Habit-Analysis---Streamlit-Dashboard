import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pyngrok import ngrok

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Habits & Productivity",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NGROK TUNNEL SETUP ---
def setup_ngrok():
    # Replace this string with your actual ngrok token when running locally
    NGROK_TOKEN = "PASTE_NGROK_TOKEN_HERE" 
    
    if NGROK_TOKEN != "PASTE_NGROK_TOKEN_HERE":
        try:
            ngrok.set_auth_token(NGROK_TOKEN)
            public_url = ngrok.connect(8501).public_url
            st.sidebar.success(f"🌐 App is live at: [Click Here]({public_url})")
        except Exception as e:
            st.sidebar.error("Failed to connect to ngrok. Check terminal.")
    else:
        st.sidebar.warning("Ngrok token not set. Running on localhost only.")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    daily_df = pd.read_csv("data/digital_habits_march2026.csv")
    monthly_df = pd.read_csv("data/parami_digital_summary_3years.csv")
    return daily_df, monthly_df

# --- MAIN APP LOGIC ---
def main():
    setup_ngrok()
    
    # Load datasets
    df_daily, df_monthly = load_data()
    
    # --- HEADER ---
    st.title("📱 Digital Habit Analysis: Screen Time vs. Productivity")
    st.markdown("""
    Welcome to my final project dashboard. This tool analyzes my personal digital habits, comparing micro-level daily behaviors with macro-level academic trends. 
    Use the sidebar to filter the data and explore the relationships between screen time, stress, and focus.
    """)
    st.divider()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔍 Filter Daily Data")
    
    # Weekday/Weekend Filter
    day_types = df_daily['weekday_type'].unique()
    selected_days = st.sidebar.multiselect(
        "Select Day Type:", 
        options=day_types,
        default=day_types
    )
    
    # Stress Level Slider
    max_stress = st.sidebar.slider(
        "Maximum Stress Level:", 
        min_value=int(df_daily['stress_level'].min()), 
        max_value=int(df_daily['stress_level'].max()), 
        value=int(df_daily['stress_level'].max())
    )

    # Apply Filters
    filtered_df = df_daily[
        (df_daily['weekday_type'].isin(selected_days)) & 
        (df_daily['stress_level'] <= max_stress)
    ]

    # --- METRIC CARDS ---
    st.subheader("📊 Summary Metrics (Filtered)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Screen Time", f"{filtered_df['total_screen_time_hours'].mean():.1f} hrs")
    with col2:
        st.metric("Avg Productivity", f"{filtered_df['productivity_score'].mean():.1f} / 10")
    with col3:
        st.metric("Avg Sleep", f"{filtered_df['sleep_hours'].mean():.1f} hrs")
    with col4:
        st.metric("Avg Focus Score", f"{filtered_df['focus_score'].mean():.1f} / 10")

    st.divider()

    # --- VISUALIZATIONS ---
    st.subheader("📈 Exploratory Visualizations")
    col_left, col_right = st.columns(2)

    with col_left:
        # Scatter Plot: Screen Time vs Productivity
        fig_scatter = px.scatter(
            filtered_df, 
            x="total_screen_time_hours", 
            y="productivity_score",
            color="weekday_type",
            size="caffeine_intake_cups",
            hover_data=["most_used_app_category"],
            title="Does screen time impact productivity?",
            labels={
                "total_screen_time_hours": "Total Screen Time (Hours)",
                "productivity_score": "Self-Reported Productivity (1-10)"
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_right:
        # Bar Chart: App Categories
        app_counts = filtered_df['most_used_app_category'].value_counts().reset_index()
        app_counts.columns = ['Category', 'Days Dominant']
        fig_bar = px.bar(
            app_counts, 
            x="Category", 
            y="Days Dominant", 
            color="Category",
            title="Most Frequent App Categories",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # --- ETHICS SECTION ---
    st.divider()
    st.subheader("⚖️ Ethical Considerations & Limitations")
    st.markdown("""
    * **Self-Reporting Bias:** Metrics like 'productivity' and 'mood' are subjective and self-reported, which introduces natural human bias.
    * **Correlation vs. Causation:** While the scatter plots may show relationships (e.g., high caffeine and high stress), we cannot definitively prove which variable causes the other.
    * **Privacy:** Behavioral tracking data carries inherent privacy risks. This dataset has been securely managed and aggregated for academic purposes.
    """)

if __name__ == "__main__":
    main()
