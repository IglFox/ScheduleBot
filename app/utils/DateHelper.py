from datetime import datetime

def get_today_date():
    return datetime.now().strftime("%H-%M_%d-%m-%Y")