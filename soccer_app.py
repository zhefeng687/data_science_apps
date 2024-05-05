"""
Selenium excels in situations where the task involves interacting with 
a web page before the actual scraping—like logging into a website, 
navigating through a series of web pages, 
or dealing with JavaScript-rendered content dynamically loaded onto the page.

"""


import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as pt
import seaborn as sns 
import requests
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from io import StringIO


# st.title('Premier League Player Advanced Goalkeeping 2023-2024')


# st.markdown(
"""
This app performs simple webscraping of Premier League Player Advanced Goalkeeping stats data!
* **Python libraries:** selenium, BeautifulSoup, pandas, streamlit
* **Data source:** [fbref.com](https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats)

"""


# design sidebar feature: Squad, Player
#st.sidebar.header('User Input Features')

# web scraping of PL GK stats
#@st.cache_data


# download the appropriate WebDriver for your browser and ensure it’s accessible from your system’s PATH. For example, to use ChromeDriver, download it from the ChromeDriver downloads page and
# update your system and user's PATH variable 
# to include the path to the downloaded executable.
url = "https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats"
chromedriver_path = "C:\Windows\System32\chromedriver.exe"
driver = webdriver.Chrome(chromedriver_path)
driver.get(url)


# Get the page source after JavaScript execution
html_content = driver.page_source


# Close the driver
driver.quit()


# Parse the HTML content
soup = bs4(html_content, 'html.parser')

# Find the table within the HTML content using id
table_html = soup.find('table', id='stats_keeper_adv')

# Check if the table is found
if table_html:
    print("Table found!")
    # Print the table HTML (for demonstration)
    print(table_html)
else:
    print("Table not found.")


# To address the FutureWarning about passing literal HTML to read_html, 
# Convert the table HTML to a string
# wrap the HTML content in a StringIO object before passing it to read_html
table_html_str = str(table_html)
html_io = StringIO(table_html_str)
dfs = pd.read_html(html_io)


# inspect the list of DataFrames
for i, df in enumerate(dfs):
    print(f"DataFrame {i}:\n{df}")


df.info()