import pandas as pd
import numpy as np

df = pd.read_csv("loldata.csv")

df = df.drop_duplicates()

# Splitting the 'Blue Bans' and 'Red Bans' columns into separate columns
blue_bans_cols = df['Blue Bans'].str.split(',', expand=True)
red_bans_cols = df['Red Bans'].str.split(',', expand=True)
blue_bans_cols.columns = [f'Blue Bans {i+1}' for i in range(blue_bans_cols.shape[1])]
red_bans_cols.columns = [f'Red Bans {i+1}' for i in range(red_bans_cols.shape[1])]
df = pd.concat([df, blue_bans_cols, red_bans_cols], axis=1)

# Splitting the 'Blue Picks' and 'Red Picks' columns into separate columns
blue_picks_cols = df['Blue Picks'].str.split(',', expand=True)
red_picks_cols = df['Red Picks'].str.split(',', expand=True)
blue_picks_cols.columns = ['Blue Top', 'Blue Jungle', 'Blue Mid', 'Blue Bot', 'Blue Support']
red_picks_cols.columns = ['Red Top', 'Red Jungle', 'Red Mid', 'Red Bot', 'Red Support']

# Merging the new columns back into the original DataFrame
df = pd.concat([df, blue_picks_cols, red_picks_cols], axis=1)

roles = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']

# Initializing empty dataframes to store the extracted data
blue_kda_columns = pd.DataFrame()
red_kda_columns = pd.DataFrame()

# Extracting KDA and CS data for Blue team
for role in roles:
    blue_kda_columns[f'Blue {role} KDA'] = df['Blue KDA'].str.split(',', expand=True)[11]
    blue_kda_columns[f'Blue {role} CS'] = df['Blue KDA'].str.split(',', expand=True)[12]
    df['Blue KDA'] = df['Blue KDA'].apply(lambda x: ','.join(x.split(',')[13:]))

# Extracting KDA and CS data for Red team
for role in roles:
    red_kda_columns[f'Red {role} KDA'] = df['Red KDA'].str.split(',', expand=True)[11]
    red_kda_columns[f'Red {role} CS'] = df['Red KDA'].str.split(',', expand=True)[12]
    df['Red KDA'] = df['Red KDA'].apply(lambda x: ','.join(x.split(',')[13:]))

# Merging the extracted data back into the original DataFrame
df = pd.concat([df, blue_kda_columns, red_kda_columns], axis=1)

# Converting 'Game Time', 'First Dragon Time', and 'First Rift Herald Time' to minute decimals
df['Game Time'] = df['Game Time'].apply(
    lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60 if isinstance(x, str) else x
)
df['First Dragon Time'] = df['First Dragon Time'].apply(
    lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60 if isinstance(x, str) else x
)
df['First Rift Herald Time'] = df['First Rift Herald Time'].apply(
    lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60 if isinstance(x, str) else x
)

# Converting 'Date' column to date format
df['Date'] = pd.to_datetime(df['Date'])

df = df.drop(columns = ['Blue Bans', 'Red Bans', 'Blue Picks', 'Red Picks', 'Blue KDA', 'Blue CS', 'Red KDA', 'Red CS'])

df.to_csv('loldata_cleaned.csv', index=False)