import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
from datetime import datetime

st.set_page_config(page_title="Cybersecurity Analytics Dashboard", page_icon="🛡️", layout="wide")

# Animated Project Name with Clock Parallel
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

# Sidebar - Search and Logo
with st.sidebar:
    st.markdown("### Search and Filter")
    search_query = st.text_input("Search College or Keyword")
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div style='position:fixed; bottom:80px;'>", unsafe_allow_html=True)
    st.image("logo.png", width=250)
    st.markdown("<p style='text-align:center;'>AI GRC - CUNY</p></div>", unsafe_allow_html=True)

# Load the Excel file
dataset = pd.ExcelFile('cyber_data.xlsx')

# Read sheets with safer NaN handling
dfs = {}
for sheet in dataset.sheet_names:
    df = pd.read_excel(dataset, sheet, dtype=str)
    df.columns = df.columns.str.strip()
    # Recalculate 'Total Score' and 'Average Score' if possible
    if {'Vulnerability Scan Report – Authenticated Scan', 'Firewall Feature Adaption', 'End Point Protection Total Installation (XDR)'}.issubset(df.columns):
        df['Total Score'] = pd.to_numeric(df['Vulnerability Scan Report – Authenticated Scan'], errors='coerce') \
                           + pd.to_numeric(df['Firewall Feature Adaption'], errors='coerce') \
                           + pd.to_numeric(df['End Point Protection Total Installation (XDR)'], errors='coerce')
        df['Average Score'] = df['Total Score'] / 3
    else:
        if 'Average Score' in df.columns:
            df['Average Score'] = pd.to_numeric(df['Average Score'], errors='coerce')
        if 'Total Score' in df.columns:
            df['Total Score'] = pd.to_numeric(df['Total Score'], errors='coerce')
    dfs[sheet] = df

if search_query:
    for sheet in dfs:
        dfs[sheet] = dfs[sheet][dfs[sheet].apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

st.markdown("### Summary Metrics")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Total Colleges", f"{len(dfs['Q1'])}")
col_b.metric("Highest Avg Score", f"{dfs['Q1']['Average Score'].replace([0, None], pd.NA).dropna().max():.2f}")
col_c.metric("Lowest Avg Score", f"{dfs['Q1']['Average Score'].replace([0, None], pd.NA).dropna().min():.2f}")
col_d.metric("Total Policies", f"{len(dfs['Policy'])}")

# Navigation within the dashboard
dashboard_options = ["Overview", "Trend Q1-Q4", "Q1", "Q2", "Q3", "Q4", "Health Record", "NIST Adoption", "Policy Status", "Training Status"]
selected = st.radio("Navigation", options=dashboard_options, horizontal=True, index=0)

if selected == "Overview":
    for q in ['Q1', 'Q2', 'Q3', 'Q4']:
        st.subheader(f"{q} - Detailed Metrics")
        plot_data = dfs[q].dropna(subset=['Average Score'])
        st.plotly_chart(px.bar(plot_data, x='College Name', y='Average Score', color='Letter Grade', title=f"{q} - Average Scores"), use_container_width=True)
        st.plotly_chart(px.bar(dfs[q], x='College Name', y='Vulnerability Scan Report – Authenticated Scan', title=f"{q} - Vulnerability Scan Report"), use_container_width=True)
        st.plotly_chart(px.line(dfs[q], x='College Name', y='Firewall Feature Adaption', title=f"{q} - Firewall Feature Adaption"), use_container_width=True)
        st.plotly_chart(px.line(dfs[q], x='College Name', y='End Point Protection Total Installation (XDR)', title=f"{q} - Endpoint Protection Installation"), use_container_width=True)

elif selected == "Trend Q1-Q4":
    st.header("Trend Analysis - Average Score across Quarters")
    trend_df = pd.DataFrame({"College Name": dfs['Q1']['College Name']})
    for q in ['Q1', 'Q2', 'Q3', 'Q4']:
        trend_df[q] = dfs[q]['Average Score'].reset_index(drop=True)
    trend_melt = trend_df.melt(id_vars=["College Name"], var_name="Quarter", value_name="Average Score")
    trend_melt = trend_melt.dropna(subset=['Average Score'])
    st.plotly_chart(px.line(trend_melt, x='Quarter', y='Average Score', color='College Name', markers=True), use_container_width=True)

elif selected in ["Q1", "Q2", "Q3", "Q4"]:
    q = selected
    st.header(f"Detailed {q} Analysis")
    plot_data = dfs[q].dropna(subset=['Average Score'])
    st.plotly_chart(px.bar(plot_data, x='College Name', y='Average Score', color='Letter Grade', title=f"{q} - Average Scores"), use_container_width=True)
    st.plotly_chart(px.bar(dfs[q], x='College Name', y='Vulnerability Scan Report – Authenticated Scan', title=f"{q} - Vulnerability Scan Report"), use_container_width=True)
    st.plotly_chart(px.line(dfs[q], x='College Name', y='Firewall Feature Adaption', title=f"{q} - Firewall Feature Adaption"), use_container_width=True)
    st.plotly_chart(px.line(dfs[q], x='College Name', y='End Point Protection Total Installation (XDR)', title=f"{q} - Endpoint Protection Installation"), use_container_width=True)

elif selected == "Health Record":
    st.header("Health Record Assessment")
    st.plotly_chart(px.bar(dfs['Health Record Assesment'], x='College Name', y='Health recod assesmnet score', title="Health Record Assessment by College"), use_container_width=True)

elif selected == "NIST Adoption":
    st.header("NIST Adoption Status")
    st.plotly_chart(px.bar(dfs['NIST'], x='College Name', y='NIST Adoption', title="NIST Cybersecurity Framework Adoption"), use_container_width=True)

elif selected == "Policy Status":
    st.header("Policy Adoption / Development Status")
    st.plotly_chart(px.bar(dfs['Policy'], x='Policy Name', y='Adoption /Development', color='Adoption /Development', title="Policy Implementation Progress (CIS)"), use_container_width=True)

elif selected == "Training Status":
    st.header("Cybersecurity Awareness Training Completion")
    st.plotly_chart(px.bar(dfs['Cybersecuiry awareness Traning'], x='College Name', y='Traning Compliation status', title="Cybersecurity Training Completion by College"), use_container_width=True)

st.markdown("""
<div style='text-align:center; padding:20px; background-color:#f0f2f6; border-top:1px solid #ccc;'>
Developed with ❤️ by <a href='#' target='_blank'>Kutub Thakur</a>
</div>
""", unsafe_allow_html=True)
