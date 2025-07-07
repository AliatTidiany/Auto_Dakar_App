import streamlit as st
import pandas as pd
import io
import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components

from scraper_cleaner import scrape_voitures_clean, scrape_motos_clean, scrape_locations_clean

st.set_page_config(page_title="Auto Dakar App", layout="wide")
st.title("🚗 Auto Dakar App")

menu = st.sidebar.selectbox("📂 Choisissez une section :", [
    "🧹 Scraping propre avec BS4",
    "📥 Télécharger données WebScraper",
    "📊 Dashboard",
    "📝 Évaluation"
])

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

#Scraper propre
if menu == "🧹 Scraping propre avec BS4":
    type_data = st.selectbox("Type de données", ["voitures", "motos", "locations"])
    num_pages = st.number_input("Nombre de pages à scraper", min_value=1, max_value=50, value=5, step=1)
    
    if st.button("Scraper les données nettoyées"):
        if type_data == "voitures":
            df = scrape_voitures_clean(num_pages)
        elif type_data == "motos":
            df = scrape_motos_clean(num_pages)
        else:
            df = scrape_locations_clean(num_pages)

        st.success("✅ Scraping terminé.")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        excel = convert_df_to_excel(df)
        st.download_button("📥 Télécharger en CSV", csv, file_name=f"{type_data}_clean.csv", mime="text/csv")
        st.download_button("📥 Télécharger en Excel", excel, file_name=f"{type_data}_clean.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

#Télécharger brut depuis fichiers déjà existants
elif menu == "📥 Télécharger données WebScraper":
    st.markdown("### 📁 Fichiers WebScraper déjà présents (non nettoyés)")
    type_data = st.selectbox("Fichier brut à télécharger", ["voitures", "motos", "locations"])
    file_path = f"data_web_scraper/{type_data}_webscraper.csv"

    if os.path.exists(file_path):
        try:
            df_raw = pd.read_csv(file_path)
            st.markdown("#### 👁️ Aperçu des données")
            st.dataframe(df_raw.head(10))  # Affiche les 5 premières lignes

            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"📥 Télécharger {type_data}_webscraper.csv",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
    else:
        st.warning(f"❌ Le fichier `{file_path}` est introuvable.")

# Dashboard
elif menu == "📊 Dashboard":
    type_data = st.selectbox("Type de données à visualiser", ["voitures", "motos", "locations"])
    file = f"data/{type_data}_clean.csv"

    if os.path.exists(file):
        try:
            df = pd.read_csv(file)
            st.dataframe(df)

            st.markdown("### 📊 Visualisation")
            if "prix" in df.columns:
                prix_series = (
                    df['prix'].astype(str)
                    .str.replace(r"[^\d]", "", regex=True)
                    .replace("", pd.NA)
                    .dropna()
                    .astype(float)
                )
                if not prix_series.empty:
                    st.write("Histogramme des prix")
                    fig, ax = plt.subplots()
                    sns.histplot(prix_series, bins=20, ax=ax, color='skyblue')
                    ax.set_xlabel("Prix (FCFA)")
                    st.pyplot(fig)
                else:
                    st.warning("Données prix indisponibles.")

            #  Répartition carburant — seulement pour voitures
                if type_data == "voitures" and "carburant" in df.columns:
                    st.write("Répartition du carburant")
                    fig2, ax2 = plt.subplots()
                    sns.countplot(y=df["carburant"], order=df["carburant"].value_counts().index, ax=ax2)
                    st.pyplot(fig2)
            
                #  Répartition par marque — pour tous les types (si dispo)
                if "marque" in df.columns:
                    st.write("Répartition des annonces par marque")
                    fig3, ax3 = plt.subplots()
                    top_marques = df["marque"].value_counts().head(10)
                    sns.barplot(x=top_marques.values, y=top_marques.index, ax=ax3, palette="viridis")
                    ax3.set_xlabel("Nombre d'annonces")
                    ax3.set_ylabel("Marque")
                    st.pyplot(fig3)
                #  Répartition par propriétaire — pour tous les types (si dispo)
                if "propriétaire" in df.columns:
                    st.write("Répartition des annonces par propriétaire")
                    fig4, ax4 = plt.subplots()
                    top_proprio = df["propriétaire"].value_counts().head(10)
                    sns.barplot(x=top_proprio.values, y=top_proprio.index, ax=ax4, palette="plasma")
                    ax4.set_xlabel("Nombre d'annonces")
                    ax4.set_ylabel("Propriétaire")
                    st.pyplot(fig4)


        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")
    else:
        st.info(f"📭 Aucune donnée disponible pour **{type_data}**. Veuillez d'abord scraper les données dans la section 🧹 *Scraper propre*.")



# Évaluation
elif menu == "📝 Évaluation":
    st.markdown("### 📝 Donnez votre avis via le formulaire externe")

    # Ajout de l'iframe du formulaire Kobo
    components.iframe("https://ee.kobotoolbox.org/i/ablbaafq", width=800, height=600)
        
        
