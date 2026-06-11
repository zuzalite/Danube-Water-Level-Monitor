import requests
from bs4 import BeautifulSoup
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 1. Dátum lekérése a dunhid_f.html-ből
    date_url = "https://www.hydroinfo.hu/tables/dunhid_f.html"
    date_res = requests.get(date_url, headers=headers, verify=False, timeout=10)
    soup_date = BeautifulSoup(date_res.text, 'html.parser')
    date_text = "Dátum nem található"
    for font in soup_date.find_all('font'):
        if "Észlelés" in font.get_text():
            date_text = font.get_text().strip()
            break

    # 2. Adatok lekérése a dunhif_a.html-ből (ez a táblázat forrása)
    data_url = "https://www.hydroinfo.hu/tables/dunhif_a.html"
    data_res = requests.get(data_url, headers=headers, verify=False, timeout=10)
    soup_data = BeautifulSoup(data_res.text, 'html.parser')
    
    for row in soup_data.find_all('tr'):
        if "442027" in row.text:
            cells = row.find_all('td')
            if len(cells) >= 10:
                return {
                    'datum': date_text,
                    'nev': cells[1].text.strip(),
                    'folyo': cells[2].text.strip(),
                    'kod': cells[0].text.strip(),
                    't_reggel': cells[3].text.strip(),
                    't_este': cells[4].text.strip(),
                    'm_reggel': cells[5].text.strip(),
                    'valtozas': cells[6].text.strip(),
                    'hozam': cells[7].text.strip(),
                    'homerseklet': cells[8].text.strip(),
                    'jeg': cells[9].text.strip()
                }
    return None

# Fő program
print("Duna Budapest adatfigyelő elindítva...")
while True:
    adat = get_data()
    if adat:
        print(f"\n--- {adat['datum']} ---")
        print(f"[{time.strftime('%H:%M:%S')}] {adat['nev']} ({adat['folyo']}, kód: {adat['kod']})")
        print(f" - Vízállás (tegnap reggel): {adat['t_reggel']} cm")
        print(f" - Vízállás (tegnap este):   {adat['t_este']} cm")
        print(f" - Vízállás (ma reggel):     {adat['m_reggel']} cm")
        print(f" - Változás (24h):           {adat['valtozas']} cm")
        print(f" - Vízhozam:                 {adat['hozam']} m3/s")
        print(f" - Vízhőmérséklet:           {adat['homerseklet']} °C")
        print(f" - Jégállapot:               {adat['jeg']}")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Adat nem található.")
    
    print(f"[{time.strftime('%H:%M:%S')}] Várakozás 60 másodpercig a következő frissítésig...")
    time.sleep(60)