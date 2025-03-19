import streamlit as st
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(page_title="Cybersecurity Record Adder", page_icon="🛠️", layout="wide")

# Header with Project Title and Live Clock
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("""
    <h1 style='font-size:32px;'>
        <span style='color:#2E86C1; animation: glow 1s infinite alternate;'>AI-Powered Cybersecurity Compliance Dashboard - CUNY</span>
    </h1>
    <style>
    @keyframes glow {
      from { text-shadow: 0 0 5px #3498DB, 0 0 10px #3498DB, 0 0 15px #3498DB; }
      to { text-shadow: 0 0 20px #2980B9, 0 0 30px #2980B9, 0 0 40px #2980B9; }
    }
    </style>
    """, unsafe_allow_html=True)

with col2:
    tz = pytz.timezone('America/New_York')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<div style='font-size:18px; animation: pulse 1s infinite alternate;'>🕒 {current_time}</div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    @keyframes pulse {
      from { opacity: 0.5; }
      to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Search/Filter and Logo
with st.sidebar:
    st.markdown("### Search and Filter")
    search_query = st.text_input("Search in Sheet")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='position:fixed; bottom:30px;'>", unsafe_allow_html=True)
    st.image("logo.png", width=250)
    st.markdown("<p style='text-align:center;'>AI GRC - CUNY</p></div>", unsafe_allow_html=True)

# Load the Excel file
dataset_path = 'cyber_data.xlsx'
all_sheets = pd.ExcelFile(dataset_path).sheet_names

selected_sheet = st.selectbox("Select Sheet to Add Record", all_sheets)

# Read the selected sheet with NaN handling for numeric metrics
df = pd.read_excel(dataset_path, sheet_name=selected_sheet)
df.columns = df.columns.str.strip()

# Ensure numeric fields are converted and NaN filled for all relevant columns
numeric_columns = ['Average Score', 'Total Score', 'Rating']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

if search_query:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

st.markdown(f"### Current Data Preview - {selected_sheet}")
st.dataframe(df.tail(5), use_container_width=True)

st.markdown("---")
st.header("Add New Record")

# Dynamic form for adding record
form = st.form("add_record_form")
new_record = {}
# Dynamic columns excluding "Total Score" and "Average Score" for Q-sheets
auto_calc_cols = ['Vulnerability Scan Report – Authenticated Scan', 'Firewall Feature Adaption', 'End Point Protection Total Installation (XDR)']

target_is_quarter = selected_sheet in ['Q1', 'Q2', 'Q3', 'Q4']

for col in df.columns:
    if target_is_quarter and col in ['Total Score', 'Average Score']:
        continue  # Skip manual input for these
    dtype = df[col].dtype
    if pd.api.types.is_numeric_dtype(dtype):
        new_record[col] = form.number_input(f"{col}", value=0.0)
    else:
        new_record[col] = form.text_input(f"{col}", value="")

submit = form.form_submit_button("Add Record")

if submit:
    # Append user entry
    new_df = pd.DataFrame([new_record])

    # Auto compute Total and Average Score for quarter sheets
    if target_is_quarter:
        for field in auto_calc_cols:
            new_df[field] = pd.to_numeric(new_df[field], errors='coerce').fillna(0)
        new_df['Total Score'] = new_df[auto_calc_cols].sum(axis=1)
        new_df['Average Score'] = new_df['Total Score'] / len(auto_calc_cols)

    df = pd.concat([df, new_df], ignore_index=True)

    try:
        with pd.ExcelWriter(dataset_path, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=selected_sheet, index=False)
        st.success("Record added successfully!")
    except Exception as e:
        st.error(f"Failed to save record. Error: {e}")

    st.dataframe(df.tail(5), use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px; background-color:#f0f2f6; border-top:1px solid #ccc;'>
Developed with ❤️ by <a href='#' target='_blank'>Kutub Thakur</a>
</div>
""", unsafe_allow_html=True)