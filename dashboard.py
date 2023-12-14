import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
lol = pd.read_csv('loldata_cleaned.csv')

st.title('League of Legends Data Exploration')

# Sidebar for role character selection
selected_blue_top = st.sidebar.selectbox('Select Blue Side Top Laner', ['Any'] + list(lol['Blue Top'].unique()))
selected_blue_mid = st.sidebar.selectbox('Select Blue Side Mid Laner', ['Any'] + list(lol['Blue Mid'].unique()))
selected_blue_bot = st.sidebar.selectbox('Select Blue Side Bot Laner', ['Any'] + list(lol['Blue Bot'].unique()))
selected_red_top = st.sidebar.selectbox('Select Red Side Top Laner', ['Any'] + list(lol['Red Top'].unique()))
selected_red_mid = st.sidebar.selectbox('Select Red Side Mid Laner', ['Any'] + list(lol['Red Mid'].unique()))
selected_red_bot = st.sidebar.selectbox('Select Red Side Bot Laner', ['Any'] + list(lol['Red Bot'].unique()))

# Initialize separate DataFrames for each plot
cs_df = lol.copy()
jungle_df = lol.copy()
time_df = lol.copy()

# Apply filters for CS Differential plots
if selected_blue_top != 'Any':
    cs_df = cs_df[cs_df['Blue Top'] == selected_blue_top]
if selected_blue_mid != 'Any':
    cs_df = cs_df[cs_df['Blue Mid'] == selected_blue_mid]
if selected_blue_bot != 'Any':
    cs_df = cs_df[cs_df['Blue Bot'] == selected_blue_bot]
if selected_red_top != 'Any':
    cs_df = cs_df[cs_df['Red Top'] == selected_red_top]
if selected_red_mid != 'Any':
    cs_df = cs_df[cs_df['Red Mid'] == selected_red_mid]
if selected_red_bot != 'Any':
    cs_df = cs_df[cs_df['Red Bot'] == selected_red_bot]

# Function to create and display a box plot
def display_boxplot(data, title, role):
    # Construct the correct column name based on your DataFrame
    column_name = f'{role} CS Diff'  # Adjust this to match your DataFrame's actual column name

    # Check if the DataFrame is empty or the column name is not present
    if data.empty or column_name not in data.columns:
        st.error(f"No data available or incorrect column name for plotting {title}.")
        return

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=column_name)
    plt.title(title)
    st.pyplot(plt)

# Display box plots for each role
st.header('Top Role CS Differential')
display_boxplot(cs_df, 'Top Role CS Differential', 'Top')

st.header('Mid Role CS Differential')
display_boxplot(cs_df, 'Mid Role CS Differential', 'Mid')

st.header('Bot Role CS Differential')
display_boxplot(cs_df, 'Bot Role CS Differential', 'Bot')

selected_blue_jungler = st.sidebar.selectbox('Select Blue Side Jungler', ['Any'] + list(lol['Blue Jungle'].unique()))
selected_red_jungler = st.sidebar.selectbox('Select Red Side Jungler', ['Any'] + list(lol['Red Jungle'].unique()))

if selected_blue_jungler != 'Any':
    jungle_df = jungle_df[jungle_df['Blue Jungle'] == selected_blue_jungler]
if selected_red_jungler != 'Any':
    jungle_df = jungle_df[jungle_df['Red Jungle'] == selected_red_jungler]

# Function to create and display a bar chart for the number of dragons
def display_bar_chart(data, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Team', y='Dragons', data=data, estimator=sum, ci=None)
    plt.title(title)
    plt.xlabel('Team')
    plt.ylabel('Total Number of Dragons')
    st.pyplot(plt)

# Preparing data for the bar chart
dragon_data = pd.DataFrame({
    'Team': ['Blue', 'Red'],
    'Dragons': [jungle_df['Blue Dragons'].sum(), jungle_df['Red Dragons'].sum()]
})

# Display bar chart for the number of dragons
st.header('Dragon Control Analysis')
display_bar_chart(dragon_data, 'Total Number of Dragons Secured by Each Team')

# Dropdown for X-Axis Selection
x_axis_variable = st.selectbox('Select X-Axis Variable', ['First Dragon Time', 'First Rift Herald Time'])

# Function to create and display a scatter plot
def display_scatter_plot(data, x_variable, y_variable):
    if data.empty or x_variable not in data.columns or y_variable not in data.columns:
        st.error(f"No data available or incorrect column names for plotting {x_variable} vs {y_variable}.")
        return

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_variable, y=y_variable, data=data)
    plt.title(f'{x_variable} vs {y_variable}')
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    st.pyplot(plt)

# Display scatter plot
st.header('Objective Timing vs Game Time')
display_scatter_plot(time_df, x_axis_variable, 'Game Time')
