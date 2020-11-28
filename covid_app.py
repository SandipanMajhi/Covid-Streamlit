import pandas as pd
import numpy as np
from datetime import datetime
#import json
import plotly.express as px
import streamlit as st

st.title("Daily India Covid-19 Numbers")
st.markdown("Untick the 'Hide' boxes to visualize")

st.sidebar.title("Options ")


dft_url = "https://api.covid19india.org/csv/latest/case_time_series.csv"
dfs_url = "https://api.covid19india.org/csv/latest/states.csv"
dfsw_url = "https://api.covid19india.org/csv/latest/state_wise.csv"
dfsd_url = "https://api.covid19india.org/csv/latest/state_wise_daily.csv"
dfsc_url = "state wise centroids_2011.csv"
dw_url = "https://api.covid19india.org/csv/latest/district_wise.csv"
dwc_url = "district wise centroids.csv"


mapaccess_token = 'pk.eyJ1IjoiYm9vc2FuZHkiLCJhIjoiY2toaXZ4aDNmMWZkazJ5bHVreWlzY2szNCJ9.zHu7eImER0mCoyvny-_30w'

#@st.cache(persist = True)

def load_dft():
    dft = pd.read_csv(dft_url)
    return dft

def load_dfs():
    dfs = pd.read_csv(dfs_url)
    return dfs

def load_dfsw():
    dfsw = pd.read_csv(dfsw_url)
    return dfsw

def load_dfsd():
    dfsd = pd.read_csv(dfsd_url)
    return dfsd

def load_dfsc():
    dfsc = pd.read_csv(dfsc_url)
    return dfsc  

def load_dw():
    dw = pd.read_csv(dw_url) 
    return dw

def load_dwc():
    dwc = pd.read_csv(dwc_url)
    return dwc        

#change the dates to datetime objects    
def change_dates():
    for i in range(dft.shape[0]):
        dft.iloc[i,1] = datetime.strptime(dft.iloc[i,1], "%Y-%m-%d") 



dft = load_dft()
dfs = load_dfs()
dfsw = load_dfsw()
dfsd = load_dfsd()
dfsc = load_dfsc() 
dw = load_dw()
dwc = load_dwc()
d = dw.merge(dwc,on= ["District","State"], how = "inner")

styling_html2 = """ 
    <style>
        
        h3{
            text-align:left;
        }
    </style>
    <div style = 'display:flex'>
        <h3 style = 'color:#FF7F01;margin-top:0px;'>Confirmed : """ + str(dfsw.head(1).iloc[0,1])+""" | +"""+ str(dft.tail(1).iloc[0,2])+"""</h3>
        <div></div>
        <h3 style = 'color:#023BFF;margin-left:50px;margin-top:0px;'>Active : """ + str(dfsw.head(1).iloc[0,4])+""" </h3>
    </div>
    <div style = 'display:flex'>
        <h3 style = 'color:#4DE001;margin-top:0px;'>Recovered : """ + str(dfsw.head(1).iloc[0,2])+""" | +"""+ str(dft.tail(1).iloc[0,4])+""" </h3>
        <h3 style = 'color:#FE0000;margin-left:50px;margin-top:0px;'>Deaths : """ + str(dfsw.head(1).iloc[0,3])+""" | +"""+ str(dft.tail(1).iloc[0,6])+""" </h3>
    </div>     
        """         

dft.tail(1).to_csv("last_update.csv",index = False)

#omitted the styling_html1 
st.markdown(styling_html2,unsafe_allow_html=True)

#plotting the time series graphs here
st.sidebar.subheader("Time series Plots")
s_plots = st.sidebar.selectbox("Modes",['Total Confirmed', 'Total Recovered','Total Deaths','Daily Confirmed', 'Daily Recovered', 'Daily Deaths'],key = '0')
if not st.sidebar.checkbox("Hide",True,key = '0_1'):
    if s_plots == 'Total Confirmed':
        st.markdown("Covid Confirmed Cases Time Series for Whole India")
        fig = px.scatter(dft, x = 'Date_YMD', y = 'Total Confirmed', labels = {'Date_YMD':'Time'}, color = 'Daily Confirmed')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)
    elif s_plots == "Total Recovered":
        st.markdown("Covid Recovery Cases Time Series for Whole India")
        fig = px.scatter(dft, x = 'Date_YMD', y = 'Total Recovered', labels = {'Date_YMD':'Time'}, color = 'Daily Recovered')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)   
    elif s_plots == "Total Deaths":
        st.markdown("Covid Deaths Time-series for Whole India ") 
        fig = px.scatter(dft, x = 'Date_YMD', y = 'Total Deceased', labels = {'Date_YMD':'Time'}, color = 'Daily Deceased')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig) 
    elif s_plots == "Daily Confirmed":
        st.markdown("Covid Daily Confirmed Trends ") 
        fig = px.scatter(dft, x = 'Date_YMD', y = 'Daily Confirmed', labels = {'Date_YMD':'Time'}, color = 'Daily Confirmed')   
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})  
        st.plotly_chart(fig)
    elif s_plots == "Daily Recovered":
        st.markdown("Covid Daily Recovery Trends ") 
        fig = px.scatter(dft, x = 'Date_YMD', y = 'Daily Recovered', labels = {'Date_YMD':'Time'}, color = 'Daily Recovered')   
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})  
        st.plotly_chart(fig) 
    elif s_plots == "Daily Deaths":
        st.markdown("Covid Daily Death Trends ") 
        fig = px.scatter(dft, x = 'Date_YMD', y = 'Daily Deceased', labels = {'Date_YMD':'Time'}, color = 'Daily Deceased')   
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})  
        st.plotly_chart(fig)         


#plotting the state wise numbers
st.sidebar.subheader("All State/ District")
select = st.sidebar.selectbox("Select",["State-Wise","District-Wise"],key = '1')
select_mode = st.sidebar.selectbox("Mode",['Active','Confirmed','Recovered','Deaths'],key='1_1_1')
if not st.sidebar.checkbox("Hide",True,key='1_1'):
    if select == "State-Wise":
        dfsw_new = dfsw.merge(dfsc,on="State",how = "inner")
        if select_mode == "Active":
            st.markdown("Active Cases ")
            fig = px.scatter_mapbox(dfsw_new, lon = "Longitude", lat = "Latitude", hover_name = "State", size = "Active" ,
                            hover_data = ["Active","Deaths", "Last_Updated_Time"], size_max = 60,
                            color = "Active",zoom=3.5, height=500, color_continuous_scale="viridis")
            fig.update_layout(mapbox_style='light', mapbox_accesstoken=mapaccess_token)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)
        elif select_mode == "Confirmed":
            st.markdown("Confirmed Cases ")
            fig = px.scatter_mapbox(dfsw_new, lon = "Longitude", lat = "Latitude", hover_name = "State", size = "Confirmed" ,
                            hover_data = ["Confirmed", "Recovered", "Deaths", "Last_Updated_Time"], size_max = 60,
                            color = "Confirmed", zoom=3.5, height=500, color_continuous_scale="dense")
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig) 
        elif select_mode == "Recovered":
            st.markdown("Recovery Cases ")
            fig = px.scatter_mapbox(dfsw_new, lon = "Longitude", lat = "Latitude", hover_name = "State", size = "Recovered",
                            hover_data = ["Confirmed", "Recovered", "Deaths", "Last_Updated_Time"], size_max = 60,
                            color = "Recovered", zoom=3.5, height=500, color_continuous_scale="YlGn")
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)    
        elif select_mode == "Deaths":    
            st.markdown("Deceased Cases ")
            fig = px.scatter_mapbox(dfsw_new, lon = "Longitude", lat = "Latitude", hover_name = "State", size = "Deaths",
                            hover_data = ["Confirmed", "Recovered", "Deaths", "Last_Updated_Time"], size_max = 60,
                            color = "Deaths", zoom=3.5, height=500, color_continuous_scale="YlOrRd")
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)
    elif select == "District-Wise":  
        if select_mode == "Confirmed": 
            fig = px.scatter_mapbox(d,lon = "Longitude", lat = "Latitude", hover_name = "District", size = "Confirmed" ,
                            hover_data = ["State","Confirmed", "Recovered", "Deceased"], size_max = 45,
                            color = "Confirmed", zoom=3.5, height=500, color_continuous_scale="dense")       
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)   
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)                  
        elif select_mode == "Recovered":
            fig = px.scatter_mapbox(d,lon = "Longitude", lat = "Latitude", hover_name = "District", size = "Recovered" ,
                            hover_data = ["State","Confirmed", "Recovered", "Deceased"], size_max = 45,
                            color = "Recovered", zoom=3.5, height=500, color_continuous_scale="YlGn")       
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)   
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig) 
        elif select_mode == "Deaths":
            fig = px.scatter_mapbox(d,lon = "Longitude", lat = "Latitude", hover_name = "District", size = "Deceased" ,
                            hover_data = ["State","Confirmed", "Recovered", "Deceased"], size_max = 45,
                            color = "Deceased", zoom=3.5, height=500, color_continuous_scale="YlOrRd")       
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)   
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)             

# Plotting state specific data
st.sidebar.subheader("State Specific Visuals")
s_list = [ 'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Assam',
       'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Goa',
       'Gujarat', 'Karnataka', 'Kerala', 'Maharashtra', 'Rajasthan',
       'Telangana', 'Tamil Nadu', 'West Bengal', 'Arunachal Pradesh',
       'Bihar', 'Chandigarh', 'Uttar Pradesh', 'Himachal Pradesh',
       'Delhi', 'Haryana', 'Jharkhand', 'Jammu and Kashmir', 'Ladakh',
       'Meghalaya', 'Manipur', 'Madhya Pradesh', 'Mizoram', 'Nagaland',
       'Odisha', 'Punjab', 'Puducherry', 'Sikkim', 'Tripura',
       'Uttarakhand']
s_list.sort()       
s_states = st.sidebar.multiselect("Pick States",s_list,key='2')
select_mode2 = st.sidebar.selectbox("Mode",['Confirmed','Recovered','Deaths'],key='2_1_1')
if not st.sidebar.checkbox("Hide",True,key = "2_1"):
    d_states = d[d.State.isin(s_states)]
    if len(s_states) > 0 :
        if select_mode2 == "Confirmed":
            fig = px.scatter_mapbox(d_states,lon = "Longitude", lat = "Latitude", hover_name = "District", size = "Confirmed" ,
                                hover_data = ["State","Confirmed", "Recovered", "Deceased"], size_max = 30,
                                color = "Confirmed", zoom=3.5, height=500, color_continuous_scale="dense",range_color = [0,max(d.Confirmed)])
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)   
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)
        elif select_mode2 == "Recovered":
            fig = px.scatter_mapbox(d_states,lon = "Longitude", lat = "Latitude", hover_name = "District", size = "Recovered" ,
                                hover_data = ["State","Confirmed", "Recovered", "Deceased"], size_max = 30,
                                color = "Recovered", zoom=3.5, height=500, color_continuous_scale="YlGn",range_color = [0,max(d.Recovered)])
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)   
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)
        elif select_mode2 == "Deaths":
            fig = px.scatter_mapbox(d_states,lon = "Longitude", lat = "Latitude", hover_name = "District", size = "Deceased" ,
                                hover_data = ["State","Confirmed", "Recovered", "Deceased"], size_max = 30,
                                color = "Deceased", zoom=3.5, height=500, color_continuous_scale="YlOrRd",range_color = [0,max(d.Deceased)])
            fig.update_layout(mapbox_style='dark', mapbox_accesstoken=mapaccess_token)   
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)        
    else:
        st.markdown("<h2 style='color:red'> Please Select Some States</h2>", unsafe_allow_html = True)    

# # Plotting the state Performances
# st.sidebar.subheader("State Performance")
# s_state_p = st.sidebar.selectbox("Pick State",s_list,key = '3')
# if not st.sidebar.checkbox("Hide",True,key="3_1"):
#     st_daily = d[["State_Code","State"]]
#     st_daily.set_index("State_Code", drop = True, inplace = True)
#     st_daily = st_daily.to_dict()['State']
#     st_daily_rev = {v : k for k,v in st_daily.items()}
#     dfsd_sliced = dfsd[["Date_YMD",'Status',st_daily_rev[s_state_p]]]





st.sidebar.subheader("Last Update: " + str(dfsw.head(1).iloc[0,5]))      
