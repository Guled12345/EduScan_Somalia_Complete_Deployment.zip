import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import os
from utils.data_utils import save_parent_observation, load_parent_observations
from utils.image_utils import get_image_html, create_image_gallery, get_student_images
from utils.educational_images import get_diverse_educational_images
from utils.image_base64 import get_base64_images, get_image_html as get_b64_image_html
from utils.language_utils import get_text, load_app_settings

# Initialize language in session state
if 'app_language' not in st.session_state:
    settings = load_app_settings()
    st.session_state['app_language'] = settings.get('language', 'English')

# Get current language
language = st.session_state.get('app_language', 'English')

st.set_page_config(
    page_title=f"{get_text('parent_tracker', language)} - EduScan",
    page_icon="⭕",
    layout="wide"
)

# CSS matching the main app design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(rgba(248, 250, 252, 0.95), rgba(248, 250, 252, 0.95)), 
                    url('data:image/jpeg;base64,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');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    .stHeader {display: none;}
    .stToolbar {display: none;}
    
    .css-1d391kg {
        background-color: white !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    .main .block-container {
        background-color: #f8fafc !important;
        padding: 1.5rem !important;
        max-width: none !important;
    }
    
    .page-header {
        background: white;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        margin: -1.5rem -1.5rem 2rem -1.5rem;
    }
    
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    .tracker-section {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }
    
    .parent-header {
        background: linear-gradient(135deg, #E91E63 0%, #FF6B35 50%, #FFD23F 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .parent-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('attached_assets/Exam-Students_1750847086459.jpg
        opacity: 0.1;
        z-index: 0;
    }
    
    .parent-header > * {
        position: relative;
        z-index: 1;
    }
    
    .family-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        margin: 1rem 0;
    }
    
    .family-showcase {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .family-card {
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .family-card:hover {
        transform: translateY(-3px);
    }
    
    .family-card img {
        width: 100%;
        height: 120px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    .highlight-text {
        background: linear-gradient(135deg, #E91E63, #FF6B35);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .tracking-form {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        margin: 1rem 0;
        border-left: 4px solid #E91E63;
    }
</style>
""", unsafe_allow_html=True)

def create_progress_chart(data, metric):
    """Create progress chart for specific metric"""
    df = pd.DataFrame(data)
    if df.empty:
        return None
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = px.line(df, x='date', y=metric, 
                  title=f"{metric.replace('_', ' ').title()} Progress Over Time",
                  markers=True)
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=metric.replace('_', ' ').title(),
        height=400
    )
    
    return fig

def create_weekly_summary(data):
    """Create weekly summary visualization"""
    if not data:
        return None, None
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.to_period('W')
    
    # Calculate weekly averages
    weekly_avg = df.groupby('week')[['homework_completion', 'behavior_rating', 'sleep_hours', 'mood_rating']].mean()
    
    # Create summary chart
    fig = go.Figure()
    
    metrics = ['homework_completion', 'behavior_rating', 'sleep_hours', 'mood_rating']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, metric in enumerate(metrics):
        fig.add_trace(go.Scatter(
            x=weekly_avg.index.astype(str),
            y=weekly_avg[metric],
            mode='lines+markers',
            name=metric.replace('_', ' ').title(),
            line=dict(color=colors[i])
        ))
    
    fig.update_layout(
        title="Weekly Progress Summary",
        xaxis_title="Week",
        yaxis_title="Score",
        height=400
    )
    
    return fig, weekly_avg

def main():
    # Page header
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{get_text('parent_tracker', language)}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Add authentic student images
    st.markdown(f"### {get_text('supporting_childs_learning', language)}")
    images = get_student_images()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(get_image_html(images['classroom_girls'], "Family Support", "100%", "200px"), unsafe_allow_html=True)
    with col2:
        st.markdown(get_image_html(images['boys_in_classroom'], "Learning Growth", "100%", "200px"), unsafe_allow_html=True)
    
    # Family showcase section with base64 images
    b64_images = get_base64_images()
    
    st.markdown(f"""
    <div class="family-section">
        <h2 class="highlight-text">{get_b64_image_html(b64_images['strengthening_connections'], "Strengthening Home-School Connections", "100%", "80px")}</h2>
        <div class="family-showcase">
            <div class="family-card">
                {get_b64_image_html(b64_images['daily_tracking'], "Family learning", "100%", "150px")}
                <h4>{get_text('daily_tracking', language)}</h4>
                <p>{get_text('monitor_child_progress', language)}</p>
            </div>
            <div class="family-card">
                {get_b64_image_html(b64_images['parent_empowerment'], "Parent support", "100%", "150px")}
                <h4>{get_text('parent_empowerment', language)}</h4>
                <p>{get_text('gain_insights_strategies', language)}</p>
            </div>
            <div class="family-card">
                {get_b64_image_html(b64_images['school_partnership'], "Family collaboration", "100%", "150px")}
                <h4>{get_text('school_partnership', language)}</h4>
                <p>{get_text('build_communication_bridges', language)}</p>
            </div>
            <div class="family-card">
                {get_b64_image_html(b64_images['student_progress_1'], "Student success", "100%", "150px")}
                <h4>{get_text('student_success', language)}</h4>
                <p>{get_text('celebrate_achievements', language)}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add student progress gallery
    st.markdown(f"### {get_text('student_progress_stories', language)}")
    images = get_student_images()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(get_image_html(images['teacher_with_students'], "Academic Progress", "100%", "170px"), unsafe_allow_html=True)
    with col2:
        st.markdown(get_image_html(images['happy_young_students'], "Learning Joy", "100%", "170px"), unsafe_allow_html=True)
    with col3:
        st.markdown(get_image_html(images['classroom_girls'], "Study Focus", "100%", "170px"), unsafe_allow_html=True)
    
    # Sidebar for child selection and navigation
    with st.sidebar:
        st.markdown(f"### {get_text('child_selection', language)}")
        child_name = st.text_input(get_text('child_name', language), placeholder="Enter child's name")
        
        if child_name:
            st.success(f"{get_text('tracking', language)}: {child_name}")
        
        st.markdown(f"### {get_text('dashboard_options', language)}")
        dashboard_view = st.selectbox(
            get_text('choose_view', language),
            [get_text('daily_entry', language), get_text('progress_tracking', language), get_text('weekly_summary', language), get_text('observations_log', language)]
        )
        
        # Date range for analysis
        if dashboard_view in ["Progress Tracking", "Weekly Summary"]:
            st.markdown("### Date Range")
            end_date = st.date_input("End Date", value=date.today())
            start_date = st.date_input("Start Date", value=end_date - timedelta(days=30))

    if not child_name:
        st.warning(get_text('please_enter_child_name', language))
        st.stop()

    if dashboard_view == get_text('daily_entry', language):
        st.markdown(f"## {get_text('daily_observation_entry', language)}")
        st.markdown(f"{get_text('recording_observations_for', language)} **{child_name}** {get_text('on', language)} {date.today().strftime('%B %d, %Y')}")
        
        # Create form for daily entry
        with st.form("daily_observation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {get_text('academic_observations', language)}")
                
                homework_completion = st.slider(
                    "Homework Completion (%)", 
                    0, 100, 75,
                    help="Percentage of assigned homework completed"
                )
                
                reading_time = st.number_input(
                    "Reading Time (minutes)", 
                    min_value=0, max_value=180, value=20,
                    help="Minutes spent reading independently"
                )
                
                focus_level = st.select_slider(
                    "Focus During Homework",
                    options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                    value="Good"
                )
                
                subjects_struggled = st.multiselect(
                    "Subjects with Difficulties",
                    ["Math", "Reading", "Writing", "Science", "Social Studies", "Other"],
                    help="Select subjects where child struggled today"
                )
            
            with col2:
                st.markdown(f"### {get_text('behavioral_emotional', language)}")
                
                behavior_rating = st.select_slider(
                    "Overall Behavior", 
                    options=["1 - Challenging", "2 - Below Average", "3 - Average", "4 - Good", "5 - Excellent"],
                    value="3 - Average",
                    help="Select your child's overall behavior today"
                )
                behavior_value = int(behavior_rating.split(' ')[0])  # Extract number for calculations
                
                mood_rating = st.select_slider(
                    "Mood/Emotional State", 
                    options=["1 - Very Upset", "2 - Upset", "3 - Neutral", "4 - Happy", "5 - Very Happy"],
                    value="3 - Neutral",
                    help="How was your child's mood today?"
                )
                mood_value = int(mood_rating.split(' ')[0])  # Extract number for calculations
                
                sleep_hours = st.number_input(
                    "Hours of Sleep", 
                    min_value=4.0, max_value=12.0, value=8.0, step=0.5,
                    help="Total hours of sleep last night"
                )
                
                energy_level = st.select_slider(
                    "Energy Level",
                    options=["Very Low", "Low", "Normal", "High", "Very High"],
                    value="Normal"
                )
            
            st.markdown("### List Additional Observations")
            
            col3, col4 = st.columns(2)
            
            with col3:
                social_interactions = st.text_area(
                    "Social Interactions",
                    placeholder="How did your child interact with siblings, friends, or family today?",
                    height=100
                )
                
                learning_wins = st.text_area(
                    "Learning Wins/Successes",
                    placeholder="What went well today? Any breakthroughs or positive moments?",
                    height=100
                )
            
            with col4:
                challenges_faced = st.text_area(
                    "Challenges Faced",
                    placeholder="What was difficult today? Any specific struggles or concerns?",
                    height=100
                )
                
                strategies_used = st.text_area(
                    "Strategies That Helped",
                    placeholder="What strategies or supports helped your child today?",
                    height=100
                )
            
            # Environmental factors
            st.markdown("### Home Environmental Factors")
            
            col5, col6 = st.columns(2)
            
            with col5:
                screen_time = st.number_input(
                    "Screen Time (hours)", 
                    min_value=0.0, max_value=12.0, value=2.0, step=0.5
                )
                
                physical_activity = st.number_input(
                    "Physical Activity (minutes)", 
                    min_value=0, max_value=300, value=60
                )
            
            with col6:
                medication_taken = st.checkbox("Medication taken as prescribed")
                
                special_events = st.text_input(
                    "Special Events/Changes",
                    placeholder="Any unusual events, schedule changes, or disruptions?"
                )
            
            # Submit button
            submitted = st.form_submit_button(" Save Daily Observation", type="primary")
            
            if submitted:
                # Prepare observation data
                observation_data = {
                    "child_name": child_name,
                    "date": date.today().isoformat(),
                    "homework_completion": homework_completion,
                    "reading_time": reading_time,
                    "focus_level": focus_level,
                    "subjects_struggled": subjects_struggled,
                    "behavior_rating": behavior_value,
                    "mood_rating": mood_value,
                    "sleep_hours": sleep_hours,
                    "energy_level": energy_level,
                    "social_interactions": social_interactions,
                    "learning_wins": learning_wins,
                    "challenges_faced": challenges_faced,
                    "strategies_used": strategies_used,
                    "screen_time": screen_time,
                    "physical_activity": physical_activity,
                    "medication_taken": medication_taken,
                    "special_events": special_events,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Save the observation
                save_parent_observation(observation_data)
                st.success(" Daily observation saved successfully!")
                st.balloons()

    elif dashboard_view == "Progress Tracking":
        st.markdown("## Growth Progress Tracking")
        st.markdown(f"Analyzing progress for **{child_name}** from {start_date} to {end_date}")
        
        # Load observations for the child
        all_observations = load_parent_observations()
        child_observations = [obs for obs in all_observations 
                            if obs.get('child_name') == child_name 
                            and start_date <= date.fromisoformat(obs['date']) <= end_date]
        
        if not child_observations:
            st.warning("Chart No observations found for the selected date range. Start by adding daily observations!")
            return
        
        # Create tabs for different metrics
        tab1, tab2, tab3, tab4 = st.tabs(["Academic", "Behavioral", "Emotional", "Health"])
        
        with tab1:
            st.markdown("### Academic Progress")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Homework completion chart
                homework_fig = create_progress_chart(child_observations, 'homework_completion')
                if homework_fig:
                    st.plotly_chart(homework_fig, use_container_width=True)
            
            with col2:
                # Reading time chart
                reading_fig = create_progress_chart(child_observations, 'reading_time')
                if reading_fig:
                    st.plotly_chart(reading_fig, use_container_width=True)
            
            # Subject struggles analysis
            st.markdown("#### Chart Subject Difficulty Analysis")
            
            all_subjects = []
            for obs in child_observations:
                all_subjects.extend(obs.get('subjects_struggled', []))
            
            if all_subjects:
                subject_counts = pd.Series(all_subjects).value_counts()
                fig_subjects = px.bar(x=subject_counts.index, y=subject_counts.values,
                                    title="Subjects with Most Difficulties",
                                    labels={'x': 'Subject', 'y': 'Number of Days'})
                st.plotly_chart(fig_subjects, use_container_width=True)
            else:
                st.info("Great news! No subject difficulties recorded in this period.")
        
        with tab2:
            st.markdown("### Behavioral Progress")
            
            behavior_fig = create_progress_chart(child_observations, 'behavior_rating')
            if behavior_fig:
                st.plotly_chart(behavior_fig, use_container_width=True)
            
            # Behavior statistics
            df = pd.DataFrame(child_observations)
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_behavior = df['behavior_rating'].mean()
                    st.metric("Average Behavior Rating", f"{avg_behavior:.1f}/5")
                
                with col2:
                    good_days = len(df[df['behavior_rating'] >= 4])
                    st.metric("Good Behavior Days", f"{good_days}/{len(df)}")
                
                with col3:
                    improvement = df['behavior_rating'].diff().mean()
                    st.metric("Trend", f"{improvement:+.2f}", delta=f"{improvement:.2f}")
        
        with tab3:
            st.markdown("### Emotional Well-being")
            
            mood_fig = create_progress_chart(child_observations, 'mood_rating')
            if mood_fig:
                st.plotly_chart(mood_fig, use_container_width=True)
            
            # Mood analysis
            df = pd.DataFrame(child_observations)
            if not df.empty:
                mood_dist = df['mood_rating'].value_counts().sort_index()
                fig_mood_dist = px.pie(values=mood_dist.values, names=[f"Mood {i}" for i in mood_dist.index],
                                     title="Mood Distribution")
                st.plotly_chart(fig_mood_dist, use_container_width=True)
        
        with tab4:
            st.markdown("### Health & Lifestyle")
            
            col1, col2 = st.columns(2)
            
            with col1:
                sleep_fig = create_progress_chart(child_observations, 'sleep_hours')
                if sleep_fig:
                    st.plotly_chart(sleep_fig, use_container_width=True)
            
            with col2:
                activity_fig = create_progress_chart(child_observations, 'physical_activity')
                if activity_fig:
                    st.plotly_chart(activity_fig, use_container_width=True)
            
            # Health summary
            df = pd.DataFrame(child_observations)
            if not df.empty:
                st.markdown("#### Chart Health Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_sleep = df['sleep_hours'].mean()
                    st.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
                
                with col2:
                    avg_activity = df['physical_activity'].mean()
                    st.metric("Average Activity", f"{avg_activity:.0f} min")
                
                with col3:
                    avg_screen = df['screen_time'].mean()
                    st.metric("Average Screen Time", f"{avg_screen:.1f} hrs")
                
                with col4:
                    med_compliance = df['medication_taken'].mean() * 100
                    st.metric("Medication Compliance", f"{med_compliance:.0f}%")

    elif dashboard_view == "Weekly Summary":
        st.markdown("## Weekly Summary")
        st.markdown(f"Weekly analysis for **{child_name}**")
        
        # Load observations
        all_observations = load_parent_observations()
        child_observations = [obs for obs in all_observations 
                            if obs.get('child_name') == child_name 
                            and start_date <= date.fromisoformat(obs['date']) <= end_date]
        
        if not child_observations:
            st.warning("Chart No observations found for the selected date range.")
            return
        
        # Create weekly summary chart
        weekly_fig, weekly_data = create_weekly_summary(child_observations)
        
        if weekly_fig:
            st.plotly_chart(weekly_fig, use_container_width=True)
            
            # Weekly insights
            st.markdown("### 💡 Weekly Insights")
            
            if weekly_data is not None and not weekly_data.empty:
                latest_week = weekly_data.iloc[-1]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### This Week's Highlights")
                    
                    if latest_week['homework_completion'] >= 80:
                        st.success(" Great homework completion!")
                    elif latest_week['homework_completion'] >= 60:
                        st.warning("️ Homework completion needs attention")
                    else:
                        st.error("Homework completion is concerning")
                    
                    if latest_week['behavior_rating'] >= 4:
                        st.success(" Excellent behavior this week!")
                    elif latest_week['behavior_rating'] >= 3:
                        st.info("ℹ️ Good behavior overall")
                    else:
                        st.warning("️ Behavior needs support")
                
                with col2:
                    st.markdown("#### Growth Areas of Growth")
                    
                    if len(weekly_data) > 1:
                        prev_week = weekly_data.iloc[-2]
                        
                        homework_change = latest_week['homework_completion'] - prev_week['homework_completion']
                        behavior_change = latest_week['behavior_rating'] - prev_week['behavior_rating']
                        mood_change = latest_week['mood_rating'] - prev_week['mood_rating']
                        
                        if homework_change > 5:
                            st.success("Homework completion improved!")
                        if behavior_change > 0.2:
                            st.success("Behavior rating improved!")
                        if mood_change > 0.2:
                            st.success("Mood has improved!")

    else:  # Observations Log
        st.markdown("## Observations Log")
        st.markdown(f"Complete observation history for **{child_name}**")
        
        # Load all observations for the child
        all_observations = load_parent_observations()
        child_observations = [obs for obs in all_observations if obs.get('child_name') == child_name]
        
        if not child_observations:
            st.warning("Note No observations recorded yet. Start by adding daily observations!")
            return
        
        # Sort by date (newest first)
        child_observations.sort(key=lambda x: x['date'], reverse=True)
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            date_filter = st.date_input("Filter by date (optional)")
        
        with col2:
            show_detailed = st.checkbox("Show detailed observations", value=False)
        
        # Display observations
        for obs in child_observations[:20]:  # Show last 20 observations
            obs_date = date.fromisoformat(obs['date'])
            
            if date_filter and obs_date != date_filter:
                continue
            
            with st.expander(f"{obs_date.strftime('%B %d, %Y')} - Rating: {obs['behavior_rating']}/5"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Academic**")
                    st.write(f"Homework: {obs['homework_completion']}%")
                    st.write(f"Reading: {obs['reading_time']} min")
                    st.write(f"Focus: {obs.get('focus_level', 'N/A')}")
                    if obs.get('subjects_struggled'):
                        st.write(f"Struggled with: {', '.join(obs['subjects_struggled'])}")
                
                with col2:
                    st.markdown("**Behavioral**")
                    st.write(f"Behavior: {obs['behavior_rating']}/5")
                    st.write(f"Mood: {obs['mood_rating']}/5")
                    st.write(f"Energy: {obs.get('energy_level', 'N/A')}")
                
                with col3:
                    st.markdown("**Health**")
                    st.write(f"Sleep: {obs['sleep_hours']} hrs")
                    st.write(f"Activity: {obs['physical_activity']} min")
                    st.write(f"Screen time: {obs['screen_time']} hrs")
                
                if show_detailed:
                    if obs.get('learning_wins'):
                        st.markdown("**Learning Wins:**")
                        st.write(obs['learning_wins'])
                    
                    if obs.get('challenges_faced'):
                        st.markdown("**Challenges:**")
                        st.write(obs['challenges_faced'])
                    
                    if obs.get('strategies_used'):
                        st.markdown("**🛠️ Helpful Strategies:**")
                        st.write(obs['strategies_used'])
                    
                    if obs.get('social_interactions'):
                        st.markdown("**Group Social Interactions:**")
                        st.write(obs['social_interactions'])
        
        # Export option
        if st.button("📥 Export Observations"):
            df_export = pd.DataFrame(child_observations)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{child_name}_observations_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    # Footer with tips
    st.markdown("---")
    st.markdown("### 💡 Parent Tracking Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Effective Tracking:**
        - Record observations consistently each day
        - Be specific about challenges and successes
        - Note what strategies work best
        - Track patterns over time, not just individual days
        """)
    
    with col2:
        st.markdown("""
        **📞 When to Seek Help:**
        - Consistent low behavior/mood ratings
        - Persistent homework struggles
        - Sleep or health concerns
        - Significant changes in patterns
        """)

if __name__ == "__main__":
    main()
