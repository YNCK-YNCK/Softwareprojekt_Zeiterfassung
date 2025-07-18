class Employer:
    def __init__(self, employer_id, name):
        self.employer_id = employer_id
        self.name = name
        self.employees = {}

    def add_employee(self, employee):
        self.employees[employee.employee_id] = employee

    def remove_employee(self, employee_id): # Note: currently not implemented.
        if employee_id in self.employees:
            del self.employees[employee_id]

    def get_employee(self, employee_id):
        return self.employees.get(employee_id)
