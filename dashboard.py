import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
lol = pd.read_csv('loldata_cleaned.csv')

st.title('League of Legends Data Exploration')

# Sidebar for blue role character selection
selected_blue_top = st.sidebar.selectbox('Select Blue Side Top Laner', ['Any'] + list(lol['Blue Top'].unique()))
selected_blue_mid = st.sidebar.selectbox('Select Blue Side Mid Laner', ['Any'] + list(lol['Blue Mid'].unique()))
selected_blue_bot = st.sidebar.selectbox('Select Blue Side Bot Laner', ['Any'] + list(lol['Blue Bot'].unique()))

# Sidebar for red role character selection
selected_red_top = st.sidebar.selectbox('Select Red Side Top Laner', ['Any'] + list(lol['Red Top'].unique()))
selected_red_mid = st.sidebar.selectbox('Select Red Side Mid Laner', ['Any'] + list(lol['Red Mid'].unique()))
selected_red_bot = st.sidebar.selectbox('Select Red Side Bot Laner', ['Any'] + list(lol['Red Bot'].unique()))

# Initialize filtered DataFrame
filtered_df = lol

# Apply filters dynamically based on user selection
if selected_blue_top != 'Any':
    filtered_df = filtered_df[filtered_df['Blue Top'] == selected_blue_top]
if selected_blue_mid != 'Any':
    filtered_df = filtered_df[filtered_df['Blue Mid'] == selected_blue_mid]
if selected_blue_bot != 'Any':
    filtered_df = filtered_df[filtered_df['Blue Bot'] == selected_blue_bot]

if selected_red_top != 'Any':
    filtered_df = filtered_df[filtered_df['Red Top'] == selected_red_top]
if selected_red_mid != 'Any':
    filtered_df = filtered_df[filtered_df['Red Mid'] == selected_red_mid]
if selected_red_bot != 'Any':
    filtered_df = filtered_df[filtered_df['Red Bot'] == selected_red_bot]

# Function to create and display a box plot
def display_boxplot(data, title, role):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=f'{role} CS Diff')
    plt.title(title)
    st.pyplot(plt)

# Display box plots for each role
st.header('Top Role CS Differential')
display_boxplot(filtered_df, 'Top Role CS Differential', 'Top')

st.header('Mid Role CS Differential')
display_boxplot(filtered_df, 'Mid Role CS Differential', 'Mid')

st.header('Bot Role CS Differential')
display_boxplot(filtered_df, 'Bot Role CS Differential', 'Bot')

# Sidebar for jungler selection - Blue Side
selected_blue_jungler = st.sidebar.selectbox('Select Blue Side Jungler', ['Any'] + list(lol['Blue Jungle'].unique()))

# Sidebar for jungler selection - Red Side
selected_red_jungler = st.sidebar.selectbox('Select Red Side Jungler', ['Any'] + list(lol['Red Jungle'].unique()))

# Apply filters dynamically based on user selection
if selected_blue_jungler != 'Any':
    filtered_df = filtered_df[filtered_df['Blue Jungle'] == selected_blue_jungler]
if selected_red_jungler != 'Any':
    filtered_df = filtered_df[filtered_df['Red Jungle'] == selected_red_jungler]

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
    'Dragons': [filtered_df['Blue Dragons'].sum(), filtered_df['Red Dragons'].sum()]
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
display_scatter_plot(filtered_df, x_axis_variable, 'Game Time')
