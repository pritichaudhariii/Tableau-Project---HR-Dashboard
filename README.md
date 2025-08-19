📊📉 HR DASHBOARD

📝 Project Overview

This project showcases a Human Resources (HR) Analytics Dashboard built in Tableau using a synthetic dataset generated with Python (Faker + NumPy). The dataset contains 8,950 employee records that mimic real-world HR data, including demographics, job roles, salaries, performance ratings, and attrition details.

The goal is to demonstrate how HR teams can use data visualization to gain insights into workforce trends. The dashboard is divided into three main sections:

- 📊 Overview – Company-wide metrics on hiring, terminations, departmental composition, and geographic distribution.
- 🟩 Demographics – Workforce composition by gender, age groups, and education levels, along with performance correlations.
- 💰 Income – Salary analysis across education levels, gender, and departments, as well as age–salary patterns.


<img width="1398" height="793" alt="Screenshot 2025-08-19 at 11 59 39 AM" src="https://github.com/user-attachments/assets/ffc27bad-baaf-4d08-887d-ebc224f94ce2" />


📦 Repository Contents

This repository contains everything needed to generate the dataset and explore the HR Dashboard in Tableau:

[HR Dataset](./HumanResources.csv) – Synthetic HR dataset (8,950 records) generated using Python’s Faker library and custom logic. Includes demographics, job details, salaries, performance ratings, and attrition history.

[Python Script](./generate_hr_data.py) – Python script that reproduces the dataset from scratch.

[Icons](./images.zip) – Icons sourced from Flaticon and customized in Photopea to match the dashboard’s theme. Includes editable PSD/Photopea files for further customization.

[HR Dashboard](./HR_Dashboard.twbx) – Tableau workbook file. 


📊 Dashboard Scope

🟦 Overview
- 👥 Total hired, active, terminated
- 📈 Hires vs. terminations over time
- 🏢 Employees by department, job title
- 🏙️ HQ (New York City) vs. branches
- 🌎 Distribution by city/state

🟩 Demographics
- 🚻 Gender ratio
- 🎂 Age groups & 🎓 education levels
- 🔢 Counts by age group and by education level
- 📚 Education vs. ⭐ performance

🟨 Income
- 💰 Salary by education level and gender
- 📊 Age–salary relationships by department
