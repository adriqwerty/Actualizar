import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def obtener_tabla(isin):
    url = f"https://markets.ft.com/data/funds/tearsheet/historical?s={isin}:EUR"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    table = soup.find("table")
    if not table:
        print("No se encontró la tabla")
        return []

    filas = table.find_all("tr")

    datos = []

    for fila in filas[1:]:  # saltar cabecera
        columnas = fila.find_all("td")
        if len(columnas) < 5:
            continue

        fecha = columnas[0].text.strip()
        open_price = columnas[1].text.strip().replace(",", "")
        high = columnas[2].text.strip().replace(",", "")
        low = columnas[3].text.strip().replace(",", "")
        close = columnas[4].text.strip().replace(",", "")

        datos.append({
            "fecha": fecha,
            "open": float(open_price) if open_price else None,
            "high": float(high) if high else None,
            "low": float(low) if low else None,
            "close": float(close) if close else None,
        })

    return datos

def obtener_precio_y_fecha_alt(isin):
    website = "https://markets.ft.com/data/funds/tearsheet/historical?s="+isin+":EUR"
    print(website)
    if not website:
        return None, None
    result = requests.get(website)
    soup = BeautifulSoup(result.text, 'lxml')
    precio_box = soup.find('span', class_='mod-ui-data-list__value')
    if not precio_box:
        print(f"⚠️ No se encontró el precio para {isin} en FT.")
        return None, None
    precio_str = precio_box.text.strip()
    precio_str = precio_str.replace(',', '')  # elimina separador de miles
    precio = float(precio_str)
    #precio=float(precio_box.text.strip())
    fecha_box = soup.find('div', class_='mod-disclaimer')
    match = re.search(r'as of ([A-Za-z]+ \d{1,2} \d{4})', fecha_box.text.strip())
    fecha_str = match.group(1)
    fecha_obj = datetime.strptime(fecha_str, "%b %d %Y")
    return round(precio, 2) if precio else None, fecha_obj

print(obtener_tabla("LU1598719752"))