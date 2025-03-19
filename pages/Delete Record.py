import streamlit as st
import pandas as pd
import pytz
from datetime import datetime

st.set_page_config(page_title="Cybersecurity Record Deletion", page_icon="🔍", layout="wide")

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

selected_sheet = st.selectbox("Select Sheet to Delete Record", all_sheets)

# Read the selected sheet
df = pd.read_excel(dataset_path, sheet_name=selected_sheet)
df.columns = df.columns.str.strip()

if search_query:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

st.markdown(f"### Current Data Preview - {selected_sheet}")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.header("Delete Record")

if df.empty:
    st.warning("No data available to delete.")
else:
    row_to_delete = st.number_input("Enter Row Number to Delete (Index)", min_value=0, max_value=len(df) - 1, step=1)
    delete_button = st.button("Delete Selected Row")

    if delete_button:
        df.drop(index=row_to_delete, inplace=True)
        df.reset_index(drop=True, inplace=True)

        try:
            with pd.ExcelWriter(dataset_path, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=selected_sheet, index=False)
            st.success(f"Row {row_to_delete} deleted successfully!")
        except Exception as e:
            st.error(f"Failed to delete record. Error: {e}")

        st.dataframe(df, use_container_width=True)

st.markdown("""
<div style='text-align:center; padding:20px; background-color:#f0f2f6; border-top:1px solid #ccc;'>
Developed with ❤️ by <a href='#' target='_blank'>Kutub Thakur</a>
</div>
""", unsafe_allow_html=True)