import pandas as pd
from datetime import datetime

class EventLogger:
    def __init__(self, file_path='events.xlsx'):
        self.file_path = file_path
        try:
            self.events_df = pd.read_excel(self.file_path)
        except FileNotFoundError:
            self.events_df = pd.DataFrame(columns=['employee_id', 'date', 'event_type', 'details'])

    def log_event(self, employee_id, event_type, details):
        new_event = pd.DataFrame([[employee_id, datetime.now().strftime("%Y-%m-%d"), event_type, details]],
                                columns=['employee_id', 'date', 'event_type', 'details'])
        self.events_df = pd.concat([self.events_df, new_event], ignore_index=True)
        self.events_df.to_excel(self.file_path, index=False)

class Employee:
    def __init__(self, employee_id, name, weekly_hours):
        self.employee_id = employee_id
        self.name = name
        self.weekly_hours = weekly_hours
        self.worked_hours = {}
        self.start_time = None
        self.weekly_reductions = {}
        self.event_logger = EventLogger()  # Initialisierung des EventLoggers

    def get_reduced_hours_for_week(self, year, week):
        return self.weekly_reductions.get((year, week), 0)

    def reduce_hours_for_week(self, year, week, hours):
        self.weekly_reductions[(year, week)] = self.weekly_reductions.get((year, week), 0) + hours
        self.event_logger.log_event(self.employee_id, 'Hours Reduction', f'Reduced weekly hours by {hours} for week {week}, {year}.')

