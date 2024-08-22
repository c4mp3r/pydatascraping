import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_tables_from_wikipedia(url):
    # Fetch the content from the Wikipedia page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables in the page
    tables = soup.find_all('table', {'class': 'wikitable'})

    return tables

def calculate_levels(table):
    # Convert the table to a DataFrame
    df = pd.read_html(str(table))[0]

    low_levels = []
    high_levels = []

    for level_range in df['Levels']:
        try:
            # Split the level range, e.g., "5-10" -> [5, 10]
            lower, upper = map(int, level_range.split('-'))
            low_levels.append(lower)
            high_levels.append(upper)
        except ValueError:
            # If the level range is a single number, just treat it as both lower and upper
            level = int(level_range)
            low_levels.append(level)
            high_levels.append(level)

    # Calculate the average low and high levels
    avg_low_level = sum(low_levels) / len(low_levels) if low_levels else None
    avg_high_level = sum(high_levels) / len(high_levels) if high_levels else None

    return avg_low_level, avg_high_level

# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_Dungeons_%26_Dragons_modules'

# Fetch the tables from Wikipedia
tables = fetch_tables_from_wikipedia(url)

# Lists to store average low and high levels
all_avg_low_levels = []
all_avg_high_levels = []

for table in tables:
    try:
        avg_low, avg_high = calculate_levels(table)
        if avg_low is not None and avg_high is not None:
            all_avg_low_levels.append(avg_low)
            all_avg_high_levels.append(avg_high)
    except Exception as e:
        continue

# Calculate the overall average low and high level
overall_avg_low_level = sum(all_avg_low_levels) / len(all_avg_low_levels) if all_avg_low_levels else None
overall_avg_high_level = sum(all_avg_high_levels) / len(all_avg_high_levels) if all_avg_high_levels else None

print(f"Overall Average Low Level: {overall_avg_low_level:.2f}")
print(f"Overall Average High Level: {overall_avg_high_level:.2f}")
average = ((overall_avg_low_level+overall_avg_high_level)/2)
print(f"Average Level: {average:.2f}")
