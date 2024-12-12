"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tereza Trčková
email: petr.svetr@gmail.com
discord: Petr Svetr#4490
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def get_obec_links(uzemi_url):
    """Získá odkazy na jednotlivé obce z daného územního celku."""
    response = requests.get(uzemi_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find("table", {"class": "table"})
    rows = table.find_all("tr")[2:]  # Vynecháme hlavičku tabulky

    obce_links = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0:
            obec_name = cols[1].text.strip()
            link = cols[-1].find("a")['href']  # Sloupec s odkazem "Výběr obce"
            full_link = BASE_URL + link
            obce_links.append((obec_name, full_link))
    return obce_links

def get_obec_results(obec_url):
    """Stáhne a vyparsuje volební výsledky pro konkrétní obec."""
    response = requests.get(obec_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Získáme základní informace o obci
    kod_obce = soup.find("h3").text.split()[0]  # První číslo v názvu obce
    nazev_obce = " ".join(soup.find("h3").text.split()[1:])  # Zbytek názvu

    # Získáme tabulku s hlavními čísly
    table = soup.find("table", {"id": "ps311_t1"})
    rows = table.find_all("tr")

    volici_v_seznamu = int(rows[0].find_all("td")[1].text.replace('\xa0', '').replace(' ', ''))
    vydane_obalky = int(rows[1].find_all("td")[1].text.replace('\xa0', '').replace(' ', ''))
    platne_hlasy = int(rows[2].find_all("td")[1].text.replace('\xa0', '').replace(' ', ''))

    # Získáme hlasy pro jednotlivé strany
    strany_table = soup.find("table", {"id": "ps311_t2"})
    strany = {}
    for row in strany_table.find_all("tr")[2:]:
        cols = row.find_all("td")
        nazev_strany = cols[1].text.strip()
        hlasy = int(cols[2].text.replace('\xa0', '').replace(' ', ''))
        strany[nazev_strany] = hlasy

    return {
        "code": kod_obce,
        "location": nazev_obce,
        "registered": volici_v_seznamu,
        "envelopes": vydane_obalky,
        "valid": platne_hlasy,
        **strany
    }

def main():
    parser = argparse.ArgumentParser(description="Scraper volebních výsledků 2017")
    parser.add_argument("uzemi_url", help="URL územního celku ke scrapování")
    parser.add_argument("output_file", help="Název výstupního CSV souboru")
    args = parser.parse_args()

    try:
        obce_links = get_obec_links(args.uzemi_url)
        print(f"Získávám výsledky pro {len(obce_links)} obcí...")

        data = []
        for obec_name, obec_url in obce_links:
            print(f"Stahuji data pro obec: {obec_name}")
            data.append(get_obec_results(obec_url))

        # Uložení do CSV
        df = pd.DataFrame(data)
        df.to_csv(args.output_file, index=False, encoding='utf-8')
        print(f"Výsledky uloženy do {args.output_file}")

    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()
