import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime



st.set_page_config(page_title="RUS Energy Market Dashboard", layout="wide")

# For local development:
# API_URL = "http://localhost:8000"
# For deployment (Render):
API_URL = "https://your-app.onrender.com"

st.title("Russian Energy Market Dashboard")
st.markdown("Russian Energy Market: Europe vs Asia Comparison")

def fetch_records():
    """Получение всех записей по API."""
    try:
        response = requests.get(f"{API_URL}/records")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error data loading: {e}")
        return pd.DataFrame()

def add_record(timestep, consumption_eur, consumption_sib, price_eur, price_sib):
    """Добавление новой записи через API."""
    try:
        response = requests.post(
            f"{API_URL}/records",
            json={
                "timestep": timestep.strftime("%Y-%m-%d %H:%M"),
                "consumption_eur": consumption_eur,
                "consumption_sib": consumption_sib,
                "price_eur": price_eur,
                "price_sib": price_sib
            }
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding record: {e}")
        return False

def delete_record(record_id):
    """Удаление записи по id через API."""
    try:
        response = requests.delete(f"{API_URL}/records/{record_id}")
        if response.status_code == 404:
            st.error(f"Record with id {record_id} not found")
            return False
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting record: {e}")
        return False

df = fetch_records()
if not df.empty:
    df['timestep'] = pd.to_datetime(df['timestep'])

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Graphs")
        fig_consumption = px.line(
            df, 
            x='timestep', 
            y=['consumption_eur', 'consumption_sib'],
            title="Energy consumption (MW)",
            labels={'timestep': 'Time', 'value': 'Consumption', 'variable': 'Region'},
            color_discrete_map={
                'consumption_eur': 'royalblue',
                'consumption_sib': 'crimson'
            }
        )
        fig_consumption.for_each_trace(lambda t: t.update(name=t.name.replace('consumption_eur', 'Europe')
                                                    .replace('consumption_sib', 'Asia')))
        fig_consumption.update_layout(legend_title_text='Region')
        st.plotly_chart(fig_consumption, width='content')
        
        fig_prices = px.line(
            df, 
            x='timestep', 
            y=['price_eur', 'price_sib'],
            title="Energy prices (RUB/MWh)",
            labels={'timestep': 'Time', 'value': 'Price', 'variable': 'Region'},
            color_discrete_map={
                'price_eur': 'green',
                'price_sib': 'orange'
            }
        )
        fig_prices.for_each_trace(lambda t: t.update(name=t.name.replace('price_eur', 'Europe')
                                                    .replace('price_sib', 'Asia')))
        fig_prices.update_layout(legend_title_text='Region')
        st.plotly_chart(fig_prices, width='content')
    
    with col2:
        st.subheader("Add record")
        
        with st.form("add_record_form"):
            date = st.date_input("Date", datetime.now())
            time = st.time_input("Time", datetime.now().time())
            consumption_eur = st.number_input("Consumption Europe (MW)", min_value=0.0)
            consumption_sib = st.number_input("Consumption Siberia (MW)", min_value=0.0)
            price_eur = st.number_input("Price Europe (RUB/MWh)", min_value=0.0)
            price_sib = st.number_input("Price Siberia (RUB/MWh)", min_value=0.0)
            
            submitted = st.form_submit_button("Add")
            
            if submitted:
                timestep = datetime.combine(date, time)
                if add_record(timestep, consumption_eur, consumption_sib, price_eur, price_sib):
                    st.success("Record added")
                    st.rerun()
    
    st.subheader("Data table")
    col_del1, col_del2, col_del3 = st.columns([1, 1, 3])
    with col_del1:
        delete_id = st.number_input("Delete ID", min_value=1, step=1)
    with col_del2:
        if st.button("Delete"):
            if delete_record(delete_id):
                st.success(f"Record {delete_id} deleted successfully")
                st.rerun()
    
    st.dataframe(
        df.sort_values('timestep', ascending=False),
        width='content',
        hide_index=True
    )
    
else:
    st.warning("No data to be viewed")