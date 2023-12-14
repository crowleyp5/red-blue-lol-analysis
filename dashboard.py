import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
lol = pd.read_csv('loldata_cleaned.csv')

st.title('League of Legends Data Exploration')

# Initialize the DataFrame
lol_df = lol.copy()

# Calculate CS Differential for each role
lol_df['Top CS Diff'] = lol_df['Blue Top CS'] - lol_df['Red Top CS']
lol_df['Mid CS Diff'] = lol_df['Blue Mid CS'] - lol_df['Red Mid CS']
lol_df['Bot CS Diff'] = lol_df['Blue Bot CS'] - lol_df['Red Bot CS']

# Function to create and display a box plot
def display_boxplot(data, title, role):
    column_name = f'{role} CS Diff'

    if data.empty or column_name not in data.columns:
        st.error(f"No data available or incorrect column name for plotting {title}.")
        return

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=column_name)
    plt.title(title)
    st.pyplot(plt)

# Display box plots and selection widgets for each role
for role in ['Top', 'Mid', 'Bot']:
    st.header(f'{role} Role CS Differential')
    selected_blue = st.selectbox(f'Select Blue Side {role} Laner', ['Any'] + list(lol_df[f'Blue {role}'].unique()), key=f'blue_{role}')
    selected_red = st.selectbox(f'Select Red Side {role} Laner', ['Any'] + list(lol_df[f'Red {role}'].unique()), key=f'red_{role}')

    # Apply filters based on user selection
    if selected_blue != 'Any':
        lol_df = lol_df[lol_df[f'Blue {role}'] == selected_blue]
    if selected_red != 'Any':
        lol_df = lol_df[lol_df[f'Red {role}'] == selected_red]

    display_boxplot(lol_df, f'{role} Role CS Differential', role)

jungle_df - lol.copy()

selected_blue_jungler = st.selectbox('Select Blue Side Jungler', ['Any'] + list(lol['Blue Jungle'].unique()))
selected_red_jungler = st.selectbox('Select Red Side Jungler', ['Any'] + list(lol['Red Jungle'].unique()))

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

time_df = lol.copy()

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
