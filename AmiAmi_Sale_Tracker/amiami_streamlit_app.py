import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

#csv_file = 'https://raw.githubusercontent.com/jon-AG/AmiAmi-Sales/a086ec56a75a9ba987f91d3185889c67f2f56f33/AmiAmi_sales.csv'
csv_file = 'AmiAmi_sales.csv'
st.title('AmiAmi Sale Tracker!')

df = pd.read_csv(csv_file,delimiter='|',header=1)

with st.sidebar:
    filter_title = st.multiselect('Filter on Title',df['Title'])
    if filter_title:
        df = df[df['Title'].isin(filter_title)]

df["Discount"] = df["Discount"].str.rstrip("%").astype(float)

c = st.columns(4)
with c[0]:
    sortby = st.selectbox('Sort by',df.columns,index=0)
    if sortby:
        df = df.sort_values(by=sortby,ascending=True)
with c[1]:
    ordering = st.selectbox('Ascending or Descending',['Ascending','Descending'])
    if ordering == 'Descending':
        df = df.sort_values(by=sortby,ascending=False)

df["Discount"] = df["Discount"].round(2).astype(str) + "%"
st.write(df.to_markdown(), unsafe_allow_html=True)


