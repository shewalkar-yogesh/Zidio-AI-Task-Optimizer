import pandas as pd
import os
import datetime

# Define the path for the CSV file
DATA_FILE = "employee_mood_data.csv"

def save_mood_entry(employee_id, timestamp, text, sentiment_score, emotion):
    """
    Save a mood entry to the CSV file.
    
    Args:
        employee_id (str): Anonymized employee ID
        timestamp (datetime): Time of the entry
        text (str): Original mood text
        sentiment_score (float): Normalized sentiment score (0-1)
        emotion (str): Emotion label (Negative, Neutral, Positive)
    """
    # Create DataFrame with the new entry
    new_entry = pd.DataFrame([{
        'employee_id': employee_id,
        'timestamp': timestamp,
        'date': timestamp.strftime('%Y-%m-%d'),
        'time': timestamp.strftime('%H:%M:%S'),
        'text': text,
        'sentiment_score': sentiment_score,
        'emotion': emotion
    }])
    
    # Check if file exists
    if os.path.exists(DATA_FILE):
        # Append to existing file
        existing_data = pd.read_csv(DATA_FILE)
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        updated_data.to_csv(DATA_FILE, index=False)
    else:
        # Create new file
        new_entry.to_csv(DATA_FILE, index=False)
    
def load_mood_data():
    """
    Load mood data from the CSV file.
    
    Returns:
        DataFrame: Mood data or empty DataFrame if file doesn't exist
    """
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE)
        # Convert timestamp strings back to datetime objects
        data['timestamp'] = pd.to_datetime(data['date'] + ' ' + data['time'])
        return data
    else:
        # Return empty DataFrame with the expected columns
        return pd.DataFrame(columns=[
            'employee_id', 'timestamp', 'date', 'time', 
            'text', 'sentiment_score', 'emotion'
        ])

def check_consecutive_negative_moods(employee_id, count=3):
    """
    Check if an employee has had consecutive negative moods.
    
    Args:
        employee_id (str): Employee ID to check
        count (int): Number of consecutive negative moods to check for
        
    Returns:
        bool: True if employee has had 'count' consecutive negative moods
    """
    data = load_mood_data()
    
    if data.empty:
        return False
    
    # Filter data for the specific employee
    employee_data = data[data['employee_id'] == employee_id].sort_values('timestamp')
    
    if len(employee_data) < count:
        return False
    
    # Check the last 'count' entries
    last_entries = employee_data.tail(count)
    
    # Check if all are negative
    return all(last_entries['emotion'] == 'Negative')
