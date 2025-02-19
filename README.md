# ELTwPostgres
Creating a ELT (Extract Load Transform) that ingests the data into a postgres database (hosted locally) and run a cleaning script. Sample data is provided in employees_data_source.csv

<h1>Script Descriptions</h1>
<ul>
  <li><strong>db_utils.py</strong> provides functions for connecting to Postgres database</li>
  <li><strong>load_data_postgres.py</strong> ingests data from <strong>employee_data_source.csv</strong> into a postgres database</li>
  <li><strong>transform_data.py</strong> fixes data quality issues in the postgres database and imposes constraints</li>
</ul>

<h1>Data Descriptions</h1>
All the data for this project comes from the <strong>employee_data_source.csv</strong>. The csv has the following attributes:
<ul>
  <li>Employee Id: An id meant to be unique for each individual worker</li>
  <li>Name: employee's name (a text field)</li>
  <li>Age: employee's age (an integer field)</li>
  <li>Department: department of employee, listed as 'Unknown' if not recorded (null)</li>
  <li>Date of Joining: date the employee started working at the company, a date field</li>
  <li>Years of Experience: employee's number of years of working total</li>
  <li>Country: the country an employee's from (a text field), listed as 'Unknown' if not recorded</li>
  <li>Salary: the employee's salary (an integer field)</li>
  <li>Performance Rating: Either 'High Performers', 'Average Performers', 'Low Performers' or 'Unknown' if not recorded</li>
</ul>

<h2>Instructions</h2>
<ol>
  <li>Install <a href = "https://www.w3schools.com/postgresql/postgresql_install.php">Postgres</a></li>
  <li>Clone the repository</li>
  <li>Create a .env file and copy-paste the contents of the .boilerplate_env into the .env file</li>
  <li>Fill in the username and password fields of the .env file</li>
  <li>Ensure Postgres is active on your machine</li>
  <li>If on Windows run setup_dependencies.ps1 and run_scripts.ps1</li>
  <li>If on Linux/Unix run setup_dependencies.sh and run_scripts.sh</li>
</ol>
*Note: Python3 must be installed on your computer in order to run the scripts locally
