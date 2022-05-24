import warnings

from datetime import date
import pandas as pd 
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

df_ori = pd.read_excel('Magic.xlsx', sheet_name = 'Carpeta')
df_cartas = df_ori['Carta']
df = df_ori.loc[:, 'Link'].to_list()


with requests.Session() as s:
    precios = []
    i = 0
    for item in df:
        page = s.get(item, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(page.content, 'html.parser')
        if 'cardkingdom' in item:
            element = soup.find(class_="stylePrice").get_text()
        else:
            element = soup.find(class_="price price--withoutTax").get_text()
        element = element.replace('$', '')
        element = float(element)
        if '(PL)' in df_cartas[i]:
            print('Ta usada la wea')
            element = element * 0.80
        if '(HP)' in df_cartas[i]:
            print('Ta MUY usada la wea')
            element = element * 0.33
        precios.append(element)
        print(f'{df_cartas[i]} - {element}')
        i += 1

df_final = pd.DataFrame({'Cartas': df_cartas,'Precio': precios})
today = date.today()
df_final.to_excel(f'PreciosActualizados{today}.xlsx')