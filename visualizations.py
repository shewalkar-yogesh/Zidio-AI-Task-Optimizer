import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

def plot_individual_mood(individual_data):
    """
    Create a line chart showing an individual's mood over time.
    
    Args:
        individual_data (DataFrame): Data for a specific employee
        
    Returns:
        Figure: Plotly figure object
    """
    # Ensure data is sorted by timestamp
    data = individual_data.sort_values('timestamp')
    
    # Create a line chart
    fig = px.line(
        data,
        x='timestamp',
        y='sentiment_score',
        labels={'timestamp': 'Date/Time', 'sentiment_score': 'Mood Score'},
        title='Your Mood Trend',
        markers=True
    )
    
    # Add reference lines and annotations
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=0.75,
        x1=data['timestamp'].max(),
        y1=0.75,
        line=dict(color="green", width=1, dash="dash"),
    )
    
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=0.45,
        x1=data['timestamp'].max(),
        y1=0.45,
        line=dict(color="orange", width=1, dash="dash"),
    )
    
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=0.25,
        x1=data['timestamp'].max(),
        y1=0.25,
        line=dict(color="red", width=1, dash="dash"),
    )
    
    # Add annotations to explain the zones
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=0.87,
        text="Positive",
        showarrow=False,
        font=dict(color="green")
    )
    
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=0.35,
        text="Neutral",
        showarrow=False,
        font=dict(color="orange")
    )
    
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=0.12,
        text="Negative",
        showarrow=False,
        font=dict(color="red")
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date/Time",
        yaxis_title="Mood Score",
        yaxis=dict(range=[0, 1]),
        hovermode="x unified"
    )
    
    return fig

def plot_team_mood(mood_data):
    """
    Create a chart showing team mood distribution.
    
    Args:
        mood_data (DataFrame): Mood data for all employees
        
    Returns:
        Figure: Plotly figure object
    """
    # Get only recent data (last 7 days)
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    
    # Convert timestamp to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(mood_data['timestamp']):
        mood_data['timestamp'] = pd.to_datetime(mood_data['timestamp'])
    
    recent_data = mood_data[mood_data['timestamp'] >= week_ago]
    
    if recent_data.empty:
        recent_data = mood_data  # Use all data if no recent data
    
    # Get mood distribution
    mood_counts = recent_data['emotion'].value_counts().reset_index()
    mood_counts.columns = ['Emotion', 'Count']
    
    # Create a pie chart
    fig = px.pie(
        mood_counts,
        values='Count',
        names='Emotion',
        title='Team Mood Distribution (Last 7 Days)',
        color='Emotion',
        color_discrete_map={
            'Positive': '#2ECC71',  # Green
            'Neutral': '#F39C12',   # Orange
            'Negative': '#E74C3C'   # Red
        }
    )
    
    # Update layout
    fig.update_layout(
        legend_title="Mood",
    )
    
    return fig
