import streamlit as st
import pandas as pd
#import os

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

    st.image('https://img.amiami.com/images/genre/icon/1000.png',use_container_width=True)
    reload = st.button('Reload',use_container_width=True)
    if reload:
        df = pd.read_csv(csv_file,delimiter='|',header=0)

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