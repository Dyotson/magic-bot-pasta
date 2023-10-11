import warnings

from datetime import date
import pandas as pd
import requests
from bs4 import BeautifulSoup
from rich import print
import multiprocessing


def process_shiit(df, df_cartas):
    page = requests.get(df).text
    soup = BeautifulSoup(page, "html.parser")
    if soup.find(class_="price price--non-sale").get_text() != "\n":
        element = soup.find(class_="price price--non-sale").get_text()
    else:
        element = soup.find(class_="price price--withoutTax").get_text()
    element = element.replace("$", "")
    element = float(element)
    if "(PL)" in df_cartas:
        print("Ta usada la wea")
        element = element * 0.80
    if "(HP)" in df_cartas:
        print("Ta MUY usada la wea")
        element = element * 0.33
    print(f"{df_cartas} - {element}", flush=True)
    return element


if __name__ == "__main__":
    print("Bienvenido al magic-bot-pasta de Jew y Max:\n")
    print("Porfavor, elige tu opcion:")
    print("[bold bright_cyan][1][/bold bright_cyan] Revisar todas las sheets")
    print("[bold bright_cyan][2][/bold bright_cyan] Revisar solo la sheet deseada")

    opcion = input("Elija su opcion: ")

    while True:
        if opcion == "1":
            Shiits = [
                "Carpeta",
                "Arcades",
                "MBT",
                "Coleccion",
                "Bulk",
                "BulkFoil",
                "NivPauper",
            ]
            Shiits = ["Bulk", "BulkFoil", "Arcades", "Coleccion", "NivPauper", "Michis"]
            break
        elif opcion == "2":
            shit = input("Ingrese el nombre del sheet a escanear: ")
            Shiits = []
            Shiits.append(shit)
            break
        else:
            print(
                "[bold red][ERROR][/bold red] Opcion elegida invalida, porfavor elige una opcion valida"
            )
            opcion = input("Elija su opcion: ")

    warnings.filterwarnings("ignore")
    sheetname = shit
    # df_hist = pd.read_excel(f'Historico{sheetname}.xlsx')
    df_ori = pd.read_excel("Magic.xlsx", sheet_name=sheetname)
    df_precios = df_ori["Precio SCG"]
    df_cartas = df_ori["Carta"].to_list()
    df = df_ori.loc[:, "Link"].to_list()

    to_process = []

    for i in range(len(df)):
        nombre = df_cartas[i]
        link = df[i]
        agregar = (link, nombre)
        to_process.append(agregar)

    with multiprocessing.Pool(4) as pool:
        precios = list(pool.starmap(process_shiit, to_process))

    df_final = pd.DataFrame(
        {
            "Cartas": df_cartas,
            "Precio": precios,
            "PrecioAnt": df_precios,
            "Diferencia": precios - df_precios,
        }
    )
    today = date.today()
    # PrecioHist = 'Precio' + today.strftime("%Y-%m-%d")
    # df_hist.assign(PrecioHist = precios)
    # df_hist[PrecioHist] = precios
    df_final.to_excel(f"PreciosActualizados{sheetname}{today}.xlsx")
    # df_hist.to_excel(f'Historico{sheetname}.xlsx')
    print("[bold bright_cyan]El Bot a terminado <3[/bold bright_cyan]")
