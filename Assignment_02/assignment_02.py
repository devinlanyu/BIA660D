# coding: utf-8

# ## BIA660D_Assignment 2.1 ##

# In[221]:

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
import bs4
import numpy as np

# In[222]:

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# In[223]:

import random
import time

# ### Question 1 ###

# In[224]:

driver = webdriver.Firefox(executable_path=r'/Users/yulanyu/Downloads/geckodriver')
driver.get('http://www.mlb.com')
# driver.close()
wait = WebDriverWait(driver, 10)
stats_header_bar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item--stats')))
stats_header_bar.click()

# In[225]:

stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
stats_line_items[0].click()

# In[226]:

hitting_season_element = wait.until(EC.element_to_be_clickable((By.ID, 'sp_hitting_season')))
hitting_season_element.click()
year2015 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sp_hitting_season > option:nth-child(4)')))
year2015.click()

# In[227]:

team_selection = driver.find_element_by_id('st_parent')
team_selection.click()

# In[230]:

regular_season_element = wait.until(EC.element_to_be_clickable((By.ID, 'st_hitting_game_type')))
regular_season_element.click()
regular_season_selection = driver.find_element_by_css_selector('#st_hitting_game_type > option:nth-child(1)')
regular_season_selection.click()

# In[231]:

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")

# In[232]:

data_head = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df = pd.DataFrame(columns=data_head)

# In[233]:

data_context = []
for a in soup.tbody.find_all('tr'):
    for b in a.find_all('td'):
        data_context.append(b.text)
clean_data_context = []
for c in range(int(len(data_context) / len(data_head))):
    d = data_context[c * len(data_head):(c + 1) * len(data_head)]
    clean_data_context.append(d)

# In[234]:

for i in range(30):
    df.loc[i] = clean_data_context[i]

# In[236]:

# df


# In[237]:

print ('The team had the most homeruns in the regular season of 2015 is', df.iloc[df['HR'].idxmax(), 1])

# In[238]:

# Export to csv file
df.to_csv('Question 1 and 2a.csv')

# ### Question 2a ###

# #### AL Selection for 2a ####

# In[239]:

# df


# In[240]:

df_al_hr = df[df['League'] == 'AL']
df_al_hr[:5]

# In[241]:

homeruns_al = pd.DataFrame(df_al_hr['HR'], dtype=np.float)

# #### NL Selection for 2a ####

# In[242]:

df_nl_hr = df[df['League'] == 'NL']
df_nl_hr[:5]

# In[243]:

homeruns_nl = pd.DataFrame(df_nl_hr['HR'], dtype=np.float)
print("AL League's average numver of homeruns is", homeruns_al['HR'].mean())
print("NL League's average numver of homeruns is", homeruns_nl['HR'].mean())

# In[244]:

print('AL had the greatest.')

# ### Question 2b ###

# #### AL Selection for 2b ####

# In[245]:

first_inning_selection = driver.find_element_by_xpath('//*[@id="st_hitting_hitting_splits"]/optgroup[12]/option[1]')
first_inning_selection.click()

# In[246]:

data_head_q2b = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df2 = pd.DataFrame(columns=data_head_q2b)

# In[247]:

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")

# In[248]:

data_context_q2b = []
for a in soup.tbody.find_all('tr'):
    for b in a.find_all('td'):
        data_context_q2b.append(b.text)
clean_data_context_q2b = []
for c in range(int(len(data_context_q2b) / len(data_head_q2b))):
    d = data_context_q2b[c * len(data_head_q2b):(c + 1) * len(data_head_q2b)]
    clean_data_context_q2b.append(d)

# In[249]:

for i in range(30):
    df2.loc[i] = clean_data_context_q2b[i]

# In[250]:

df2[:5]

# In[251]:

# Export csv file
df2.to_csv('Question 2b.csv')

# In[252]:

df_al_first_hr = df2[df2['League'] == 'AL']
df_al_first_hr[:5]

# In[253]:

homeruns_al_firstinning = pd.DataFrame(df_al_first_hr['HR'], dtype=np.float)

# #### NL Selection for 2b ####

# In[254]:

df_nl_first_hr = df2[df2['League'] == 'NL']
df_nl_first_hr[:5]

# In[255]:

homeruns_nl_firstinning = pd.DataFrame(df_nl_first_hr['HR'], dtype=np.float)
print("AL League's average numver of homeruns in the first inning is", homeruns_al_firstinning['HR'].mean())
print("NL League's average numver of homeruns in the first inning is", homeruns_nl_firstinning['HR'].mean())

# In[256]:

print('AL had the greatest.')

# ### Question 3a ###

# In[257]:

driver.get('http://www.mlb.com')
stats_header_bar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item--stats')))
stats_header_bar.click()
stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
stats_line_items[0].click()
hitting_season_element = wait.until(EC.element_to_be_clickable((By.ID, 'sp_hitting_season')))
hitting_season_element.click()

# In[258]:

year2017 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sp_hitting_season > option:nth-child(2)')))
year2017.click()

# In[259]:

regular_season_element = driver.find_element_by_xpath('//*[@id="sp_hitting_game_type"]/option[1]')
regular_season_element.click()

# In[260]:

hitting_team_element = driver.find_element_by_xpath('//*[@id="sp_hitting_team_id"]/option[20]')
hitting_team_element.click()

# In[261]:

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")

# In[262]:

data_head_q3a = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df3 = pd.DataFrame(columns=data_head_q3a)

# In[263]:

data_context_q3a = []
for a in soup.tbody.find_all('tr'):
    for b in a.find_all('td'):
        data_context_q3a.append(b.text)
clean_data_context_q3a = []
for c in range(int(len(data_context_q3a) / len(data_head_q3a))):
    d = data_context_q3a[c * len(data_head_q3a):(c + 1) * len(data_head_q3a)]
    clean_data_context_q3a.append(d)

# In[264]:

for i in range(44):
    df3.loc[i] = clean_data_context_q3a[i]

# In[265]:

df3.to_csv('Question 3.csv')
question3 = pd.read_csv('/Users/yulanyu/Downloads/Question 3.csv')

# In[295]:

pd.set_option('display.max_columns', 500)

# In[296]:

question3a = question3[question3['AB'] >= 30]
question3a[:10]

# In[297]:

# We can find out the player is Cooper, G.
# Next step is to find his full name.


# In[298]:

player_select = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody/tr[4]/td[2]/a')
player_select.click()

# In[299]:

player_name = driver.find_element_by_class_name('player-name')

# In[300]:

print('The full name of best overall batting average in the2017 regular season is',
      player_name.text, ', and his position is', question3a_filter.iloc[0, 6])

# ### Question 3b RF ###

# In[332]:

df3_rf = df3[df3['Pos'] == 'RF']
df3_rf

# In[333]:

# We can find that the player has higher AVG is Judge, A.
# Next step is to find his full name.


# In[334]:

driver.back()

# In[352]:

player_rf_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody/tr[8]/td[2]/a')))
player_rf_select.click()

# In[353]:

player_name_rf = driver.find_element_by_class_name('player-name')
print ('Player', player_name_rf.text, 'has the best overall batting average in the position of', df3_rf.iloc[0, 5])

# ### Question 3b CF ###

# In[356]:

df3_cf = df3[df3['Pos'] == 'CF']
df3_cf

# In[357]:

# We can find that the player has highest AVG is Hicks, A.
# Next step is to find his full name.


# In[364]:

driver.back()

# In[365]:

player_cf_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody/tr[12]/td[2]/a')))
player_cf_select.click()

# In[366]:

player_name_cf = driver.find_element_by_class_name('player-name')

# In[367]:

print ('Player', player_name_cf.text, 'has the best overall batting average in the position of', df3_cf.iloc[0, 5])

# ### Question 3b LF ###

# In[368]:

df3_lf = df3[df3['Pos'] == 'LF']
df3_lf

# In[369]:

# We can find that the player has higher AVG is Gardner, B.
# Next step is to find his full name.


# In[370]:

driver.back()

# In[371]:

player_lf_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody/tr[13]/td[2]/a')))
player_lf_select.click()

# In[372]:

player_name_lf = driver.find_element_by_class_name('player-name')

# In[373]:

print ('Player', player_name_lf.text, 'has the best overall batting average in the position of', df3_lf.iloc[0, 5])

# ### Question 4 ###

# In[384]:

driver.get('http://www.mlb.com')
wait = WebDriverWait(driver, 10)
stats_header_bar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item--stats')))
stats_header_bar.click()

# In[385]:

stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
stats_line_items[0].click()

# In[386]:

hitting_season_element = wait.until(EC.element_to_be_clickable((By.ID, 'sp_hitting_season')))
hitting_season_element.click()
year2015 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sp_hitting_season > option:nth-child(4)')))
year2015.click()

# In[387]:

regular_season_element = driver.find_element_by_xpath('//*[@id="sp_hitting_game_type"]/option[1]')
regular_season_element.click()

# In[388]:

al_selection = driver.find_element_by_xpath(
    '/html/body/div[2]/div/div[3]/div/div[1]/div[3]/div/div[1]/div[2]/fieldset[1]/label[2]/span')
al_selection.click()

# In[393]:

qualifiers_selection = driver.find_element_by_xpath(
    '/html/body/div[2]/div/div[3]/div/div[1]/div[3]/div/div[1]/div[1]/fieldset[5]/label[2]/span')
qualifiers_selection.click()

# In[394]:

data_head_q4a = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df4a = pd.DataFrame(columns=data_head_q4a)

# In[395]:

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")

# In[396]:

data_context_q4a = []
for a in soup.tbody.find_all('tr'):
    for b in a.find_all('td'):
        data_context_q4a.append(b.text)
clean_data_context_q4a = []
for c in range(int(len(data_context_q4a) / len(data_head_q4a))):
    d = data_context_q4a[c * len(data_head_q4a):(c + 1) * len(data_head_q4a)]
    clean_data_context_q4a.append(d)

# In[399]:

for i in range(50):
    df4a.loc[i] = clean_data_context_q4a[i]

# In[401]:

df4a[:5]

# In[402]:

next_page = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[1]/div[10]/fieldset/button[4]')
next_page.click()

# In[403]:

data_head_q4b = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df4b = pd.DataFrame(columns=data_head_q4b)

# In[404]:

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")

# In[405]:

data_context_q4b = []
for a in soup.tbody.find_all('tr'):
    for b in a.find_all('td'):
        data_context_q4b.append(b.text)
clean_data_context_q4b = []
for c in range(int(len(data_context_q4b) / len(data_head_q4b))):
    d = data_context_q4b[c * len(data_head_q4b):(c + 1) * len(data_head_q4b)]
    clean_data_context_q4b.append(d)

# In[406]:

for i in range(19):
    df4b.loc[i] = clean_data_context_q4b[i]

# In[408]:

df4b[:5]

# In[441]:

frame = [df4a, df4b]
df4 = pd.concat(frame)
df4.reset_index()
df4_sort = df4.sort_values(by=['AB'], ascending=False)
df4_sort[:5]

# In[425]:

# We can find that the player has higher AVG is Altuve, J.
# Next step is to find his full name.


# In[426]:

driver.back()

# In[448]:

player4_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/div[8]/table/tbody/tr[3]/td[2]/a')))
player4_select.click()

# In[449]:

player4_name = driver.find_element_by_class_name('player-name')

# In[450]:

# Next, find his full team name.


# In[451]:

player4_team = driver.find_element_by_xpath('//*[@id="roster-search"]/div/div[2]/div[3]/select/option[12]')

# In[455]:

print ('The player had the most at bats is', player4_name.text, ', his team is', player4_team.text,
       ',and his position is', df4_sort.iloc[0, 5])

# In[539]:

df4.to_csv('Question 4.csv')

# ### Question 5 ###

# In[508]:

driver.get('http://www.mlb.com')

# In[509]:

stats_header_bar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'megamenu-navbar-overflow__menu-item--stats')))
stats_header_bar.click()

# In[510]:

stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
stats_line_items[0].click()

# In[511]:

hitting_season_element = wait.until(EC.element_to_be_clickable((By.ID, 'sp_hitting_season')))
hitting_season_element.click()
year2014 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sp_hitting_season > option:nth-child(5)')))
year2014.click()

# In[513]:

all_star_element = driver.find_element_by_xpath('//*[@id="sp_hitting_game_type"]')
all_star_element.click()

# In[514]:

all_star_selection = driver.find_element_by_css_selector('#sp_hitting_game_type > option:nth-child(2)')
all_star_selection.click()

# In[515]:

data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(data_html, "html5lib")

# In[516]:

data_head_q5 = [t.text.replace("▼", "") for t in soup.thead.find_all("th")]
df5 = pd.DataFrame(columns=data_head_q5)

# In[517]:

data_context_q5 = []
for a in soup.tbody.find_all('tr'):
    for b in a.find_all('td'):
        data_context_q5.append(b.text)
clean_data_context_q5 = []
for c in range(int(len(data_context_q5) / len(data_head_q5))):
    d = data_context_q5[c * len(data_head_q5):(c + 1) * len(data_head_q5)]
    clean_data_context_q5.append(d)

# In[522]:

for i in range(41):
    df5.loc[i] = clean_data_context_q5[i]

# In[524]:

df5[:5]

# In[540]:

df5.to_csv('Question 5.csv')

# In[533]:

as_list = df5['Player']
player_list = []
for i in range(41):
    player_list.append(as_list[i])

name_list = set(player_list)

# In[527]:

latin_country = '''Argentina;Bolivia;Brazil;Chile;Colombia;Costa Rica;Cuba;Dominican Republic;Ecuador;El Salvador;French Guiana;Guadeloupe;Guatemala;Haiti;Honduras;Martinique;Mexico;Nicaragua;Panama;Paraguay;Peru;Puerto Rico;Saint Barthélemy;Saint Martin;Uruguay;Venezuela'''
latin_list = latin_country.split(';')

# In[538]:

name_list = []
data_div_all_star = driver.find_element_by_id('datagrid')

data_html_all_star = data_div_all_star.get_attribute('innerHTML')

soup_all_star = bs4.BeautifulSoup(data_html_all_star, 'html5lib')
for name in soup_all_star.tbody.find_all('a'):
    z = 0
    if len(name_list) == 0:
        name_list.append(name.text)
    else:
        for i in range(len(name_list)):
            if name.text == name_list[i]:
                z = 1
        if z == 0:
            name_list.append(name.text)

# In[537]:

wait = WebDriverWait(driver, 10)
q5 = []
for name in name_list:
    player_bar = driver.find_elements_by_link_text(name)
    for k in range(len(player_bar)):

        print(name)
        time.sleep(3)
        player_bar_temp = driver.find_elements_by_link_text(name)
        player_bar_temp[k].click()
        player_bio = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'player-bio')))

        for country in latin_list:
            if country in player_bio.text:
                player_name = driver.find_element_by_class_name('full-name').text
                datahtml = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'dropdown.team'))).text
                team_name = datahtml.split('\n')[0].strip()
                print('player_name:', player_name)
                q5.append(player_name)
                print('team_name:', team_name)
                q5.append(team_name)

        time.sleep(5)
        driver.back()

# ### Question 6 ###

# In[542]:

import http.client, urllib.request, urllib.parse, urllib.error, base64
import json


# In[543]:

def api(html):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'e4de2addd38245e59c32a8be76dcedb2',
    }
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", html, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close
    return data


# In[544]:

data_stats_stadium = api("/v3/mlb/stats/json/Stadiums")
time.sleep(5)
data_stats_stadium = json.loads(data_stats_stadium)
data_stats_stadium

# In[546]:

match_info = []
for i in data_stats_stadium:
    match_info.append([i["StadiumID"], i["Name"], i["City"], i["State"]])
data_stats_game = json.loads(api("/v3/mlb/stats/json/Games/2016"))
data_stats_game
game_info = []
for i in data_stats_game:
    game_info.append([i["HomeTeam"], i["AwayTeam"], i["DateTime"][0:10], i["StadiumID"]])

game_info

# In[547]:

general_info = []

for i in match_info:
    for j in game_info:
        if i[0] == j[3]:
            temp = j[:-1] + i[1:]
            general_info.append(temp)

general_info

# In[548]:

data_q6 = []
for a in general_info:

    if 'HOU' in a:
        data_q6.append(a)

data_q6

# In[549]:

df6 = pd.DataFrame(columns=['Home Team', 'Away Team', 'Date', 'Stadium Name', 'City', 'State'])

for i in range(len(data_q6)):
    df6.loc[i] = data_q6[i]

df6

# In[550]:

df6.to_csv('Question 6.csv')

