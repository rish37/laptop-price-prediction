
import pandas as pd
import streamlit as st
import plotly.express as px
import warning 

st.set_page_config(page_title='Laptop Data Analysis')


@st.cache
def load_data():
    df = pd.read_csv('laptop_data.csv')
    df['ram'] = df['ram'].str.replace('GB','').astype('int32')
    df['weight'] = df['weight'].str.replace('kg','').astype('float32')
    new = df['screen resolution'].str.split('x', n=1, expand=True)
    df['X_res'] = new[0].str.replace(',','').str.findall(r'(\d+\.?\d+)').apply(lambda x:x[0]).astype('int')
    df['Y_res'] = new[1].astype('int')
    df['ppi'] = (((df['X_res']**2) + (df['Y_res']**2))**0.5/df['inches']).astype('float')
    df.drop(columns=['inches','X_res','Y_res'], inplace=True)
    df['memory'] = df['memory'].astype(str).replace('\.0', '', regex=True)
    df['memory'] = df['memory'].str.replace('GB', '')
    df['memory'] = df['memory'].str.replace('TB', '000')
    df['memory'] = df['memory'].apply(
     lambda x: sum(int(i) for i in x.split('+')) if all(i.isdigit() for i in x.split('+')) else None)
    df['Touchscreen'] = df['screen resolution'].apply(lambda x: 1 if 'Touchscreen' in x else 0)
    df['gpu'] = df['screen resolution'].apply(lambda x: 1 if 'gpu' in x else 0)
    df['cpu Name'] = df['cpu'].apply(lambda x: " ".join(x.split()[0:3]))
    df['cpu brand'] = df['cpu Name'].apply(lambda x: x if x in ['Intel Core i7', 'Intel Core i5', 'Intel Core i3'] else 'Other Intel Processor' if x.startswith('Intel') else 'AMD Processor')
    df.drop(columns=['cpu', 'cpu Name', 'Unnamed: 0'], inplace=True)
    return df

df = load_data()
if df.empty:
 st.write("Data not loaded properly.")


st.title('Laptop Data Analysis')
st.write('This app analyzes the laptop data and provides insights into various aspects of laptops.')

if st.checkbox('Show raw data'):
    st.write(df)
# Plotting functions
def plot_bar(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title, height=400)
    st.plotly_chart(fig)

def plot_hist(df, column, title):
    fig = px.histogram(df, x=column, title=title, height=400)
    st.plotly_chart(fig)

def plot_scatter(df, x, y, title):
    fig = px.scatter(df, x=x, y=y, title=title, height=400)
    st.plotly_chart(fig)

# Data analysis
st.header('Data Analysis')
st.write('This section provides some insights into the laptop data.')

plot_hist(df, 'price', 'Price Distribution')
plot_bar(df, 'company', 'price', 'Company-wise Distribution of Laptops')
plot_bar(df, 'type name', 'price','Type Name-wise Distribution of Laptops')
plot_hist(df, 'screen resolution', 'Screen Resolution Distribution')
plot_hist(df, 'ram', 'RAM Distribution')
plot_hist(df, 'weight', 'Weight Distribution')
plot_hist(df, 'ppi', 'PPI Distribution')


# Touchscreen vs Non-Touchscreen laptops
df_touch = df.groupby('Touchscreen')['price'].count().reset_index()
df_touch['Touchscreen'] = df_touch['Touchscreen'].apply(lambda x: 'Yes' if x == 1 else 'No')
plot8 = px.bar(df_touch, x='Touchscreen', y='price', title='Touchscreen vs Non-Touchscreen Laptops')
st.plotly_chart(plot8)

# CPU brand-wise distribution of laptops
plot10 = px.bar(df, x='cpu brand', y='price', title='CPU Brand-wise Distribution of Laptops')
st.plotly_chart(plot10)


