# -*- coding: utf-8 -*-
"""Untitled19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/127ddIgejc4ME--GI5DXA-pQTK23oIvhP
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress
import six

lol = pd.read_csv('loldata_cleaned.csv')
lol.head(5)

df_display = lol.head(5)  # Displaying the first 5 rows for example

fig, ax = plt.subplots(figsize=(12, 2))  # Adjust figure size as needed
ax.axis('off')
the_table = ax.table(cellText=df_display.values, colLabels=df_display.columns, loc='center', cellLoc='center')

the_table.auto_set_font_size(False)
the_table.set_fontsize(10)
the_table.scale(1, 1.5)

# Save the table as an image
plt.savefig('df_head.png', bbox_inches='tight', pad_inches=0.05)
plt.show()

# Show top champion picks
def get_top_picks(lol, role, team_color):
    role_column = f'{team_color} {role}'
    return lol[role_column].value_counts().head(5).index

roles = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
top_5_picks = pd.DataFrame()
for role in roles:
    top_5_picks[f'Blue {role}'] = get_top_picks(lol, role, 'Blue')
    top_5_picks[f'Red {role}'] = get_top_picks(lol, role, 'Red')
top_5_picks.index = [f'Top {i}' for i in range(1, 6)]

fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('tight')
ax.axis('off')
table_data = top_5_picks.reset_index().values.tolist()
column_labels = ['Rank'] + list(top_5_picks.columns)
table = ax.table(cellText=table_data, colLabels=column_labels, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

# Save the table as an image
plt.savefig('top_5_picks.png', bbox_inches='tight', pad_inches=0.05)
plt.show()

# Calculating CS differentials for the Top, Mid, and Bot roles
lol['Top CS Differential'] = lol['Blue Top CS'] - lol['Red Top CS']
lol['Mid CS Differential'] = lol['Blue Mid CS'] - lol['Red Mid CS']
lol['Bot CS Differential'] = lol['Blue Bot CS'] - lol['Red Bot CS']

# Melting the DataFrame to have role CS differentials in one column for seaborn
cs_differentials = lol[['Top CS Differential', 'Mid CS Differential', 'Bot CS Differential']].melt(
    var_name='Role',
    value_name='CS Differential'
)

# Updating the 'Role' column to only contain the role names (Top, Mid, Bot)
cs_differentials['Role'] = cs_differentials['Role'].str.replace(' CS Differential', '')
plt.figure(figsize=(10, 6))
sns.boxplot(x='Role', y='CS Differential', data=cs_differentials)
plt.title('CS Differential by Role')
plt.xlabel('Role')
plt.ylabel('CS Differential (Blue - Red)')

# Function to extract kills from a KDA formatted string
def extract_kills(kda):
    if kda and '/' in kda:
        return int(kda.split('/')[0])
    return 0

# Extracting kills for each role for the Blue team
lol['Blue Top Kills'] = lol['Blue Top KDA'].apply(extract_kills)
lol['Blue Mid Kills'] = lol['Blue Mid KDA'].apply(extract_kills)
lol['Blue Bot Kills'] = lol['Blue Bot KDA'].apply(extract_kills)

# Extracting kills for each role for the Red team
lol['Red Top Kills'] = lol['Red Top KDA'].apply(extract_kills)
lol['Red Mid Kills'] = lol['Red Mid KDA'].apply(extract_kills)
lol['Red Bot Kills'] = lol['Red Bot KDA'].apply(extract_kills)

# Calculating the average kills per game for each role and team
average_kills_data = pd.DataFrame({
    'Role': ['Top', 'Mid', 'Bot'] * 2,
    'Team': ['Blue'] * 3 + ['Red'] * 3,
    'Average Kills': [
        lol['Blue Top Kills'].mean(),
        lol['Blue Mid Kills'].mean(),
        lol['Blue Bot Kills'].mean(),
        lol['Red Top Kills'].mean(),
        lol['Red Mid Kills'].mean(),
        lol['Red Bot Kills'].mean()
    ]
})

palette_colors = {"Blue": "darkslateblue", "Red": "firebrick"}
sns.barplot(x='Role', y='Average Kills', hue='Team', data=average_kills_data, palette=palette_colors)
plt.title('Kills by Role for Blue and Red Teams')
plt.xlabel('Role')
plt.ylabel('Average Kills per Game')
plt.show()

average_stats = pd.DataFrame({
    'Stat': ['Dragons', 'Barons', 'Turrets'] * 2,
    'Team': ['Blue', 'Blue', 'Blue', 'Red', 'Red', 'Red'],
    'Average': [
        lol['Blue Dragons'].mean(), lol['Blue Barons'].mean(), lol['Blue Turrets'].mean(),
        lol['Red Dragons'].mean(), lol['Red Barons'].mean(), lol['Red Turrets'].mean()
    ]
})

palette_colors = {"Blue": "darkslateblue", "Red": "firebrick"}
plt.figure(figsize=(10, 6))
sns.barplot(x='Stat', y='Average', hue='Team', data=average_stats, palette=palette_colors)
plt.title('Objectives for Blue and Red Teams')
plt.xlabel('Objective')
plt.ylabel('Average per Game')
plt.show()

# Preparing the data for the scatterplot
scatter_data_blue = lol[['Blue Dragons', 'Blue Turrets']].rename(columns={'Blue Dragons': 'Dragons', 'Blue Turrets': 'Turrets'})
scatter_data_red = lol[['Red Dragons', 'Red Turrets']].rename(columns={'Red Dragons': 'Dragons', 'Red Turrets': 'Turrets'})

# Hexbin plot for Blue side
blue_plot = sns.jointplot(x='Dragons', y='Turrets', data=scatter_data_blue, kind="hex", color="darkslateblue")
blue_plot.fig.suptitle('Hexbin Plot of Number of Turrets vs. Number of Dragons for Blue Side')
blue_plot.fig.subplots_adjust(top=0.95)

# Hexbin plot for Red side
red_plot = sns.jointplot(x='Dragons', y='Turrets', data=scatter_data_red, kind="hex", color="firebrick")
red_plot.fig.suptitle('Hexbin Plot of Number of Turrets vs. Number of Dragons for Red Side')
red_plot.fig.subplots_adjust(top=0.95)
red_plot.ax_joint.set_xlim(scatter_data_blue['Dragons'].min(), scatter_data_blue['Dragons'].max())

plt.show()

# Filtering the data based on the combinations
blue_dragon_blue_herald_count = len(lol[(lol['First Dragon Team'] == 'Blue') & (lol['First Rift Herald Team'] == 'Blue')])
blue_dragon_red_herald_count = len(lol[(lol['First Dragon Team'] == 'Blue') & (lol['First Rift Herald Team'] == 'Red')])
red_dragon_blue_herald_count = len(lol[(lol['First Dragon Team'] == 'Red') & (lol['First Rift Herald Team'] == 'Blue')])
red_dragon_red_herald_count = len(lol[(lol['First Dragon Team'] == 'Red') & (lol['First Rift Herald Team'] == 'Red')])
total_games = len(lol)

# Calculating the proportions
proportions_data = pd.DataFrame({
    'Combination': ['Blue Dragon & Blue Herald', 'Blue Dragon & Red Herald',
                    'Red Dragon & Blue Herald', 'Red Dragon & Red Herald'],
    'Proportion': [
        blue_dragon_blue_herald_count / total_games,
        blue_dragon_red_herald_count / total_games,
        red_dragon_blue_herald_count / total_games,
        red_dragon_red_herald_count / total_games
    ]
})

color_scheme = ['blue', 'orange', 'purple', 'red']
combination_order = ['Blue Dragon & Blue Herald', 'Blue Dragon & Red Herald', 'Red Dragon & Blue Herald', 'Red Dragon & Red Herald']

# Create bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Combination', y='Proportion', data=proportions_data, palette=color_scheme, order=combination_order)
plt.title('Proportion of Games for Each Dragon-Herald Combination')
plt.xlabel('First Dragon & Rift Herald Combination')
plt.ylabel('Proportion of Games')
plt.xticks(rotation=45)

# Filtering data for scatter plots
blue_dragon_blue_herald = lol[(lol['First Dragon Team'] == 'Blue') & (lol['First Rift Herald Team'] == 'Blue')]
blue_dragon_red_herald = lol[(lol['First Dragon Team'] == 'Blue') & (lol['First Rift Herald Team'] == 'Red')]
red_dragon_blue_herald = lol[(lol['First Dragon Team'] == 'Red') & (lol['First Rift Herald Team'] == 'Blue')]
red_dragon_red_herald = lol[(lol['First Dragon Team'] == 'Red') & (lol['First Rift Herald Team'] == 'Red')]

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
scatter_datasets = [blue_dragon_blue_herald, blue_dragon_red_herald, red_dragon_blue_herald, red_dragon_red_herald]
colors = ['blue', 'orange', 'purple', 'red']
titles = ['Blue Dragon & Blue Herald', 'Blue Dragon & Red Herald', 'Red Dragon & Blue Herald', 'Red Dragon & Red Herald']

for ax, dataset, color, title in zip(axes.flatten(), scatter_datasets, colors, titles):
    sns.scatterplot(ax=ax, x='First Dragon Time', y='First Rift Herald Time', data=dataset, color=color)
    ax.set_title(title)
    ax.set_xlabel('Time of First Dragon (Minutes)')
    ax.set_ylabel('Time of First Rift Herald (Minutes)')
    ax.set_xlim(5, 17)
    y_max = 8 + (x_max - x_min)
    ax.set_ylim(8, 15)

plt.tight_layout()
plt.show()

# Preparing the data for Blue and Red side scatterplots
blue_side_data = lol[['Red Wards Placed', 'Blue Wards Destroyed']]
red_side_data = lol[['Blue Wards Placed', 'Red Wards Destroyed']]

# Function to calculate and annotate slope
def annotate_slope(ax, x, y, color):
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    slope_annotation = f'Slope: {slope:.2f}'
    ax.text(0.05, 0.95, slope_annotation, transform=ax.transAxes, color=color)

plt.figure(figsize=(12, 6))

# Scatterplot for Blue side
ax1 = plt.subplot(1, 2, 1)
sns.scatterplot(x='Red Wards Placed', y='Blue Wards Destroyed', data=blue_side_data, color='darkslateblue')
sns.regplot(x='Red Wards Placed', y='Blue Wards Destroyed', data=blue_side_data, scatter=False, color='darkslateblue')
annotate_slope(ax1, blue_side_data['Red Wards Placed'], blue_side_data['Blue Wards Destroyed'], 'darkslateblue')
plt.title('Blue Side: Opponent Wards Placed vs Team Wards Destroyed')
plt.xlabel('Number of Wards Opponent Placed')
plt.ylabel('Number of Wards Team Destroyed')

# Scatterplot for Red side
ax2 = plt.subplot(1, 2, 2)
sns.scatterplot(x='Blue Wards Placed', y='Red Wards Destroyed', data=red_side_data, color='firebrick')
sns.regplot(x='Blue Wards Placed', y='Red Wards Destroyed', data=red_side_data, scatter=False, color='firebrick')
annotate_slope(ax2, red_side_data['Blue Wards Placed'], red_side_data['Red Wards Destroyed'], 'firebrick')
plt.title('Red Side: Opponent Wards Placed vs Team Wards Destroyed')
plt.xlabel('Number of Wards Opponent Placed')
plt.ylabel('Number of Wards Team Destroyed')

# Adjusting y-axes to match each other
max_y_value = max(blue_side_data['Blue Wards Destroyed'].max(), red_side_data['Red Wards Destroyed'].max())
ax1.set_ylim(0, max_y_value)
ax2.set_ylim(0, max_y_value)

plt.tight_layout()
plt.show()