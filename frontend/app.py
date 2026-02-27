from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api/v1')


@app.route('/')
def index():
    """Dashboard/Home page"""
    try:
        # Get counts
        departments_response = requests.get(f'{API_BASE_URL}/departments')
        employees_response = requests.get(f'{API_BASE_URL}/employees')
        
        dept_count = len(departments_response.json()) if departments_response.ok else 0
        emp_count = len(employees_response.json()) if employees_response.ok else 0
        
        return render_template('index.html', 
                             dept_count=dept_count, 
                             emp_count=emp_count)
    except Exception as e:
        flash(f'Error connecting to API: {str(e)}', 'error')
        return render_template('index.html', dept_count=0, emp_count=0)


@app.route('/departments')
def departments():
    """List all departments"""
    try:
        response = requests.get(f'{API_BASE_URL}/departments')
        if response.ok:
            departments_list = response.json()
            return render_template('departments.html', departments=departments_list)
        else:
            flash('Failed to fetch departments', 'error')
            return render_template('departments.html', departments=[])
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('departments.html', departments=[])


@app.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    """Add a new department"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        payload = {
            'name': name,
            'description': description
        }
        
        try:
            response = requests.post(f'{API_BASE_URL}/departments/', json=payload)
            if response.ok:
                flash(f'Department "{name}" created successfully!', 'success')
                return redirect(url_for('departments'))
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                flash(f'Error: {error_detail}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('add_department.html')


@app.route('/employees')
def employees():
    """List all employees"""
    try:
        # Get employees and departments
        emp_response = requests.get(f'{API_BASE_URL}/employees')
        dept_response = requests.get(f'{API_BASE_URL}/departments')
        
        if emp_response.ok and dept_response.ok:
            employees_list = emp_response.json()
            departments_list = dept_response.json()
            
            # Create department lookup dictionary
            dept_dict = {dept['id']: dept['name'] for dept in departments_list}
            
            # Add department names to employees
            for emp in employees_list:
                emp['department_name'] = dept_dict.get(emp['department_id'], 'N/A')
            
            return render_template('employees.html', employees=employees_list)
        else:
            flash('Failed to fetch employees', 'error')
            return render_template('employees.html', employees=[])
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('employees.html', employees=[])


@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    """Add a new employee"""
    # Get departments for dropdown
    try:
        dept_response = requests.get(f'{API_BASE_URL}/departments')
        departments_list = dept_response.json() if dept_response.ok else []
    except:
        departments_list = []
    
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        department_id = request.form.get('department_id')
        is_active = request.form.get('is_active') == 'on'
        
        payload = {
            'email': email,
            'full_name': full_name,
            'role': role,
            'department_id': int(department_id),
            'is_active': is_active
        }
        
        try:
            response = requests.post(f'{API_BASE_URL}/employees/', json=payload)
            if response.ok:
                flash(f'Employee "{full_name}" created successfully!', 'success')
                return redirect(url_for('employees'))
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                flash(f'Error: {error_detail}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('add_employee.html', departments=departments_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
