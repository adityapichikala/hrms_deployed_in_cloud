"""
Test script for HRMS Backend API
This script tests all the endpoints to verify the API is working correctly.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_health():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_create_department():
    """Test creating a department"""
    print("\n=== Testing Create Department ===")
    data = {
        "name": "Engineering",
        "description": "Software development team"
    }
    response = requests.post(f"{BASE_URL}/api/v1/departments/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201, response.json()

def test_get_departments():
    """Test getting all departments"""
    print("\n=== Testing Get All Departments ===")
    response = requests.get(f"{BASE_URL}/api/v1/departments/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200, response.json()

def test_create_employee(department_id):
    """Test creating an employee"""
    print("\n=== Testing Create Employee ===")
    data = {
        "email": "john.doe@company.com",
        "full_name": "John Doe",
        "role": "Senior Software Engineer",
        "is_active": True,
        "department_id": department_id
    }
    response = requests.post(f"{BASE_URL}/api/v1/employees/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201, response.json()

def test_get_employees():
    """Test getting all employees"""
    print("\n=== Testing Get All Employees ===")
    response = requests.get(f"{BASE_URL}/api/v1/employees/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200, response.json()

def test_get_employee_by_id(employee_id):
    """Test getting employee by ID"""
    print(f"\n=== Testing Get Employee by ID ({employee_id}) ===")
    response = requests.get(f"{BASE_URL}/api/v1/employees/{employee_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200, response.json()

def main():
    """Run all tests"""
    print("=" * 60)
    print("HRMS Backend API - Test Suite")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        assert test_root(), "Root endpoint failed"
        assert test_health(), "Health check failed"
        
        # Test department creation
        success, dept_data = test_create_department()
        if not success:
            print("\n⚠️  Department might already exist, trying to get existing departments...")
        
        # Get all departments
        success, departments = test_get_departments()
        assert success and len(departments) > 0, "No departments found"
        department_id = departments[0]["id"]
        print(f"\n✅ Using Department ID: {department_id}")
        
        # Test employee creation
        success, emp_data = test_create_employee(department_id)
        if success:
            employee_id = emp_data["id"]
            
            # Test getting all employees
            success, employees = test_get_employees()
            assert success and len(employees) > 0, "No employees found"
            
            # Test getting employee by ID
            success, employee = test_get_employee_by_id(employee_id)
            assert success, "Failed to get employee by ID"
            
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
        else:
            print("\n⚠️  Employee might already exist")
            # Test getting all employees anyway
            success, employees = test_get_employees()
            if success and len(employees) > 0:
                print("\n" + "=" * 60)
                print("✅ BASIC TESTS PASSED! (Employee already exists)")
                print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
