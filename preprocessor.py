import re
import pandas as pd

def preprocess(data):
    # Regex to match date-time pattern in WhatsApp chats
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[apm]{2}\s-\s',  # Example: 12/05/21, 8:45 pm -
        r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s[apm]{2}\s-\s'   # Example: 12/05/2021, 8:45 pm -
    ]
    
    messages, dates = [], []
    
    for pattern in patterns:
        temp_messages = re.split(pattern, data)[1:]
        temp_dates = re.findall(pattern, data)
        
        if temp_dates:
            messages = temp_messages
            dates = temp_dates
            break
        
     # If no dates were found, return an empty DataFrame
    if not dates:
        return pd.DataFrame()

    # Create initial DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Try parsing with different date formats
    date_formats = [
        '%d/%m/%y, %I:%M %p -',  # Example: 12/05/21, 8:45 pm
        '%d/%m/%Y, %I:%M %p -'   # Example: 12/05/2021, 8:45 pm
    ]
    
    # Parse dates
    for fmt in date_formats:
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format=fmt, errors='coerce')
            if df['message_date'].notna().all():
                break
        except ValueError:
            pass

    # Rename and filter
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users, messages = [], []
    for message in df['user_message']:
        if ': ' in message:
            user, msg = message.split(': ', 1)
            users.append(user)
            messages.append(msg)
        else:
            users.append('group_notification')
            messages.append(message)

    df['user'] = users
    df['message'] = messages

    # Drop original column
    df.drop(columns=['user_message'], inplace=True)

    # Add date features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Define periods for heatmaps
    period = []
    for hour in df['hour']:
        if pd.isna(hour):
            period.append(None)
        elif hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period

    return df
"""

    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]  # Skip first empty split
    dates = re.findall(pattern, data)

    # Create initial DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    print(df)

    # Convert 'message_date' to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p -', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        if ': ' in message:
            user, msg = message.split(': ', 1)
            users.append(user)
            messages.append(msg)
        else:
            users.append('group_notification')
            messages.append(message)

    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    # Add additional date-related columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Define time periods for hours
    period = []
    for hour in df['hour']:
        if pd.isna(hour):
            period.append(None)
        elif hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period

    return df"""