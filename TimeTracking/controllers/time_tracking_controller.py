import os
import pandas as pd
from datetime import datetime
from models.employee import Employee
from models.employer import Employer

class TimeTrackingController:
    def __init__(self):
        self.employer = Employer(employer_id="001", name="ACME CORPORATION")
        # Load existing data from Excel files
        try:
            self.employees_df = pd.read_excel('employees.xlsx')
            self.worked_hours_df = pd.read_excel('worked_hours.xlsx')
        except FileNotFoundError:
            self.employees_df = pd.DataFrame(columns=['employee_id', 'name', 'weekly_hours'])
            self.worked_hours_df = pd.DataFrame(columns=['employee_id', 'date', 'hours'])

        # Add employees to the employer from the DataFrame
        for _, row in self.employees_df.iterrows():
            employee = Employee(row['employee_id'], row['name'], row['weekly_hours'])
            self.employer.add_employee(employee)
    
    def create_employee(self, employee_id, name, weekly_hours):
            employee = Employee(employee_id, name, weekly_hours)
            self.employer.add_employee(employee)
            # Add employee to the DataFrame
            new_employee = pd.DataFrame([[employee_id, name, weekly_hours]],
                                        columns=['employee_id', 'name', 'weekly_hours'])
            self.employees_df = pd.concat([self.employees_df, new_employee], ignore_index=True)
            # Save to Excel
            self.employees_df.to_excel('employees.xlsx', index=False)
            return employee
  
    @staticmethod
    def calculate_break_time(total_hours, has_break_logged):
        if total_hours > 9:
            return 15 if has_break_logged else 45  # 15 minutes additional break if already logged, else 45 minutes
        elif total_hours > 6:
            return 0 if has_break_logged else 30  # No additional break if already logged, else 30 minutes
        else:
            return 0  # No break for 6 hours or less


    def log_hours_for_employee(self, employee_id, date, hours):
        employee = self.employer.get_employee(employee_id)
        if employee:
            date = pd.to_datetime(date)
            existing_hours = self.worked_hours_df[
                (self.worked_hours_df['employee_id'] == employee_id) &
                (self.worked_hours_df['date'] == date)
            ]['hours'].sum()
            total_hours = existing_hours + hours

            # Check if a break has already been logged for this employee on this date
            event_logger = EventLogger()
            has_break_logged = event_logger.has_break_event(employee_id, date)

            break_time = self.calculate_break_time(total_hours, has_break_logged)
            effective_hours = total_hours - (break_time / 60)

            # Remove existing entries for the same date to avoid duplication
            self.worked_hours_df = self.worked_hours_df[
                ~((self.worked_hours_df['employee_id'] == employee_id) &
                  (self.worked_hours_df['date'] == date))
            ]

            new_hours = pd.DataFrame([[employee_id, date, effective_hours]],
                                     columns=['employee_id', 'date', 'hours'])
            self.worked_hours_df = pd.concat([self.worked_hours_df, new_hours], ignore_index=True)

            # Log the break time in the EventLogger
            self.log_break_event(employee_id, date, break_time)

            # Save to Excel
            self.worked_hours_df.to_excel('worked_hours.xlsx', index=False)
            return True
        return False

    def log_break_event(self, employee_id, date, break_time):
        event_logger = EventLogger()
        event_logger.log_event(employee_id, 'break', f'Pausenzeit von {break_time} Minuten abgezogen.')

    def get_employee_weekly_hours(self, employee_id, year, week):
        # Filter worked hours for the specific employee, year, and week
        weekly_hours = self.worked_hours_df[
            (self.worked_hours_df['employee_id'] == employee_id) &
            (pd.to_datetime(self.worked_hours_df['date']).dt.year == year) &
            (pd.to_datetime(self.worked_hours_df['date']).dt.isocalendar().week == week)
        ]['hours'].sum()
        return weekly_hours

    def get_employee_remaining_hours(self, employee_id, year, week):
        employee = self.employer.get_employee(employee_id)
        if employee:
            weekly_hours_worked = self.get_employee_weekly_hours(employee_id, year, week)
            reduced_hours = employee.get_reduced_hours_for_week(year, week)
            return (employee.weekly_hours - reduced_hours) - weekly_hours_worked
        return None

    def create_employee_directory(self):
        # Create a directory DataFrame
        directory_df = self.employees_df[['employee_id', 'name']].copy()
        directory_df.to_excel('employee_directory.xlsx', index=False)

    def create_yearly_summary(self):
        # Ensure the directory exists
        if not os.path.exists('yearly_summaries'):
            os.makedirs('yearly_summaries')

        # Convert the 'date' column to datetime if it's not already
        self.worked_hours_df['date'] = pd.to_datetime(self.worked_hours_df['date'])

        # Group by employee and year, and only consider years with logged hours
        yearly_summaries = self.worked_hours_df.groupby(['employee_id', self.worked_hours_df['date'].dt.year])['hours'].sum().reset_index()

        # Create a summary file for each employee and year where hours were logged
        for employee_id, year, total_hours in yearly_summaries.itertuples(index=False):
            filename = f"yearly_summaries/{int(year)}_employee-{employee_id}.xlsx"
            summary_df = pd.DataFrame([[int(year), total_hours]], columns=['year', 'total_hours'])
            summary_df.to_excel(filename, index=False)

class Message:
    def __init__(self, employee_id, content):
        self.employee_id = employee_id
        self.content = content

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

    def has_break_event(self, employee_id, date):
        date_str = date.strftime("%Y-%m-%d")
        break_events = self.events_df[
            (self.events_df['employee_id'] == employee_id) &
            (self.events_df['date'] == date_str) &
            (self.events_df['event_type'] == 'break')
        ]
        return not break_events.empty
