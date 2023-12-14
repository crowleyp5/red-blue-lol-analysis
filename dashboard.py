import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    column_name = f'{role} CS Diff'
    if column_name not in data.columns or data.empty:
        st.write(f"No data available for {title}.")
        return

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=column_name)
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

# Initialize filtered DataFrame
jungle_df = lol

# Apply filters dynamically based on user selection
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
x_axis_variable = st.selectbox(
    'Select X-Axis Variable',
    ['First Dragon Time', 'First Rift Herald Time']
)

# Team filter based on the selected objective
team_filter = st.selectbox(
    'Select Team that Secured the Objective',
    ['Any', 'Blue', 'Red']
)

# Filter data based on team selection
if team_filter != 'Any':
    if x_axis_variable == 'First Dragon Time':
        time_df = lol[lol['First Dragon Team'] == team_filter]
    else:
        time_df = lol[lol['First Rift Herald Team'] == team_filter]
else:
    time_df = lol

# Function to create and display a scatter plot
def display_scatter_plot(data, x_variable, y_variable):
    # Directly use the column names as they appear in your DataFrame
    if x_variable == 'First Dragon Time':
        x_col = 'First Dragon Time'  # Replace with the exact column name from your DataFrame
    elif x_variable == 'First Rift Herald Time':
        x_col = 'First Rift Herald Time'  # Replace with the exact column name from your DataFrame

    y_col = 'Game Time'  # Replace with the exact game time column name from your DataFrame

    if data.empty or x_col not in data.columns or y_col not in data.columns:
        st.error(f"No data available or incorrect column names for plotting {x_col} vs {y_col}.")
        return

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_col, y=y_col, data=data)
    plt.title(f'{x_col} vs {y_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    st.pyplot(plt)

# Display scatter plot
st.header('Objective Timing vs Game Time')
display_scatter_plot(
    filtered_df,
    x_axis_variable.replace(' ', ''),  # Adjust column name if necessary
    'GameTime'  # Adjust column name for game time if necessary
)
