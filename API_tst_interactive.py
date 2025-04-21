import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

# --- API Functions ---

# Function 1: Get all columns
def Customer_App_Column():
    url = "https://api.l2datamapping.com"
    call = "/api/v2/customer/application/columns/USER_NAME_HERE/VM_MI?id=1DBB&apikey=INSERT_API_KEY_HERE"
    return requests.get(url + call)

# Function 2: Get values for a specific column
def Customer_App_Column_Values(Column):
    url = "https://api.l2datamapping.com"
    

        
    call="/api/v2/customer/application/column/values/USER_NAME_HERE/VM_MI/" + Column  + "?&id=INSERT_API_KEY_HERE&"
    
    return requests.get(url + call)

# Function 3: Get stats
def Customer_App_Column_Stats(Column, Filter, FilterValue):
    url = "https://api.l2datamapping.com"
    base = "/api/v2/customer/application/stats/USER_NAME_HERE/VM_MI?"
    params = (
        f"id=&"
        f"view.{Column}&filter.{Filter}={FilterValue}"
    )
    return requests.get(url + base + params)

# --- Streamlit UI ---

st.set_page_config(page_title="Customer Data Explorer", layout="wide")
st.title("📊 Customer App Column Explorer")

# 1. Get list of columns
with st.spinner("Fetching available columns..."):
    response = Customer_App_Column()

    if response.status_code == 200:
        columns_data = response.json()
        
        hldr3 = pd.DataFrame(columns_data["columns"])
        columns_list = hldr3[hldr3["id"].str.startswith("hf")]["id"]
        
    else:
        st.error("Failed to fetch columns.")
        st.stop()

# 2. Column selection
filter_col = st.selectbox("🔎 Select a column to use as a filter", columns_list)
value_col = st.selectbox("📘 Select another column to get values from", columns_list)
print(value_col)
# 3. Get possible values for selected column
with st.spinner("Getting values..."):
    
    values_response2 = Customer_App_Column_Values(filter_col)
    values_response =  pd.DataFrame(values_response2.json()["values"]).rename(columns={0:"values"})
    if values_response2.status_code == 200:
        values= values_response["values"]
    else:
        st.error("Failed to fetch column values.")
        st.stop()

selected_value = st.selectbox("🔢 Choose a value for the selected column", values)

# 4. Fetch and display stats
if st.button("📈 Get Stats"):
    with st.spinner("Fetching statistics..."):
        print(filter_col)
        print(value_col)
        print(selected_value)
        stats_response = Customer_App_Column_Stats(Column=value_col, Filter=filter_col, FilterValue=selected_value)
        if stats_response.status_code == 200:
            stats_json = stats_response.json()
            stats_df = pd.DataFrame(stats_json.get("statistics", []))

            if not stats_df.empty:
                stats_df.reset_index(inplace=True)
                stats_df.rename(columns={"index": "Row"}, inplace=True)
                
                st.subheader("📊 Result Table")
                gb = GridOptionsBuilder.from_dataframe(stats_df)
                gb.configure_pagination()
                gb.configure_side_bar()
                gb.configure_default_column(editable=False, groupable=True)
                grid_options = gb.build()

                AgGrid(stats_df, gridOptions=grid_options, theme="material")
            else:
                st.info("No data returned from the stats query.")
        else:
            st.error("Failed to fetch stats.")
            
            
# streamlit run API_tst_interactive.py
# cd "C:\Users\Elijah Work\OneDrive - Digital Strategies\Desktop\Python Module Testing"