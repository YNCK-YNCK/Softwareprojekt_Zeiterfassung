import pandas as pd
from datetime import datetime
from TimeTracking.models.employee import Employee
from TimeTracking.models.employer import Employer

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

    def log_hours_for_employee(self, employee_id, date, hours):
        employee = self.employer.get_employee(employee_id)
        if employee:
            employee.log_hours(date, hours)
            # Log hours to the DataFrame
            new_hours = pd.DataFrame([[employee_id, date, hours]],
                                    columns=['employee_id', 'date', 'hours'])
            self.worked_hours_df = pd.concat([self.worked_hours_df, new_hours], ignore_index=True)
            # Save to Excel
            self.worked_hours_df.to_excel('worked_hours.xlsx', index=False)
            return True
        return False

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
