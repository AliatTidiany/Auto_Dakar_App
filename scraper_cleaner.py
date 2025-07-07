import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

#Créer le dossier data s'il n'existe pas pour stocker les fichiers CSV
# pour le scraping pr
def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

#Sépare la marque et l'année du titre 
def extract_marque_annee(title_text):
    parts = title_text.split()
    if not parts:
        return "", ""
    annee = parts[-1] if parts[-1].isdigit() else ""
    marque = " ".join(parts[:-1]) if annee else title_text
    return marque, annee

# Fonction générique pour scraper les données de Dakar Auto, en fonction du type de données (voitures, motos, locations)
def scrape_generic(url, type_data, output_file, num_pages=25):
    data = []
    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}...")
        r = requests.get(f"{url}?page={page}")
        soup = BeautifulSoup(r.content, "html.parser")
        cards = soup.find_all("div", class_="listing-card__details")

        for item in cards:
            try:
                title_tag = item.find_previous("h2", class_="listing-card__header__title")
                title_text = title_tag.get_text(strip=True) if title_tag else ""
                marque, annee = extract_marque_annee(title_text)

                price_tag = item.find_previous("h3", class_="listing-card__header__price")
                prix = price_tag.get_text(strip=True) if price_tag else ""

                addr_tag = item.select_one("div.entry-zone-address")
                adresse = addr_tag.get_text(" ", strip=True) if addr_tag else ""

                props = item.select("ul.listing-card__attribute-list li")
                kilometrage = ""
                boite = ""
                carburant = ""
                for p in props:
                    txt = p.get_text(strip=True)
                    if "km" in txt:
                        kilometrage = txt
                    elif "Manuelle" in txt or "Automatique" in txt:
                        boite = txt
                    elif "Essence" in txt or "Diesel" in txt:
                        carburant = txt

                owner_tag = item.find_next("p", class_="time-author")
                proprio = owner_tag.get_text(strip=True).replace("Par ", "") if owner_tag else ""

                if type_data == "voitures":
                    row = [marque, annee, prix, adresse, kilometrage, boite, carburant, proprio]
                elif type_data == "motos":
                    row = [marque, annee, prix, adresse, kilometrage, proprio]
                else:
                    row = [marque, annee, prix, adresse, proprio]

                data.append(row)

            except Exception as e:
                print(f"Erreur sur un item : {e}")
                continue

    columns = {
        "voitures": ["marque", "année", "prix", "adresse", "kilométrage", "boite", "carburant", "propriétaire"],
        "motos": ["marque", "année", "prix", "adresse", "kilométrage", "propriétaire"],
        "locations": ["marque", "année", "prix", "adresse", "propriétaire"]
    }

    df = pd.DataFrame(data, columns=columns[type_data])
    ensure_data_dir()
    df.to_csv(output_file, index=False)
    return df

# Scraping des données nettoyées pour voitures, motos et locations
def scrape_voitures_clean(num_pages=25):
    return scrape_generic("https://dakar-auto.com/senegal/voitures-4", "voitures", "data/voitures_clean.csv", num_pages)

def scrape_motos_clean(num_pages=25):
    return scrape_generic("https://dakar-auto.com/senegal/motos-and-scooters-3", "motos", "data/motos_clean.csv", num_pages)

def scrape_locations_clean(num_pages=25):
    return scrape_generic("https://dakar-auto.com/senegal/location-de-voitures-19", "locations", "data/locations_clean.csv", num_pages)
