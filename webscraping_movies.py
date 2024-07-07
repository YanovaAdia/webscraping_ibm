import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'movies.db'
csv_path = 'top_50.csv'
table_name = 'top_50'
df = pd.DataFrame()

page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')

tables = soup.find_all('tbody')
rows_of_tables1 = tables[0].find_all('tr')

for row in rows_of_tables1[1:51]:
    col = row.find_all('td')[:3]
    if len(col) != 0:
        data_dict = {
            'average_rank':col[0].contents[0],
            'film':col[1].contents[0],
            'year':col[2].contents[0]
        }
        df = pd.concat([df, pd.DataFrame(data_dict, index=[0])], ignore_index=True)
    else:
        continue

df.to_csv(csv_path)

conn = sqlite3.connect(db_name)
with conn:
    df.to_sql(table_name, conn, if_exists='replace', index=False)