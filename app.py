import streamlit as st
import pandas as pd
import datetime
import uuid
import os

from sentiment_analysis import analyze_sentiment, get_emotion_label, get_emotion_detail
from data_handling import save_mood_entry, load_mood_data, check_consecutive_negative_moods
from utils import get_task_recommendation, display_alert_status, get_wellness_tip
from visualizations import plot_individual_mood, plot_team_mood

# Page configuration
st.set_page_config(
    page_title="Zidio - AI Task Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state if not exists
if 'employee_id' not in st.session_state:
    # Generate a unique employee ID using uuid
    st.session_state.employee_id = str(uuid.uuid4())[:8]

if 'consecutive_negatives' not in st.session_state:
    st.session_state.consecutive_negatives = 0

if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Personal"

# Sidebar for app navigation and info
with st.sidebar:
    st.image("zidio_icon.svg", width=100)
    st.title("SentimentSync")
    st.markdown("### AI-Powered Task Optimizer")
    
    st.markdown("---")
    
    # View mode selection
    st.markdown("### View Settings")
    view_mode = st.radio("Select View Mode:", ("Personal", "Team Overview"))
    st.session_state.view_mode = view_mode
    
    st.markdown("---")
    
    
    with st.expander("How to use Zidio?"):
        st.markdown("""
        1. 📝 Share how you're feeling in the text box
        2. 🔍 Click "Analyze & Get Recommendations"
        3. 📊 View your mood analysis and task suggestions
        4. 📈 Track your mood patterns over time
        """)
    
    # About section
    with st.expander("About SentimentSync"):
        st.markdown("""
        Zidio uses AI to analyze your mood through text and recommends 
        suitable tasks to optimize your productivity and wellbeing.
        
        All data is anonymized to protect your privacy.
        """)
    
    st.markdown("---")
    st.markdown(f"Employee ID: **{st.session_state.employee_id}**")
    st.markdown("© 2025 Zidio")

# Main content
st.title("Zidio - AI Task Optimizer")
st.subheader("Analyze Your Mood and Get Task Recommendations")


with st.container():
    st.markdown("### How are you feeling today?")
    
    
    st.info(f"Your Employee ID: {st.session_state.employee_id}")
    
   
    mood_text = st.text_area("Share how are you feeling? (This helps us recommend appropriate tasks)", 
                             height=100, 
                             max_chars=500,
                             placeholder="I'm feeling...")
    
    submit_button = st.button("Analyze & Get Recommendations")

# If the submit button is clicked, analyze the mood and provide recommendations
if submit_button and mood_text:
    # Perform sentiment analysis
    sentiment_score, polarity = analyze_sentiment(mood_text)
    emotion = get_emotion_label(sentiment_score)
    
    # Extract key emotional phrases from the text (if any)
    emotion_details = get_emotion_detail(mood_text)
    
    # Get task recommendation based on sentiment
    task_recommendation = get_task_recommendation(emotion)
    
    # Save the mood entry to CSV
    timestamp = datetime.datetime.now()
    save_mood_entry(st.session_state.employee_id, timestamp, mood_text, 
                    sentiment_score, emotion)
    
    # Add to session state for mood history
    st.session_state.mood_history.append({
        'timestamp': timestamp,
        'sentiment_score': sentiment_score,
        'emotion': emotion
    })
    
    # Check for consecutive negative moods
    if emotion == "Negative":
        st.session_state.consecutive_negatives += 1
    else:
        st.session_state.consecutive_negatives = 0
    
    # Display results in an expander
    with st.expander("Analysis Results", expanded=True):
        cols = st.columns(3)
        
        # Display the detected mood
        with cols[0]:
            st.markdown("### Detected Mood")
            
            # Color code for the emotion
            if emotion == "Positive":
                st.success(f"**{emotion}** (Score: {sentiment_score:.2f})")
            elif emotion == "Neutral":
                st.info(f"**{emotion}** (Score: {sentiment_score:.2f})")
            else:
                st.error(f"**{emotion}** (Score: {sentiment_score:.2f})")
            
            # Display wellness tip
            st.markdown("### Wellness Tip")
            st.markdown(f"*{get_wellness_tip(emotion)}*")
        
        # Display the recommended tasks
        with cols[1]:
            st.markdown("### Recommended Tasks")
            st.write(task_recommendation)
            
        # Display alert status if needed
        with cols[2]:
            st.markdown("### Alert Status")
            display_alert_status(st.session_state.consecutive_negatives)

# Visualization section
st.markdown("---")
st.markdown("## Mood Visualizations")

# Load historical data for visualizations
mood_data = load_mood_data()

if not mood_data.empty:
    # Display visualizations based on the selected view mode
    if st.session_state.view_mode == "Personal":
        # Personal view - show individual mood over time and team distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Your Mood Over Time")
            # Filter data for the current employee
            individual_data = mood_data[mood_data['employee_id'] == st.session_state.employee_id]
            
            if not individual_data.empty:
                mood_fig = plot_individual_mood(individual_data)
                st.plotly_chart(mood_fig, use_container_width=True)
                
                # Add some metrics
                total_entries = len(individual_data)
                avg_sentiment = individual_data['sentiment_score'].mean()
                last_sentiment = individual_data.iloc[-1]['sentiment_score']
                
                metric_cols = st.columns(3)
                metric_cols[0].metric("Total Entries", total_entries)
                metric_cols[1].metric("Average Mood", f"{avg_sentiment:.2f}")
                metric_cols[2].metric("Latest Mood", f"{last_sentiment:.2f}", 
                                      f"{(last_sentiment - avg_sentiment):.2f}")
                
                # Add download button for personal data
                st.markdown("### Download Your Data")
                
                # Create a downloadable version of the data
                download_data = individual_data[['date', 'time', 'sentiment_score', 'emotion']]
                download_data = download_data.rename(columns={
                    'date': 'Date',
                    'time': 'Time',
                    'sentiment_score': 'Mood Score',
                    'emotion': 'Emotion'
                })
                
                # Convert to CSV for download
                csv = download_data.to_csv(index=False)
                st.download_button(
                    label="Download Your Mood History",
                    data=csv,
                    file_name="my_mood_history.csv",
                    mime="text/csv"
                )
            else:
                st.info("No mood data available yet. Submit your first mood to start tracking!")
                
        with col2:
            st.markdown("### Team Mood Distribution")
            # Check if there's enough team data to show meaningful distribution
            if len(mood_data) > 1:
                team_fig = plot_team_mood(mood_data)
                st.plotly_chart(team_fig, use_container_width=True)
            else:
                st.info("Not enough team data available for visualization.")
    
    else:  # Team Overview mode
        st.markdown("### Team Mood Overview")
        # Team Overview - show team mood distribution and trends
        
        # Date filter for team data
        today = datetime.datetime.now().date()
        last_week = today - datetime.timedelta(days=7)
        last_month = today - datetime.timedelta(days=30)
        
        time_period = st.radio(
            "Select Time Period:",
            options=["Today", "Last 7 Days", "Last 30 Days", "All Time"],
            horizontal=True
        )
        
        # Filter data based on selected time period
        if time_period == "Today":
            filtered_data = mood_data[mood_data['date'] == today.strftime('%Y-%m-%d')]
            period_title = "Today"
        elif time_period == "Last 7 Days":
            filtered_data = mood_data[mood_data['timestamp'] >= pd.Timestamp(last_week)]
            period_title = "Last 7 Days"
        elif time_period == "Last 30 Days":
            filtered_data = mood_data[mood_data['timestamp'] >= pd.Timestamp(last_month)]
            period_title = "Last 30 Days"
        else:  # All Time
            filtered_data = mood_data
            period_title = "All Time"
        
        if not filtered_data.empty:
            # Create a two-column layout for team visualizations
            team_col1, team_col2 = st.columns(2)
            
            with team_col1:
                st.markdown(f"### Team Mood Distribution ({period_title})")
                team_fig = plot_team_mood(filtered_data)
                st.plotly_chart(team_fig, use_container_width=True)
                
            with team_col2:
                st.markdown(f"### Team Stats ({period_title})")
                
                # Team stats
                total_employees = filtered_data['employee_id'].nunique()
                total_entries = len(filtered_data)
                avg_team_sentiment = filtered_data['sentiment_score'].mean()
                
                # Display team metrics
                team_metrics = st.columns(3)
                team_metrics[0].metric("Active Employees", total_employees)
                team_metrics[1].metric("Total Entries", total_entries)
                team_metrics[2].metric("Avg Team Mood", f"{avg_team_sentiment:.2f}")
                
                # Display mood counts
                mood_counts = filtered_data['emotion'].value_counts()
                st.markdown("### Mood Distribution")
                st.write(f"**Positive:** {mood_counts.get('Positive', 0)}")
                st.write(f"**Neutral:** {mood_counts.get('Neutral', 0)}")
                st.write(f"**Negative:** {mood_counts.get('Negative', 0)}")
                
                # HR Alert info
                negative_moods = filtered_data[filtered_data['emotion'] == 'Negative']['employee_id'].value_counts()
                employees_with_multiple_negative = negative_moods[negative_moods > 1].count()
                
                if employees_with_multiple_negative > 0:
                    st.warning(f"⚠️ {employees_with_multiple_negative} employees have reported multiple negative moods in this period.")
                
                # Add download button for team data (for managers/HR)
                st.markdown("### Export Team Data")
                
                # Create a downloadable version of the team data (anonymized)
                download_team_data = filtered_data[['date', 'time', 'employee_id', 'sentiment_score', 'emotion']]
                download_team_data = download_team_data.rename(columns={
                    'date': 'Date',
                    'time': 'Time',
                    'employee_id': 'Employee ID',
                    'sentiment_score': 'Mood Score',
                    'emotion': 'Emotion'
                })
                
                # Convert to CSV for download
                team_csv = download_team_data.to_csv(index=False)
                st.download_button(
                    label=f"Export Team Mood Data ({period_title})",
                    data=team_csv,
                    file_name=f"team_mood_data_{period_title.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    help="Download anonymized team mood data for analysis."
                )
        else:
            st.info(f"No mood data available for {period_title}.")
else:
    st.info("No mood data available yet. Be the first to submit your mood!")

# HR Alert System (this would trigger an email in a production system)
if st.session_state.consecutive_negatives >= 3:
    # In a production environment, this would send an email alert to HR
    st.warning("⚠️ **HR Alert**: System has detected 3 consecutive negative mood entries from employee " +
              f"{st.session_state.employee_id}. Consider checking in with this team member.")
    
    # Log the alert to the console
    print(f"ALERT: Employee {st.session_state.employee_id} has reported negative mood for 3 consecutive times.")

# Footer with helpful information
st.markdown("---")
st.markdown("""
**About SentimentSync:**  
This application helps optimize your work by recommending tasks based on your current mood.
All mood data is stored with anonymized IDs to protect your privacy.
""")
