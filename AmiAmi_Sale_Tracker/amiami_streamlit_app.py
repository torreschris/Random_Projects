import streamlit as st
import pandas as pd
#import os
import requests
from datetime import datetime
import pytz

# GitHub repo details
owner = "jon-AG"
repo = "AmiAmi-Sales"
file_path = "AmiAmi_sales.csv"

# GitHub API URL for file commits
url = f"https://api.github.com/repos/{owner}/{repo}/commits?path={file_path}&per_page=1"

# Make a request
response = requests.get(url)
pst_time = ''
if response.status_code == 200:
    commit_data = response.json()
    if commit_data:
        creation_date = commit_data[-1]["commit"]["committer"]["date"]
        # Given UTC time in ISO 8601 format
        utc_time_str = creation_date

        # Convert to a datetime object
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")

        # Define timezones
        utc_zone = pytz.utc
        pst_zone = pytz.timezone("America/Los_Angeles")

        # Convert UTC to PST
        utc_time = utc_zone.localize(utc_time)  # Mark as UTC timezone
        pst_time = utc_time.astimezone(pst_zone)  # Convert to PST
    else:
        pass
else:
    pass

st.set_page_config(layout="wide")
cols = st.columns(2)
with cols[0]:
    st.title('AmiAmi Sale Tracker!')
with cols[1]:
    st.image('https://www.amiami.com/images/common/site_logo.png')

#csv_file = 'https://raw.githubusercontent.com/jon-AG/AmiAmi-Sales/a086ec56a75a9ba987f91d3185889c67f2f56f33/AmiAmi_sales.csv'
# dir_path = os.path.dirname(os.path.realpath(__file__))
# csv_file = 'AmiAmi_sales.csv'
# csv_file = os.path.join(dir_path, csv_file)

csv_file = 'https://raw.githubusercontent.com/jon-AG/AmiAmi-Sales/refs/heads/main/AmiAmi_sales.csv'



df = pd.read_csv(csv_file,delimiter='|',header=0)

with st.sidebar:
    st.image('https://img.amiami.com/images/genre/icon/1001.png')
    reload = st.button('Reload',use_container_width=True)
    if reload:
        df = pd.read_csv(csv_file,delimiter='|',header=0)
    st.write('Last updated:')
    st.write(pst_time.strftime("%Y-%m-%d %I:%M:%S %p %Z"))
    
    st.divider()

    filter_title = st.multiselect('Filter on Title',df['Title'])
    if filter_title:
        df = df[df['Title'].isin(filter_title)]
    
c = st.columns(4)
with c[0]:
    sortby = st.selectbox('Sort by',df.columns,index=df.columns.get_loc("Discount"))
    if sortby == "Discount":
        df["Discount"] = df["Discount"].str.rstrip("%").astype(float)
    elif sortby == "Original Price":
        df["Original Price"] = df["Original Price"].str.replace("JPY","")
        df["Original Price"] = df["Original Price"].str.replace(",","").astype(int)
    elif sortby == "Discounted Price":
        df["Discounted Price"] = df["Discounted Price"].str.replace("JPY","")
        df["Discounted Price"] = df["Discounted Price"].str.replace(",","").astype(int)

    if sortby:
        df = df.sort_values(by=sortby,ascending=True)

with c[1]:
    ordering = st.selectbox('Ascending or Descending',['Ascending','Descending'],index=1)
    if ordering == 'Descending':
        df = df.sort_values(by=sortby,ascending=False)
    
    if sortby == "Discount":
        df["Discount"] = df["Discount"].round(2).astype(str) + "%"
    elif sortby == "Original Price":
        df["Original Price"] = df["Original Price"].apply(lambda x: f"{x:,} JPY")
    elif sortby == "Discounted Price":
        df["Discounted Price"] = df["Discounted Price"].apply(lambda x: f"{x:,} JPY")


st.write(df.to_markdown(index=False), unsafe_allow_html=True)