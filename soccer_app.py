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


# tweak the data
# remove dup row and drop unwanted multi-level cols 
goalkeeper_stats=(df
.drop(25, inplace=True) 
.drop(columns=[('Unnamed: 0_level_0','Rk'), ('Unnamed: 2_level_0','Nation'), ('Unnamed: 3_level_0','Pos'),
                 ('Unnamed: 5_level_0','Age'), ('Unnamed: 6_level_0','Born'), ('Unnamed: 33_level_0',  'Matches')],
                 inplace=True)
)


# flatten the cols with mulitilevel index
# rename the first 3 cols
# convert the undesired dtype
def flatten_cols(df_):
    cols = ['_'.join(cs) for cs in df_.columns.to_flat_index()]
    df_.columns = cols 
    return df_

def convert_col_type(df_):    
    for col in df_.columns:
        df_[col] = pd.to_numeric(df_[col], errors = 'coerce')
    return df_


goalkeeper_stats_p1= (goalkeeper_stats
.pipe(flatten_cols)
.rename(columns={'Unnamed: 1_level_0_Player': 'Player', \
                 'Unnamed: 4_level_0_Squad': 'Squad', \
                 'Unnamed: 7_level_0_90s': '90s'})
)

goalkeeper_stats_p2= (goalkeeper_stats
.iloc[:, 2:]
.pipe(convert_col_type)
)

goalkeeper_stats =goalkeeper_stats_p1.assign(**goalkeeper_stats_p2)