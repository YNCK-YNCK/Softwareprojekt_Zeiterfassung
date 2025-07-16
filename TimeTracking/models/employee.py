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

    def log_hours(self, date, hours):
        if date in self.worked_hours:
            self.worked_hours[date] += hours
        else:
            self.worked_hours[date] = hours

    def start_tracking(self):
        if self.start_time is None:
            self.start_time = datetime.now()
            return True
        return False

    def stop_tracking(self):
        if self.start_time is not None:
            elapsed = datetime.now() - self.start_time
            self.log_hours(datetime.now().date(), elapsed.total_seconds() / 3600)
            self.start_time = None
            return True
        return False

    def get_tracked_hours_today(self):
        today = datetime.now().date()
        return self.worked_hours.get(today, 0)

    def check_warnings(self):
        today_hours = self.get_tracked_hours_today()
        if today_hours > 8:
            self.event_logger.log_event(self.employee_id, 'Warning', 'Exceeded 8 hours of work.')
            if today_hours > 11:
                self.stop_tracking()
                self.event_logger.log_event(self.employee_id, 'System Action', 'Stopped: Exceeded maximum working hours of 11.')
                return "Stopped: Exceeded maximum working hours of 11."
            return "Warning: Exceeded 8 hours of work."
        return None

    def get_reduced_hours_for_week(self, year, week):
        return self.weekly_reductions.get((year, week), 0)

    def reduce_hours_for_week(self, year, week, hours):
        self.weekly_reductions[(year, week)] = self.weekly_reductions.get((year, week), 0) + hours
        self.event_logger.log_event(self.employee_id, 'Hours Reduction', f'Reduced weekly hours by {hours} for week {week}, {year}.')
