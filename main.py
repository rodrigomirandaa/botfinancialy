import pandas as pd
import os
import pygsheets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv

#https://selenium-python.readthedocs.io/locating-elements.html
#https://pygsheets.readthedocs.io/en/stable/index.html 
#https://pandas.pydata.org/docs/

pd.set_option('display.float_format', '{:,.2f}'.format)


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


# Remove a primeira linha
df = df.iloc[1:]

# Lista das colunas numéricas
cols_numericas = ['Cotação', 'P/L', 'P/VP', 'PSR', 'Div.Yield', 'P/Ativo', 'P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq',
                  'EV/EBIT', 'EV/EBITDA', 'Mrg Ebit', 'Mrg. Líq.', 'Liq. Corr.', 'ROIC', 'ROE', 'Liq.2meses',
                  'Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a']

# Iterar sobre as colunas numéricas e aplicar o tratamento
for col in cols_numericas:
    df[col] = df[col].str.replace('.', '').str.replace(',', '.').str.rstrip('%').astype(float)


# Lista das colunas para analise
cols_analise = ['Papel', 'Cotação', 'P/L', 'P/VP', 'Div.Yield', 'P/EBIT','EV/EBIT', 'EV/EBITDA', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a',]
print(df[cols_analise])

#carrega variaveis de ambiente
load_dotenv()

#acessando var google service acoount
gc = pygsheets.authorize(service_account_env_var= "GOOGLE_SERVICE_ACCOUNT")

#id da planilha
sheet = gc.open_by_key("1EbonaYCca30BiNK47BCbuezIKQhR00qlnWwk1XyNmi8")
worksheet = sheet.worksheet_by_title("input")

worksheet.set_dataframe(df[cols_analise], "A1", copy_index=False, copy_head=True, extend=False, fit=False, escape_formulae=False)

#filtros no código
#formula via código
