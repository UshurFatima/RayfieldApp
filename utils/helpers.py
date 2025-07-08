import pandas as pd
import streamlit as st
from utils.db import get_db_connection


def display_asset_table():
    conn = get_db_connection()
    assets = pd.read_sql("SELECT name as ASSET, status as STATUS, location as LOCATION, alerts as ALERTS FROM assets",
                         conn)
    conn.close()

    st.dataframe(
        assets,
        column_config={
            "ASSET": "ASSET",
            "STATUS": st.column_config.TextColumn(
                "STATUS",
                help="Current status of the asset",
                default="Normal",
            ),
            "LOCATION": "LOCATION",
            "ALERTS": st.column_config.NumberColumn(
                "ALERTS",
                help="Number of active alerts",
                format="%d",
            ),
        },
        hide_index=True,
        use_container_width=True
    )


def display_reports():
    st.subheader("Reports Dashboard")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Maintenance Summary", "78%")
    with col2:
        st.metric("Technician Performance", "45")
    with col3:
        st.metric("Downtime Analysis", "75%")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Work Orders", "135")
    with col2:
        st.metric("Cost Analysis", "1000")
    with col3:
        st.metric("Equipment Overview", "90%")