# AI-Powered Cybersecurity Compliance Dashboard - CUNY

## Overview
This project is a comprehensive Streamlit-based interactive dashboard designed to analyze, visualize, and manage cybersecurity compliance data for CUNY colleges. It provides powerful insights into various cybersecurity metrics, including vulnerability assessments, NIST adoption, policy status, and cybersecurity awareness training completion.

## Features
- **Dynamic Dashboard** for real-time visual analytics.
- **Trend Analysis** across Q1 to Q4 for each college.
- **Health Record Assessment** visualization.
- **NIST Adoption Status Tracking**.
- **Policy Implementation Progress**.
- **Cybersecurity Awareness Training Monitoring**.
- **Live Clock and Animated Project Title**.
- **Search and Filter** functionality.
- **Add, Edit, and Delete Records** with seamless Excel sheet updates.
- **PK Programmers branding and CUNY logo integration**.

## Project Structure
```
.
├── app.py                   # Main Dashboard Python file
├── add_record.py            # Add new records module
├── edit_record.py           # Edit existing records module
├── delete_record.py         # Delete records module
├── cyber_data.xlsx          # Excel dataset with multiple sheets (Q1-Q4, NIST, Health, Policy, Training)
├── logo.png                 # CUNY Logo
├── requirements.txt         # Python package dependencies
└── README.md                # Project Documentation
```

## Dataset
The dataset `cyber_data.xlsx` includes multiple sheets:
- **Q1, Q2, Q3, Q4**: Quarterly cybersecurity compliance data
- **Health Record Assessment**
- **NIST Adoption**
- **Policy**
- **Cybersecurity Awareness Training**

Each sheet includes columns like `College Name`, `Vulnerability Scan Report`, `Firewall Feature Adaption`, `End Point Protection`, `Total Score`, `Average Score`, and `Letter Grade`.

## Technology Stack
- **Python 3.9+**
- **Streamlit**
- **Pandas**
- **Plotly Express**
- **OpenPyXL**
- **Seaborn (optional)**

## Installation
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
streamlit run app.py
```

## Key Functionalities
- **Auto-Calculation of Total and Average Scores** for each record.
- **Interactive Navigation Menu** for seamless transitions between views.
- **Edit and Delete Functionality** that updates the Excel dataset dynamically.
- **NaN Handling and Data Cleaning** before plotting.
- **Responsive layout optimized for wide screens**.

## Future Improvements
- Add User Authentication and Role-based Access Control.
- Implement PDF and Report generation.
- Integration with real-time cybersecurity data sources.

## Developed By
[PK Programmers](https://www.pkprogrammers.com/)

## License
This project is developed for educational purposes for CUNY cybersecurity compliance management.

---
