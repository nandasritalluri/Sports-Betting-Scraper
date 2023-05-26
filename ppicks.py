from selenium import webdriver
from selenium.webdriver.common.by import By

# Get the player name from the user
player_name = input("Enter player name: ")

# Get the desired stat from the user
stat = input("Enter desired stat (e.g. FG, 3P, FT): ")

# Get the desired line from the user
line = input("Enter desired line (e.g. 10, 20, 30): ")
line = float(line)

# Construct the last name and first two letters of the first name
parts = player_name.lower().split()
last_name = parts[-1]
first_name = parts[0]
first_two_letters = first_name[:2]

# Construct the URL for the player's playoff stats for the current year
year = 2023
url = f"https://www.basketball-reference.com/players/{last_name[0]}/{last_name[:5]}{first_two_letters}01/gamelog/{year}/"

# Create a Firefox web driver
driver = webdriver.Firefox()

# Navigate to the player's playoff stats page
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Find the table that contains the player's playoff stats
stats_table = driver.find_element(By.ID, "div_pgl_basic_playoffs")

# Extract the rows of the table
rows = stats_table.find_elements(By.TAG_NAME, "tr")

# Find the index of the desired stat column
header_row = rows[0]
headers = header_row.find_elements(By.TAG_NAME, "th")
stat_index = None
for i in range(len(headers)):
    if headers[i].text == stat:
        stat_index = i-1
        #print(stat_index)
        break

# Check if the desired stat was found
if stat_index is None:
    print(f"No {stat} column found for this player.")
else:
    # Count the number of entries in the desired stat column that are greater than the line
    num_greater = 0
    for i in range(1, len(rows)):
        row = rows[i]
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > stat_index:
            value = float(cells[stat_index].text)
            if value > line:
                num_greater += 1
    
    # Calculate and print the percentage of entries in the desired stat column that are greater than the line
    total_entries = len(rows) - 1
    percentage_greater = num_greater / total_entries * 100
    print(f"The percentage of {stat} entries that are greater than {line} is: {percentage_greater:.2f}%")

# Close the web driver
driver.quit()
