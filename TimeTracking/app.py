from flask import Flask, request, jsonify, render_template, redirect, url_for
from controllers.time_tracking_controller import TimeTrackingController, Message
from datetime import datetime

app = Flask(__name__)
controller = TimeTrackingController()
messages = []

# Web-Oberfläche
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    user_id = request.form['user_id']
    if role == 'employer':
        return redirect(url_for('employer_dashboard'))
    elif role == 'employee':
        return redirect(url_for('employee_dashboard', employee_id=user_id))

@app.route('/employer')
def employer_dashboard():
    employees = controller.employees_df.to_dict('records')
    return render_template('employer_dashboard.html', employees=employees)

@app.route('/employer/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        weekly_hours = int(request.form['weekly_hours'])
        employee_id = f"1{len(controller.employees_df) + 1:02d}"
        controller.create_employee(employee_id, name, weekly_hours)
        return redirect(url_for('employer_dashboard'))
    return render_template('add_employee.html')

@app.route('/employer/employee/<employee_id>')
def view_employee(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    employee_records = controller.employees_df[controller.employees_df['employee_id'] == employee_id].to_dict('records')
    if not employee_records:
        return "Employee not found", 404
    employee = employee_records[0]
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    weekly_hours = controller.get_employee_weekly_hours(employee_id, current_year, current_week)
    reduced_hours = controller.get_employee_remaining_hours(employee_id, current_year, current_week)
    return render_template('view_employee.html', employee=employee, weekly_hours=weekly_hours, reduced_hours=reduced_hours)

@app.route('/employer/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        reduction_hours = int(request.form['reduction_hours'])
        employee = controller.employer.get_employee(employee_id)
        if employee:
            current_year = datetime.now().year
            current_week = datetime.now().isocalendar()[1]
            employee.reduce_hours_for_week(current_year, current_week, reduction_hours)
            weekly_hours_worked = controller.get_employee_weekly_hours(employee_id, current_year, current_week)
            remaining_hours = (employee.weekly_hours - employee.get_reduced_hours_for_week(current_year, current_week)) - weekly_hours_worked
            message_content = f"Due to operational requirements, your working hours need to be reduced by {reduction_hours} hours for the current week. Your current remaining hours are {remaining_hours}."
            messages.append(Message(employee_id, message_content))
        return redirect(url_for('employer_dashboard'))
    employees = controller.employees_df.to_dict('records')
    return render_template('send_message.html', employees=employees)

@app.route('/employer/create_yearly_summaries', methods=['POST'])
def create_yearly_summaries():
    controller.create_yearly_summary()
    return redirect(url_for('employer_dashboard'))

@app.route('/employee/<employee_id>/start_tracking', methods=['POST'])
def start_tracking(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    if controller.start_tracking(employee_id):
        return jsonify({"status": "Tracking started"})
    return jsonify({"status": "Already tracking"}), 400

@app.route('/employee/<employee_id>/stop_tracking', methods=['POST'])
def stop_tracking(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    if controller.stop_tracking(employee_id):
        return jsonify({"status": "Tracking stopped"})
    return jsonify({"status": "Not tracking"}), 400

@app.route('/employee/<employee_id>/check_warnings', methods=['GET'])
def check_warnings(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    warning = controller.check_warnings(employee_id)
    if warning:
        print(f"Warning for employee {employee_id}: {warning}")
        return jsonify({"warning": warning})
    print(f"No warnings for employee {employee_id}")
    return jsonify({"warning": "No warnings"}), 200

@app.route('/employee/<employee_id>/log_hours', methods=['GET', 'POST'])
def log_hours(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    if request.method == 'POST':
        date_str = request.form.get('date')
        hours = request.form.get('hours')
        if not date_str or not hours:
            return "Date and hours are required", 400
        try:
            hours = float(hours)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError as e:
            return f"Invalid input: {str(e)}", 400
        success = controller.log_hours_for_employee(employee_id, date, hours)
        if success:
            return redirect(url_for('employee_dashboard', employee_id=employee_id))
        else:
            return "Failed to log hours", 400
    return render_template('log_hours.html', employee_id=employee_id)

@app.route('/employee/<employee_id>')
def employee_dashboard(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    employee = controller.employer.get_employee(employee_id)
    if not employee:
        return "Employee not found", 404
    employee_messages = [msg.content for msg in messages if msg.employee_id == employee_id]
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    weekly_hours = controller.get_employee_weekly_hours(employee_id, current_year, current_week)
    remaining_hours = controller.get_employee_remaining_hours(employee_id, current_year, current_week)
    return render_template('employee_dashboard.html',
                           employee=employee,
                           employee_id=employee_id,
                           weekly_hours=weekly_hours,
                           remaining_hours=remaining_hours,
                           messages=employee_messages)

@app.route('/employee/<employee_id>/weekly_hours')
def weekly_hours(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    employee = controller.employer.get_employee(employee_id)
    if not employee:
        return "Employee not found", 404
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    weekly_hours = controller.get_employee_weekly_hours(employee_id, current_year, current_week)
    return render_template('weekly_hours.html', employee=employee, year=current_year, week=current_week, weekly_hours=weekly_hours)

# API-Endpunkte
@app.route('/api/employees', methods=['GET'])
def api_get_employees():
    employees = controller.employees_df.to_dict('records')
    return jsonify(employees)

@app.route('/api/employees/<employee_id>', methods=['GET'])
def api_get_employee(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    employee_records = controller.employees_df[controller.employees_df['employee_id'] == employee_id].to_dict('records')
    if not employee_records:
        return jsonify({"error": "Employee not found"}), 404
    employee = employee_records[0]
    return jsonify(employee)

@app.route('/api/employees/<employee_id>/tracking/start', methods=['POST'])
def api_start_tracking(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    if controller.start_tracking(employee_id):
        return jsonify({"status": "Tracking started"})
    return jsonify({"status": "Already tracking"}), 400

@app.route('/api/employees/<employee_id>/tracking/stop', methods=['POST'])
def api_stop_tracking(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    if controller.stop_tracking(employee_id):
        return jsonify({"status": "Tracking stopped"})
    return jsonify({"status": "Not tracking"}), 400

@app.route('/api/employees/<employee_id>/hours', methods=['POST'])
def api_log_hours(employee_id):
    data = request.get_json()
    date_str = data.get('date')
    hours = data.get('hours')
    if not date_str or not hours:
        return jsonify({"error": "Date and hours are required"}), 400
    try:
        hours = float(hours)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    success = controller.log_hours_for_employee(employee_id, date, hours)
    if success:
        return jsonify({"status": "Hours logged"})
    else:
        return jsonify({"error": "Failed to log hours"}), 400

@app.route('/api/employees/<employee_id>/hours', methods=['GET'])
def api_get_employee_hours(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    employee_records = controller.employees_df[controller.employees_df['employee_id'] == employee_id].to_dict('records')
    if not employee_records:
        return jsonify({"error": "Employee not found"}), 404
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    weekly_hours = controller.get_employee_weekly_hours(employee_id, current_year, current_week)
    remaining_hours = controller.get_employee_remaining_hours(employee_id, current_year, current_week)
    return jsonify({
        "weekly_hours": weekly_hours,
        "remaining_hours": remaining_hours
    })

@app.route('/api/employees/<employee_id>/check_warnings', methods=['GET'])
def api_check_warnings(employee_id):
    employee_id = controller.employees_df['employee_id'].dtype.type(employee_id)
    warning = controller.check_warnings(employee_id)
    if warning:
        print(f"Warning for employee {employee_id}: {warning}")
        return jsonify({"warning": warning})
    print(f"No warnings for employee {employee_id}")
    return jsonify({"warning": "No warnings"}), 200

if __name__ == '__main__':
    app.run(debug=True)
