import streamlit as st
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import requests
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO





st.title('Premier League Player Advanced Goalkeeping 2023-2024')


st.markdown(
"""
This app performs simple webscraping of Premier League Player Advanced Goalkeeping stats data!
* **Python libraries:** selenium, BeautifulSoup, pandas, streamlit
* **Data source:** [fbref.com](https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats)

"""
)

# design sidebar input
st.sidebar.header('User Input Features')
url= 'https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats'

website = st.text_input("URL", url)


# web scraping of PL GK stats
@st.cache_data

def load_web_data(link):
    # Use raw string for Windows paths      
    # chromedriver_path = r"C:\Windows\System32\chromedriver.exe"

    # Setup Chrome options
    chrome_options = Options()
    # chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless') # Run Chrome in headless mode
    chrome_options.add_argument('--disable-dev-shm-usage')


    # Install ChromeDriver and set path
    chrome_driver_path = ChromeDriverManager().install()
    service = Service(chrome_driver_path)

    
    # Create a new Chrome webdriver with the specified options using the explicitly set path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(link)


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
    else:
        print("Warning: Table not found!")

    # To address the FutureWarning about passing literal HTML to read_html, 
    # Convert the table HTML to a string
    # wrap the HTML content in a StringIO object before passing it to read_html
    table_html_str = str(table_html)
    html_io = StringIO(table_html_str)
    dfs = pd.read_html(html_io)

    if dfs:
        df = dfs[0]

    else:
        print("Warning: No DataFrames found!")
        return None
    
    # tweak the data
    # remove dup row and drop unwanted multi-level cols 
    raw=(df
         .drop(25, inplace=False) 
         .drop(columns=[('Unnamed: 0_level_0','Rk'), ('Unnamed: 2_level_0','Nation'), ('Unnamed: 3_level_0','Pos'),
                    ('Unnamed: 5_level_0','Age'), ('Unnamed: 6_level_0','Born'), ('Unnamed: 33_level_0',  'Matches')],
                inplace=False)
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


    raw1= (raw
           .pipe(flatten_cols)
           .rename(columns={'Unnamed: 1_level_0_Player': 'Player', 
                            'Unnamed: 4_level_0_Squad': 'Squad', 
                            'Unnamed: 7_level_0_90s': '90s'})
          )

    raw2= (raw1
           .iloc[:, 2:]
          .pipe(convert_col_type)
          )

    goalkeeper_stats = raw1.assign(**raw2)
    return goalkeeper_stats


goalkeeper_stats = load_web_data(url)


if goalkeeper_stats is not None:
    # Sidebar - Squad selection
    sorted_unique_squad = sorted(goalkeeper_stats.Squad.unique())
    selected_squad = st.sidebar.multiselect('Squad', sorted_unique_squad, sorted_unique_squad)

    # Filtering data
    df_selected_squad = goalkeeper_stats[goalkeeper_stats.Squad.isin(selected_squad)]
    

    st.header('Display Goalkeeper Stats of Selected Squad(s)')
    st.write('Data Dimension: ' + str(df_selected_squad.shape[0]) + ' rows and ' + str(df_selected_squad.shape[1]) + ' columns.')
    st.dataframe(df_selected_squad)


    def filedownload(df):
        csv = df.to_csv(index=False)
        # Ensure proper encoding
        # strings <-> bytes conversions
        b64 = base64.b64encode(csv.encode('utf-8')).decode()  
        href = f'<a href="data:file/csv;base64,{b64}" download="goalkeeper_stats.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(df_selected_squad), unsafe_allow_html=True)

else:
    st.error("Failed to load data from the provided URL.")



