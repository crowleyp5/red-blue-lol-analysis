import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

url = 'https://gol.gg/esports/home/'

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)

# These are the columns of data we hope to scrape
columns = ['Tournament', 'Date', 'Game Time', 'Blue Team', 'Red Team', 
           'Blue Kills', 'Blue Turrets', 'Blue Dragons', 'Blue Barons', 
           'Red Kills', 'Red Turrets', 'Red Dragons', 'Red Barons',
           'Blue Bans', 'Red Bans', 'Blue Picks', 'Red Picks',
           'Blue KDA', 'Blue CS', 'Red KDA', 'Red CS', 
           'Blue Wards Placed', 'Blue Wards Destroyed', 
           'Red Wards Placed', 'Red Wards Destroyed',
           'First Dragon Team', 'First Dragon Time', 
           'First Rift Herald Team', 'First Rift Herald Time']
df = pd.DataFrame(columns=columns)

''' 
The format of this site is a table with 10 of the most recent professional sets of League of Legends.
There is a back button to show the previous 10 sets. This does not redirect to a new page.
In the row corresponding to each set, there is a link that redirects us to a stats page where we scrape most of the info.
Since this redirects us to a new page with the game stats, whenever we navigate back, we will have to push the previous 10 
button again to get back to the set we were analyzing, so we will keep track of the back count. 
Each set could have anywhere from 1 to 5 games.
It is important to note that some games did not have the required stats, so the program throws errors. At first, I 
tried to filter the offending tournaments out, but this is not feasible.
If the program throws errors, I simply adjust the backcount loop and start again.
'''
back_count = 40
for i in range(back_count):

    # Print iteration number in case need of restart
    print(i)

    # Find the sets on the main page
    games_container = driver.find_element(By.ID, 'lastgames_tab')
    recent_games = games_container.find_elements(By.XPATH, './/tbody/tr')
    for i, game in enumerate(recent_games):
        games_container = driver.find_element(By.ID, 'lastgames_tab')
        recent_games = games_container.find_elements(By.XPATH, './/tbody/tr')
        game = recent_games[i]

        recent_game_rows = game.find_elements(By.XPATH, './td')
        # Get tournament name and date
        if len(recent_game_rows) >= 3:
            tournament = recent_game_rows[0].text
            # Attempt to filter out tournaments lacking desired data
            if 'EMEA' in tournament:
                continue
            if tournament == 'CBLOL Academy Split 2 2023':
                continue
            date = recent_game_rows[1].text
            print(f"Tournament: {tournament}, Date: {date}")

            # Redirect to link with game stats
            game_link = recent_game_rows[2].find_element(By.TAG_NAME, 'a')
            game_link.click()
            time.sleep(1)

            # Get url of all games in set
            game_navbar = driver.find_element(By.CLASS_NAME, 'gamemenu')
            game_links = game_navbar.find_elements(By.TAG_NAME, 'a')
            game_urls = [link.get_attribute('href') for link in game_links if 'page-game' in link.get_attribute('href')]

            for game_url in game_urls:
                driver.get(game_url)
                time.sleep(1)

                # Get game time
                game_time = driver.find_element(By.CSS_SELECTOR, 'div.col-6.text-center h1').text
                print(f"Game Time: {game_time}")
                
                # Get team names
                blue_team_name = driver.find_element(By.CSS_SELECTOR, 'div.blue-line-header a').text
                red_team_name = driver.find_element(By.CSS_SELECTOR, 'div.red-line-header a').text
                print(f"Blue Side Team: {blue_team_name}, Red Side Team: {red_team_name}")

                # Get kills, turrets, dragons, and barons from both sides
                blue_kills = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box blue_line"])[1]').text
                blue_turrets = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box blue_line"])[2]').text
                blue_dragons = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box blue_line"])[3]').text
                blue_barons = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box blue_line"])[4]').text
                print(f"Blue Side - Kills: {blue_kills}, Turrets: {blue_turrets}, Dragons: {blue_dragons}, Barons: {blue_barons}")

                red_kills = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box red_line"])[1]').text
                red_turrets = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box red_line"])[2]').text
                red_dragons = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box red_line"])[3]').text
                red_barons = driver.find_element(By.XPATH, '(//div[@class="col-2"]/span[@class="score-box red_line"])[4]').text
                print(f"Blue Side - Kills: {blue_kills}, Turrets: {blue_turrets}, Dragons: {blue_dragons}, Barons: {blue_barons}")

                # Get picks and bans from both sides
                blue_bans = driver.find_elements(By.XPATH, '(//div[contains(text(), "Bans")])[1]/following-sibling::div//img[@class="champion_icon_medium rounded-circle"]')
                print("Blue Side Bans:")
                for ban in blue_bans:
                    print(ban.get_attribute('alt'))

                red_bans = driver.find_elements(By.XPATH, '(//div[contains(text(), "Bans")])[2]/following-sibling::div//img[@class="champion_icon_medium rounded-circle"]')
                print("Red Side Bans:")
                for ban in red_bans:
                    print(ban.get_attribute('alt'))

                blue_picks = driver.find_elements(By.XPATH, '(//div[contains(text(), "Picks")])[1]/following-sibling::div//img[@class="champion_icon_medium rounded-circle"]')
                print("Blue Side Picks:")
                for pick in blue_picks:
                    print(pick.get_attribute('alt'))

                red_picks = driver.find_elements(By.XPATH, '(//div[contains(text(), "Picks")])[2]/following-sibling::div//img[@class="champion_icon_medium rounded-circle"]')
                print("Red Side Picks:")
                for pick in red_picks:
                    print(pick.get_attribute('alt'))
                
                # Get KDA and CS for both sides in separate table
                blue_team_div = driver.find_element(By.CSS_SELECTOR, "div.col-cadre div.row div.col-12.col-md-6:nth-of-type(1)")
                red_team_div = driver.find_element(By.CSS_SELECTOR, "div.col-cadre div.row div.col-12.col-md-6:nth-of-type(2)")

                blue_team_table = blue_team_div.find_element(By.TAG_NAME, "table")
                red_team_table = red_team_div.find_element(By.TAG_NAME, "table")

                rows = blue_team_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    if len(columns) >= 5:  # Ensure there are enough columns
                        kda = columns[-2].text.strip()
                        cs = columns[-1].text.strip()
                        print("Blue Team - KDA:", kda, "CS:", cs)

                rows = red_team_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    if len(columns) >= 5:  # Ensure there are enough columns
                        kda = columns[-2].text.strip()
                        cs = columns[-1].text.strip()
                        print("Red Team - KDA:", kda, "CS:", cs)
                
                # Get wards data from javascript graph object
                blue_team_wards_destroyed = driver.execute_script("return visionData.datasets[0].data[0];")
                blue_team_wards_placed = driver.execute_script("return visionData.datasets[0].data[1];")

                red_team_wards_destroyed = driver.execute_script("return visionData.datasets[1].data[0];")
                red_team_wards_placed = driver.execute_script("return visionData.datasets[1].data[1];")

                # Print the extracted information
                print("Blue Team - Wards Placed:", blue_team_wards_placed, "Wards Destroyed:", blue_team_wards_destroyed)
                print("Red Team - Wards Placed:", red_team_wards_placed, "Wards Destroyed:", red_team_wards_destroyed)

                # Get dragon and rift herald stats from another table
                first_dragon_time = None
                first_dragon_team = None
                first_rift_herald_time = None
                first_rift_herald_team = None

                events = driver.find_elements(By.CSS_SELECTOR, "span[style='display:inline-block']")

                for event in events:
                    html_content = event.get_attribute('innerHTML')
                    # Check for first dragon
                    if "Drake" in html_content and first_dragon_time is None:
                        first_dragon_time = event.text.strip().split('\n')[-1]
                        if 'blue_action' in html_content:
                            first_dragon_team = 'Blue'
                        elif 'red_action' in html_content:
                            first_dragon_team = 'Red'
                        else:
                            first_dragon_team = None
                    # Check for first rift herald
                    elif "herald-icon.png" in html_content and first_rift_herald_time is None:
                        first_rift_herald_time = event.text.strip().split('\n')[-1]
                        if 'blue_action' in html_content:
                            first_rift_herald_team = 'Blue' 
                        elif 'red_action' in html_content:
                            first_rift_herald_team = 'Red'
                        else:
                            first_rift_herald_team = None
                
                # Compile data
                game_data = {
                    'Tournament': tournament,
                    'Date': date,
                    'Game Time': game_time,
                    'Blue Team': blue_team_name,
                    'Red Team': red_team_name,
                    'Blue Kills': blue_kills,
                    'Blue Turrets': blue_turrets,
                    'Blue Dragons': blue_dragons,
                    'Blue Barons': blue_barons,
                    'Red Kills': red_kills,
                    'Red Turrets': red_turrets,
                    'Red Dragons': red_dragons,
                    'Red Barons': red_barons,
                    'Blue Bans': ', '.join([ban.get_attribute('alt') for ban in blue_bans]),
                    'Red Bans': ', '.join([ban.get_attribute('alt') for ban in red_bans]),
                    'Blue Picks': ', '.join([pick.get_attribute('alt') for pick in blue_picks]),
                    'Red Picks': ', '.join([pick.get_attribute('alt') for pick in red_picks]),
                    'Blue KDA': ', '.join([column.text.strip() for row in blue_team_table.find_elements(By.TAG_NAME, "tr")[1:] for column in row.find_elements(By.TAG_NAME, "td") if len(row.find_elements(By.TAG_NAME, "td")) >= 5]),
                    'Blue CS': ', '.join([column.text.strip() for row in blue_team_table.find_elements(By.TAG_NAME, "tr")[1:] for column in row.find_elements(By.TAG_NAME, "td") if len(row.find_elements(By.TAG_NAME, "td")) >= 5]),
                    'Red KDA': ', '.join([column.text.strip() for row in red_team_table.find_elements(By.TAG_NAME, "tr")[1:] for column in row.find_elements(By.TAG_NAME, "td") if len(row.find_elements(By.TAG_NAME, "td")) >= 5]),
                    'Red CS': ', '.join([column.text.strip() for row in red_team_table.find_elements(By.TAG_NAME, "tr")[1:] for column in row.find_elements(By.TAG_NAME, "td") if len(row.find_elements(By.TAG_NAME, "td")) >= 5]),
                    'Blue Wards Placed': blue_team_wards_placed,
                    'Blue Wards Destroyed': blue_team_wards_destroyed,
                    'Red Wards Placed': red_team_wards_placed,
                    'Red Wards Destroyed': red_team_wards_destroyed,
                    'First Dragon Team': first_dragon_team,
                    'First Dragon Time': first_dragon_time,
                    'First Rift Herald Team': first_rift_herald_team,
                    'First Rift Herald Time': first_rift_herald_time
                }

                # Append to dataset periodically in case of errors
                df = pd.DataFrame([game_data])
                df.to_csv('loldata.csv', mode='a', header=False, index=False)

                print(f"First Dragon Taken By: {first_dragon_team} at {first_dragon_time}")
                print(f"First Rift Herald Taken By: {first_rift_herald_team} at {first_rift_herald_time}")

                # Back to main page
                driver.back()
                time.sleep(1)

                # Push button to get back to the right list of sets
                for i in range(back_count):
                    previous_button = driver.find_element(By.ID, 'previous10')
                    previous_button.click()
            
                time.sleep(7)

driver.quit() 