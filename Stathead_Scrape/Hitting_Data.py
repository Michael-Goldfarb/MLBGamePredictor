import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# ignore warnings
pd.options.mode.chained_assignment = None

# start webdriver
driver = webdriver.Chrome(executable_path="C:\chromedriver.exe")

# automate login
driver.get('https://stathead.com/users/login.cgi')
username = None
password = None
driver.find_element(By.ID, 'username').send_keys(username)
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="sh-login-button"]').click()

# GET DATA
frames = []
df_number = 0
for offset in range(0, 732400, 200):
    df_number += 1
    print('getting dataframe', str(df_number), 'of', str(732400/200), '(offset =', str(offset) + ')')
    
    # use batter game stat finder url to get data
    request_url = 'https://stathead.com/baseball/player-batting-game-finder.cgi?request=1&team_game_min=1&comp_type=reg&order_by=date&player_game_max=9999&team_game_max=165&order_by_asc=0&locationMatch=is&year_min=2012&player_game_min=1&GF=anyGF&max_wind_speed=90&location=pob&max_temperature=120&match=player_game&year_max=2022&min_temperature=0&exactness=anymarked&min_wind_speed=0&offset=' + str(offset)
    wait = WebDriverWait(driver, 100)
    driver.get(request_url)
    get_url = driver.current_url
    wait.until(EC.url_to_be(request_url))
    
    # create ActionChains object
    a = ActionChains(driver)
    
    # find export button
    m = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="stats_sh"]/div/ul/li[1]/span')))
    
    # click export data button
    a.move_to_element(m).perform()
    
    # click export to CSV button
    n = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Get table as CSV (for Excel)"]')))
    n.click()
    
    # get page source for BS4 to parse
    if get_url == request_url:
        page_source = driver.page_source
    
    # get soup
    soup = BeautifulSoup(page_source,features='html.parser')
    
    # get csv formatted table from page
    t_text = soup.find('pre', {"id": "csv_stats"}).getText()[80:]
    
    # create dataframe with table
    csv_df = pd.read_csv(StringIO(t_text), sep=",")

    # append csv_df to frames
    frames.append(csv_df)

    batter_df_all = pd.concat(frames)

    batter_df_all.tail()

    batter_df_all = batter_df_all.reset_index(drop = True)

    batter_df_all.to_csv('batter_stats.csv')