import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="UAC System Capacity Analytics", page_icon="🏥", layout="wide")
st.title("System Capacity & Care Load Analytics for Unaccompanied Children")
st.markdown("Monitoring system stress and care pipeline dynamics for the HHS UAC Program.")

# --- 2. DATA LOADING & ENGINEERING ---
# @st.cache_data ensures the app doesn't reload and clean the CSV every time you click a filter
@st.cache_data
def load_and_clean_data():
    # Load the dataset
    df = pd.read_csv('HHS_Unaccompanied_Alien_Children_Program.csv')
    
    # Dynamic Column Mapping (Handles variations, trailing spaces, or asterisks in Gov data)
    new_cols = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'date' in col_lower: new_cols[col] = 'Date'
        elif 'apprehended' in col_lower: new_cols[col] = 'Daily_Intake'
        elif 'transferred' in col_lower: new_cols[col] = 'Transferred_Out_CBP'
        elif 'cbp custody' in col_lower: new_cols[col] = 'CBP_Custody'
        elif 'discharged' in col_lower: new_cols[col] = 'HHS_Discharged'
        elif 'hhs care' in col_lower: new_cols[col] = 'HHS_Care'
    df = df.rename(columns=new_cols)
    
    # Clean Numbers (Remove commas from numbers like "1,500" and convert to float)
    numeric_cols = ['Daily_Intake', 'CBP_Custody', 'Transferred_Out_CBP', 'HHS_Care', 'HHS_Discharged']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            
    # Time-Series Indexing
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.set_index('Date', inplace=True)
    
    # --- Derived Healthcare Capacity Metrics ---
    # 1. Total humanitarian footprint
    df['Total_System_Load'] = df['CBP_Custody'] + df['HHS_Care']
    
    # 2. Are we taking in more than we are releasing?
    df['Net_Daily_Intake'] = df['Transferred_Out_CBP'] - df['HHS_Discharged']
    
    # 3. 7-Day sustained backlog warning
    df['Backlog_Accumulation'] = df['Net_Daily_Intake'].rolling(window=7).sum()
    
    # 4. Pipeline flow ratio (<1.0 means bottlenecking)
    df['Discharge_Offset_Ratio'] = np.where(
        df['Transferred_Out_CBP'] == 0, 0, 
        df['HHS_Discharged'] / df['Transferred_Out_CBP']
    )
    
    return df

# Load the data using the function above
df = load_and_clean_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Controls")
st.sidebar.markdown("Use these controls to narrow down specific timeframes, such as sudden influx periods.")

start_date = st.sidebar.date_input("Start Date", df.index.min())
end_date = st.sidebar.date_input("End Date", df.index.max())

# Apply filters
mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]


# --- 4. KPI SUMMARY CARDS ---
st.subheader("Current System Status (End of Selected Period)")
col1, col2, col3, col4 = st.columns(4)

latest_load = filtered_df['Total_System_Load'].iloc[-1]
latest_backlog = filtered_df['Backlog_Accumulation'].iloc[-1]
avg_offset = filtered_df['Discharge_Offset_Ratio'].mean()
latest_net_intake = filtered_df['Net_Daily_Intake'].iloc[-1]

col1.metric("Total Children Under Care", f"{latest_load:,.0f}")
col2.metric("7-Day Backlog Accumulation", f"{latest_backlog:,.0f}", 
            help="Sum of Net Daily Intake over the last 7 days. Positive numbers indicate growing strain.")
col3.metric("Avg Discharge Offset Ratio", f"{avg_offset:.2f}", 
            help="Ratio of Discharges to Intake. Below 1.0 indicates a bottleneck in sponsor placements.")
col4.metric("Net Daily Intake", f"{latest_net_intake:,.0f}")

st.markdown("---")

# --- 5. INTERACTIVE CHARTS ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Care Load Dynamics")
    st.markdown("Visualizing the total volume of children across both CBP and HHS facilities.")
    
    fig_load = px.area(filtered_df, x=filtered_df.index, y=['CBP_Custody', 'HHS_Care'],
                       labels={'value': 'Number of Children', 'variable': 'Facility Type'},
                       color_discrete_map={'CBP_Custody': '#EF553B', 'HHS_Care': '#636EFA'})
    # Move legend to top
    fig_load.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_load, use_container_width=True)

with col_chart2:
    st.subheader("System Pressure Indicators")
    st.markdown("Tracking net intake against the 7-day rolling backlog to identify sustained strain.")
    
    fig_pressure = px.line(filtered_df, x=filtered_df.index, y=['Net_Daily_Intake', 'Backlog_Accumulation'],
                           labels={'value': 'Count', 'variable': 'Metric'})
    # Add a horizontal line at 0 (the balance point)
    fig_pressure.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="System Balance Point")
    fig_pressure.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_pressure, use_container_width=True)
