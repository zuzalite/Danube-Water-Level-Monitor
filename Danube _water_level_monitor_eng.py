import requests
from bs4 import BeautifulSoup
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def translate_date(date_string):
    # Magyar hónapnevek megfeleltetése angolra
    months = {
        "január": "January", "február": "February", "március": "March",
        "április": "April", "május": "May", "június": "June",
        "július": "July", "augusztus": "August", "szeptember": "September",
        "október": "October", "november": "November", "december": "December"
    }
    
    # Fordítás és az "Észlelés" szó cseréje
    translated = date_string.replace("Észlelés:", "Observation:")
    for hun, eng in months.items():
        translated = translated.replace(hun, eng)
    return translated

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    date_url = "https://www.hydroinfo.hu/tables/dunhid_f.html"
    date_res = requests.get(date_url, headers=headers, verify=False, timeout=10)
    soup_date = BeautifulSoup(date_res.text, 'html.parser')
    
    date_text = "Date not found"
    for font in soup_date.find_all('font'):
        if "Észlelés" in font.get_text():
            # Itt hívjuk meg a fordító függvényt
            date_text = translate_date(font.get_text().strip())
            break

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
print("Danube Budapest monitor started...")
while True:
    adat = get_data()
    if adat:
        print(f"\n--- {adat['datum']} ---")
        print(f"[{time.strftime('%H:%M:%S')}] {adat['nev']} ({adat['folyo']}, code: {adat['kod']})")
        print(f" - Water level (yesterday morning): {adat['t_reggel']} cm")
        print(f" - Water level (yesterday evening):   {adat['t_este']} cm")
        print(f" - Water level (today morning):     {adat['m_reggel']} cm")
        print(f" - Change (24h):           {adat['valtozas']} cm")
        print(f" - Discharge:                 {adat['hozam']} m3/s")
        print(f" - Water temperature:           {adat['homerseklet']} °C")
        print(f" - Ice condition:                 {adat['jeg']}")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Data not found.")
    
    print(f"[{time.strftime('%H:%M:%S')}] Waiting 60 seconds for next update...")
    time.sleep(60)