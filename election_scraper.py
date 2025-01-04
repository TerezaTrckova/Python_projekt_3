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

# -------------------- Helper functions --------------------
def fetch_page_content(url):
    """Fetches the content of a web page and returns it as a BeautifulSoup object."""
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error while fetching the page: {url}. Status code: {response.status_code}")
    return BeautifulSoup(response.content, 'html.parser')

def safe_int(value):
    """Converts a string to an integer, handling non-breaking spaces and empty values."""
    return int(value.replace('\xa0', '').replace(' ', '')) if value.strip() != '-' else 0

def parse_row(row, index_name, index_link=None):
    """Parses a table row and extracts specified columns."""
    cols = row.find_all("td")
    if len(cols) == 0 or (index_link is not None and not cols[0].find("a")):
        return None
    name = cols[index_name].text.strip()
    link = f"{BASE_URL}{cols[0].find('a')['href']}" if index_link is not None else None
    return (name, link) if link else (name,)
# -------------------- Functions for processing location data --------------------
def get_location_links(uzemi_url):
    """Fetches links to individual locations from all tables on the page."""
    soup = fetch_page_content(uzemi_url)
    tables = soup.find_all("table", {"class": "table"})
    if not tables:
        raise ValueError(f"No tables found on the page: {uzemi_url}")

    location_links = []
    for table in tables:
        rows = table.find_all("tr")[2:]  # Skip header rows
        for row in rows:
            link_data = parse_row(row, 1, 0)
            if link_data:
                location_links.append(link_data)
    return location_links

def get_location_info(soup, location_url):
    """Extracts the location name and location code from the page and URL."""
    header = soup.find("h3")
    if header is None:
        raise ValueError("Page header with the location name is missing.")
    location_name = " ".join(header.text.split()[1:])
    location_code = location_url.split("xobec=")[1].split("&")[0]
    return {"code": location_code, "location": location_name}

def get_main_table_data(soup):
    """Extracts data from the main table (registered voters, envelopes, valid votes)."""
    main_table = soup.find("table", {"id": "ps311_t1"})
    if main_table is None:
        raise ValueError("The main table is missing.")
    main_rows = main_table.find_all("tr")
    if len(main_rows) < 3:
        raise ValueError("The main table does not contain enough rows.")
    main_data_row = main_rows[2].find_all("td")
    if len(main_data_row) < 8:
        raise ValueError("The main table does not contain the expected number of columns.")
    return {
        "registered": safe_int(main_data_row[3].text),
        "envelopes": safe_int(main_data_row[4].text),
        "valid": safe_int(main_data_row[7].text),
    }

def get_party_votes_data(soup):
    """Extracts votes for each political party from the tables."""
    party_tables = soup.find_all("table", {"class": "table"})[1:]  # Skip the first table (main table)
    parties = {}
    for table in party_tables:
        for row in table.find_all("tr")[2:]:  # Skip header rows
            party_name, = parse_row(row, 1)
            votes = safe_int(row.find_all("td")[2].text)
            if party_name:
                parties[party_name] = votes
    return parties

def process_location(location_url):
    """Fetches and parses the election results for a specific location."""
    soup = fetch_page_content(location_url)

    # Get location info (name and code)
    location_info = get_location_info(soup, location_url)

    # Get voter statistics from the main table
    main_data = get_main_table_data(soup)

    # Get votes for political parties
    party_data = get_party_votes_data(soup)

    # Combine all data into one dictionary
    return {**location_info, **main_data, **party_data}

# -------------------- Main program function --------------------
def main():
    parser = argparse.ArgumentParser(description="Election results scraper 2017")
    parser.add_argument("uzemi_url", help="The URL of the administrative unit to scrape (e.g., https://...)")
    parser.add_argument("output_file", help="The name of the output CSV file")
    args = parser.parse_args()

    try:
        location_links = get_location_links(args.uzemi_url)
        print(f"Fetching data from the specified URL: {args.uzemi_url}")
        print(f"There are {len(location_links)} locations to process")

        data = []
        for location_name, location_url in location_links:
            try:
                location_info = process_location(location_url)
                location_info["location"] = location_name  # Ensure correct name assignment
                data.append(location_info)
            except ValueError as e:
                print(f"Skipping location due to error: {location_name}. Details: {e}")

        df = pd.DataFrame(data)
        # Save data to CSV file
        df.to_csv(args.output_file, index=False, encoding='utf-8-sig', sep=',')
        print(f"Results saved to file: {args.output_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
