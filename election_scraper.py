"""
projekt_3.py: Třetí projekt do Engeto Online Python Akademie
author: Tereza Trčková
email: terda.trckova@seznam.cz
discord: tereza_trckova
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def get_obec_links(uzemi_url):
    """Získá odkazy na jednotlivé obce ze všech tabulek na dané stránce."""
    response = requests.get(uzemi_url)
    if response.status_code != 200:
        raise ValueError(f"Chyba při načítání stránky: {uzemi_url}. Status kód: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table", {"class": "table"})
    if not tables:
        raise ValueError("Stránka neobsahuje žádné tabulky. URL: " + uzemi_url)

    obce_links = []
    for table in tables:
        rows = table.find_all("tr")[2:]  # Vynechání hlavičky tabulky
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 0:
                obec_name = cols[1].text.strip()
                link_tag = cols[0].find("a")
                if link_tag:
                    link = link_tag["href"]
                    full_link = BASE_URL + link
                    obce_links.append((obec_name, full_link))

    return obce_links

def get_obec_results(obec_url):
    """Stáhne a vyparsuje volební výsledky pro konkrétní obec."""
    response = requests.get(obec_url)
    if response.status_code != 200:
        raise ValueError(f"Chyba při načítání stránky: {obec_url}. Status kód: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Získání kódu obce z URL
    code_param = obec_url.split("xobec=")[1].split("&")[0]

    # Získání názvu obce
    kod_obce_h3 = soup.find("h3")
    if kod_obce_h3 is None:
        raise ValueError(f"Stránka neobsahuje nadpis s kódem obce. URL: {obec_url}")
    nazev_obce = " ".join(kod_obce_h3.text.split()[1:])

    # Získání údajů z hlavní tabulky
    main_table = soup.find("table", {"id": "ps311_t1"})
    if main_table is None:
        raise ValueError(f"Stránka neobsahuje hlavní tabulku. URL: {obec_url}")

    main_rows = main_table.find_all("tr")
    if len(main_rows) < 2:
        raise ValueError(f"Hlavní tabulka neobsahuje dostatek řádků. URL: {obec_url}")

    main_data_row = main_rows[2].find_all("td")
    if len(main_data_row) < 8:
        raise ValueError(f"Hlavní tabulka neobsahuje očekávaný počet datových sloupců. URL: {obec_url}")

    # Funkce pro bezpečné převedení hodnoty na číslo
    def safe_int(value):
        return int(value.replace('\xa0', '').replace(' ', '')) if value.strip() != '-' else 0

    volici_v_seznamu = safe_int(main_data_row[3].text)
    vydane_obalky = safe_int(main_data_row[4].text)
    platne_hlasy = safe_int(main_data_row[7].text)

    # Získání údajů z obou tabulek politických stran
    tables = soup.find_all("table", {"class": "table"})[1:]
    strany = {}
    for table in tables:
        for row in table.find_all("tr")[2:]:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue
            nazev_strany = cols[1].text.strip()
            hlasy = safe_int(cols[2].text)
            strany[nazev_strany] = hlasy

    # Vrácení dat jako slovníku
    return {
        "code": code_param,
        "location": nazev_obce,
        "registered": volici_v_seznamu,
        "envelopes": vydane_obalky,
        "valid": platne_hlasy,
        **strany
    }

def main():
    parser = argparse.ArgumentParser(description="Scraper volebních výsledků 2017")
    parser.add_argument("uzemi_url", help="URL územního celku ke scrapování (např. https://...)")
    parser.add_argument("output_file", help="Název výstupního CSV souboru")
    args = parser.parse_args()

    # Kontrola, zda argumenty jsou zadány
    if not args.uzemi_url or not args.output_file:
        parser.error("Je nutné zadat oba argumenty: URL a název výstupního souboru.")

    # Kontrola URL
    if not (args.uzemi_url.startswith("http://") or args.uzemi_url.startswith("https://")):
        parser.error("Argument uzemi_url musí být platné URL začínající na 'http://' nebo 'https://'.")

    try:
        obce_links = get_obec_links(args.uzemi_url)
        print(f"Stahuji data z vybraného URL: {args.uzemi_url}")
        print(f"To znamená celkem {len(obce_links)} obcí ke zpracování")

        data = []
        for obec_name, obec_url in obce_links:
            obec_data = get_obec_results(obec_url)
            obec_data["location"] = obec_name
            data.append(obec_data)

        # Uložení do CSV
        df = pd.DataFrame(data)
        df.to_csv(args.output_file, index=False, encoding='utf-8-sig', sep=',')
        print(f"Ukládám do souboru: {args.output_file}")
        print("Ukončuji election-scraper")

    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()




