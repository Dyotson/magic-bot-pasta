import warnings
import csv

import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

warnings.filterwarnings("ignore")

df_ori = pd.read_excel('Magic.xlsx', sheet_name = 'Carpeta')
df_cartas = df_ori['Carta']
df = df_ori.loc[:, 'Link'].to_list()

driver = webdriver.Firefox('.')
precios = []
i = 0
for item in df:
    driver.get(item)
    if 'cardkingdom' in item:
        element = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[3]/div[1]/ul[2]/li[1]/form/div[1]/span[4]').text
    else:
        element = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[1]/div[3]/section[2]/div[1]/div[3]/span[2]').text
    
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
driver.close()

df_final = pd.DataFrame({'Cartas': df_cartas,'Precio': precios})

df_final.to_excel('PreciosActualizadosCarpeta23052.xlsx')