-- Create Database
CREATE DATABASE IF NOT EXISTS employee_management;
USE employee_management;

-- Create Departments Table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL
);

-- Create Roles Table
CREATE TABLE Roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) NOT NULL,
    base_salary DECIMAL(10, 2) NOT NULL
);

-- Create Employees Table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    department_id INT,
    role_id INT,
    hire_date DATE,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id) ON DELETE SET NULL,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE SET NULL
);

-- Create Salary History Table
CREATE TABLE SalaryHistory (
    salary_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    salary_amount DECIMAL(10, 2),
    change_date DATE,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE
);

-- Create Projects Table
CREATE TABLE Projects (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(100) NOT NULL,
    budget DECIMAL(15, 2) NOT NULL
);

-- Create EmployeeProject
CREATE TABLE EmployeeProject (
    employee_id INT,
    project_id INT,
    role_in_project VARCHAR(100),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE,
    PRIMARY KEY (employee_id, project_id)
);

-- Insert Data into Departments
INSERT INTO Departments (department_name) VALUES
('Human Resources'),
('Engineering'),
('Sales'),
('Marketing');

-- Insert Data into Roles
INSERT INTO Roles (role_name, base_salary) VALUES
('HR Manager', 60000.00),
('Software Engineer', 85000.00),
('Sales Representative', 50000.00),
('Marketing Specialist', 55000.00);

-- Insert Data into Employees
INSERT INTO Employees (first_name, last_name, department_id, role_id, hire_date) VALUES
('John', 'Doe', 1, 1, '2020-01-15'),
('Jane', 'Smith', 2, 2, '2019-07-01'),
('Mark', 'Johnson', 3, 3, '2021-03-10'),
('Steven', 'Brown', 4, 4, '2018-05-23');

-- Insert Data into Salary History
INSERT INTO SalaryHistory (employee_id, salary_amount, change_date) VALUES
(1, 60000.00, '2020-01-15'),
(2, 85000.00, '2019-07-01'),
(3, 50000.00, '2021-03-10'),
(4, 55000.00, '2018-05-23');

-- Insert Data into Projects
INSERT INTO Projects (project_name, budget) VALUES
('Employee Portal Development', 150000.00),
('Customer Relationship Management', 200000.00);

-- Assign Employees to Projects
INSERT INTO EmployeeProject (employee_id, project_id, role_in_project) VALUES
(2, 1, 'Lead Developer'),
(3, 2, 'Project Manager');

-- Query to Get All Employees with Their Department and Role
SELECT e.first_name, e.last_name, d.department_name, r.role_name
FROM Employees e
JOIN Departments d ON e.department_id = d.department_id
JOIN Roles r ON e.role_id = r.role_id;

-- Query to Calculate Total Salary Expense Per Department
SELECT d.department_name, SUM(r.base_salary) AS total_salary_expense
FROM Employees e
JOIN Departments d ON e.department_id = d.department_id
JOIN Roles r ON e.role_id = r.role_id
GROUP BY d.department_name;

-- Query to Get Employee’s Salary History
SELECT e.first_name, e.last_name, s.salary_amount, s.change_date
FROM SalaryHistory s
JOIN Employees e ON s.employee_id = e.employee_id
ORDER BY e.last_name;

-- Query to Get Employees Working on a Specific Project
SELECT e.first_name, e.last_name, p.project_name, ep.role_in_project
FROM EmployeeProject ep
JOIN Employees e ON ep.employee_id = e.employee_id
JOIN Projects p ON ep.project_id = p.project_id;

-- Query to Get Average Salary in Each Department
SELECT d.department_name, AVG(r.base_salary) AS average_salary
FROM Employees e
JOIN Departments d ON e.department_id = d.department_id
JOIN Roles r ON e.role_id = r.role_id
GROUP BY d.department_name;

-- Query to Find Employees Who Have Received a Salary Raise
SELECT e.first_name, e.last_name, MAX(s.salary_amount) AS latest_salary
FROM SalaryHistory s
JOIN Employees e ON s.employee_id = e.employee_id
GROUP BY e.employee_id
HAVING MAX(s.salary_amount) > (SELECT salary_amount FROM SalaryHistory WHERE employee_id = e.employee_id ORDER BY change_date LIMIT 1);

-- Create a Stored Procedure to Hire an Employee
DELIMITER $$

CREATE PROCEDURE HireEmployee(
    IN emp_first_name VARCHAR(100),
    IN emp_last_name VARCHAR(100),
    IN emp_dept_id INT,
    IN emp_role_id INT,
    IN emp_salary DECIMAL(10,2)
)
BEGIN
    DECLARE emp_id INT;

    START TRANSACTION;

    -- Insert new employee
    INSERT INTO Employees (first_name, last_name, department_id, role_id, hire_date)
    VALUES (emp_first_name, emp_last_name, emp_dept_id, emp_role_id, CURDATE());

    SET emp_id = LAST_INSERT_ID();

    -- Insert salary record
    INSERT INTO SalaryHistory (employee_id, salary_amount, change_date)
    VALUES (emp_id, emp_salary, CURDATE());

    COMMIT;
END$$

DELIMITER ;

-- Use the Stored Procedure to Hire a New Employee
CALL HireEmployee('David', 'Smith', 2, 2, 90000);
