import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
lol = pd.read_csv('loldata_cleaned.csv')

st.title('League of Legends Data Exploration')

st.write("""
Welcome to the League of Legends Data Exploration Dashboard! 

I have an earlier [blog post](https://jbfish00.github.io/statsofplato.github.io/2023/12/07/classic-lit-pt1.html) where I conduct some exploratory data analysis on red and blue side playstyles. I recommend you read it if you have not. Rather than reiterating what was already explained in the blog post, I figured it would be more interesting to take advantage of interactive aspects of this dashboard do explore matchups. Many of these metrics are also presented in my blog, but there are too many matchups to cover in a short post. Thus, there is a lot of supplemental information in this dashboard that is not present in my blog.

Have fun exploring!
""")

# Initialize the DataFrame
lol_df = lol.copy()

# Calculate CS Differential for each role
lol_df['Top CS Diff'] = lol_df['Blue Top CS'] - lol_df['Red Top CS']
lol_df['Mid CS Diff'] = lol_df['Blue Mid CS'] - lol_df['Red Mid CS']
lol_df['Bot CS Diff'] = lol_df['Blue Bot CS'] - lol_df['Red Bot CS']

def get_top_champions(role):
    return ['Any'] + list(lol[f'{role}'].value_counts().head(10).index)

# Function to create and display a box plot
def display_boxplot(data, title, role, color):
    column_name = f'{role} CS Diff'

    if data.empty or column_name not in data.columns:
        st.error(f"No data available or incorrect column name for plotting {title}.")
        return

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=column_name, color=color)
    plt.title(title)
    st.pyplot(plt)

# Display box plots and selection widgets for each role
for role in ['Top', 'Mid', 'Bot']:
    st.header(f'CS Differential in the {role} lane (Blue - Red)')
    st.write("""
    Compare gold efficiency in a matchup you would like to see by selecting a champion for both sides. When you select one, the boxplot will display only games where that champion was played for the team specified.
    """)
    role_df = lol.copy()  # Create a copy of the DataFrame for each role

    # Calculate CS Differential for the role
    role_df[f'{role} CS Diff'] = role_df[f'Blue {role} CS'] - role_df[f'Red {role} CS']

    blue_champions = get_top_champions(f'Blue {role}')
    red_champions = get_top_champions(f'Red {role}')

    selected_blue = st.selectbox(f'Select Blue Side {role} Laner', blue_champions, key=f'blue_{role}')
    selected_red = st.selectbox(f'Select Red Side {role} Laner', red_champions, key=f'red_{role}')

    # Apply filters based on user selection
    if selected_blue != 'Any':
        role_df = role_df[role_df[f'Blue {role}'] == selected_blue]
    if selected_red != 'Any':
        role_df = role_df[role_df[f'Red {role}'] == selected_red]

    display_boxplot(role_df, f'{role} Lane CS Differential', role, 'green')

jungle_df = lol.copy()

top_blue_junglers = get_top_champions('Blue Jungle')
top_red_junglers = get_top_champions('Red Jungle')

selected_blue_jungler = st.selectbox('Select Blue Side Jungler', top_blue_junglers)
selected_red_jungler = st.selectbox('Select Red Side Jungler', top_red_junglers)

# Apply filters based on user selection
if selected_blue_jungler != 'Any':
    jungle_df = jungle_df[jungle_df['Blue Jungle'] == selected_blue_jungler]
if selected_red_jungler != 'Any':
    jungle_df = jungle_df[jungle_df['Red Jungle'] == selected_red_jungler]

# Function to create and display a bar chart for the number of dragons
def display_bar_chart(data, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Team', y='Dragons', data=data, estimator=sum, ci=None, palette=['blue', 'red'])
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
st.write("""
Junglers are responsible for securing objectives. See which junglers have the easiest time securing dragons relative to their opponents! Similarly to the boxplots, the bar chart will filter according to the champions specified.
""")
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
    sns.scatterplot(x=x_variable, y=y_variable, data=data, color='green')
    plt.title(f'{x_variable} vs {y_variable}')
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    st.pyplot(plt)

# Display scatter plot
st.header('Objective Timing vs Game Time')
st.write("""
Choose an objective (Dragon or Rift Herald). The scatterplot will show how long games last overall relative to the time taken for the first objective to be secured.
""")
display_scatter_plot(time_df, x_axis_variable, 'Game Time')

def display_wards_plot(data, x_col, y_col, title, color):
    if data.empty or x_col not in data.columns or y_col not in data.columns:
        st.error(f"No data available for plotting {title}.")
        return

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_col, y=y_col, data=data, color=color)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)
    st.pyplot(plt)

ward_df = lol.copy()

# Selection widgets for Blue and Red Support
st.header('Ward Analysis')

top_blue_supports = get_top_champions('Blue Support')
top_red_supports = get_top_champions('Red Support')

selected_blue_support = st.selectbox('Select Blue Side Support', top_blue_supports, key='blue_support')
selected_red_support = st.selectbox('Select Red Side Support', top_red_supports, key='red_support')

# Apply filters based on user selection
if selected_blue_support != 'Any':
    ward_df = ward_df[ward_df['Blue Support'] == selected_blue_support]
if selected_red_support != 'Any':
    ward_df = ward_df[ward_df['Red Support'] == selected_red_support]

# Display scatter plots
st.subheader('Blue Team Ward Analysis')
st.write("""
Supports tend to be the primary source of vision control. See which supports perform the best compared to their opponents!
""")
display_wards_plot(ward_df, 'Red Wards Placed', 'Blue Wards Destroyed', 'Blue Team Warding vs Ward Destruction', 'blue')

st.subheader('Red Team Ward Analysis')
display_wards_plot(ward_df, 'Blue Wards Placed', 'Red Wards Destroyed', 'Red Team Warding vs Ward Destruction', 'red')
