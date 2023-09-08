import pandas as pd
import os
import pygsheets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv


#documentação:https://selenium-python.readthedocs.io/locating-elements.html
#documentação:https://pygsheets.readthedocs.io/en/stable/index.html 


driver = webdriver.Chrome()
driver.get("https://fundamentus.com.br/resultado.php")

table = driver.find_element(By.ID,"resultado")

soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

table_headers = []
for th in soup.find_all('th'):
    table_headers.append(th.text)

table_data = []
for row in soup.find_all('tr'):
    columns = row.find_all('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    table_data.append(output_row)

df = pd.DataFrame(table_data, columns=table_headers)

print(df.head())

#carrega variaveis de ambiente
load_dotenv()

#acessando var google service acoount
gc = pygsheets.authorize(service_account_env_var= "GOOGLE_SERVICE_ACCOUNT")

#id da planilha
sheet = gc.open_by_key("1EbonaYCca30BiNK47BCbuezIKQhR00qlnWwk1XyNmi8")
worksheet = sheet.worksheet_by_title("input")

worksheet.set_dataframe(df, "A1", copy_index=False, copy_head=True, extend=False, fit=False, escape_formulae=False)

