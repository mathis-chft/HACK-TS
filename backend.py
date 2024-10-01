import os
import re
import tempfile
import time
import logging

from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import fitz  # PyMuPDF
import yake
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware  # Import du middleware CORS

# Configurez le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Définissez les origines autorisées
origins = [
    "http://localhost:3000",  # URL de votre frontend React
    # Ajoutez d'autres origines si nécessaire, par exemple votre domaine en production
]

# Ajoutez le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Liste des origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

# Constants
ALLOWED_URL_PREFIXES = [
    "https://www.linkedin.com/jobs/view/",
    # "https://fr.indeed.com/",  # Désactivé
    # "https://www.indeed.com/"   # Désactivé
]

# Fonctions Utilitaires

def extraire_mots_cles(text, N=400):
    """
    Extrait les mots-clés d'un texte en utilisant YAKE.
    """
    language = "fr"
    max_ngram_size = 2
    deduplication_threshold = 0.7
    deduplication_algo = "seqm"

    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        dedupFunc=deduplication_algo,
        windowsSize=1,
        top=N,
        features=None
    )

    keywords = custom_kw_extractor.extract_keywords(text)
    mots_cles = [kw for kw, score in keywords]
    return mots_cles

def sanitize_filename(filename):
    """
    Remplace les caractères invalides dans un nom de fichier par des tirets.
    """
    return re.sub(r'[\\/:"*?<>|]+', '-', filename)

def ajouter_mots_cles_et_titre_pdf(path_pdf, mots_cles, titre_poste, sortie_path):
    """
    Ajoute les mots-clés et le titre du poste au PDF.
    """
    try:
        doc = fitz.open(path_pdf)

        font_size = 8
        font_name = "helv"
        couleur = (0, 0, 0)

        total_pages = len(doc)
        total_mots = len(mots_cles)
        mots_par_page = total_mots // total_pages + 1

        for page_num in range(total_pages):
            page = doc[page_num]
            rect = page.rect

            x = 0
            y = 0

            start = page_num * mots_par_page
            end = start + mots_par_page
            mots_page = mots_cles[start:end]

            if not mots_page and page_num != 0:
                continue

            mots_par_ligne = 11
            lignes = []

            if page_num == 0 and titre_poste and titre_poste != "Titre du poste non trouvé":
                lignes.append(f"[{titre_poste}]")
                lignes.append("")

            if mots_page:
                mots_lignes = [" ".join(mots_page[i:i + mots_par_ligne]) for i in range(0, len(mots_page), mots_par_ligne)]
                lignes.extend(mots_lignes)

            ligne_spacing = font_size - 5

            for index, ligne in enumerate(lignes):
                if page_num == 0 and index == 0 and titre_poste and titre_poste != "Titre du poste non trouvé":
                    font_size_line = 16
                else:
                    font_size_line = font_size

                page.insert_text(
                    (x, y),
                    ligne,
                    fontname=font_name,
                    fontsize=font_size_line,
                    color=couleur,
                    overlay=False
                )
                y += ligne_spacing

        doc.save(sortie_path)
        doc.close()
        logger.info(f"✅ CV optimisé sauvegardé sous : {sortie_path}")

    except Exception as e:
        logger.error(f"❌ Une erreur est survenue lors de la modification du PDF : {e}")
        raise

def scraper_offre_linkedin(url, max_retries=5):
    """
    Scrape la description et le titre du poste depuis une offre LinkedIn.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    session = requests.Session()
    session.headers.update(headers)

    retries = 0
    backoff = 1  # Temps en secondes

    while retries < max_retries:
        try:
            response = session.get(url, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Trouver le div contenant la description de l'offre
                module_description = soup.find('div', class_='show-more-less-html__markup')

                if not module_description:
                    logger.warning("⚠️ Le module contenant la description de l'annonce n'a pas été trouvé.")
                    description = ""
                else:
                    # Extraire le texte de la description
                    description = module_description.get_text(separator='\n', strip=True)

                # Trouver le h1 contenant le titre du poste
                module_titre = soup.find('h1', class_='topcard__title')

                if not module_titre:
                    # Tenter de trouver le titre du poste via une autre méthode
                    h1 = soup.find('h1')
                    if h1:
                        titre_poste = h1.get_text(separator=' ', strip=True)
                        logger.info(f"Titre du poste trouvé : {titre_poste}")
                    else:
                        titre_poste = "Titre du poste non trouvé"
                        logger.warning("⚠️ Le titre du poste n'a pas été trouvé.")
                else:
                    titre_poste = module_titre.get_text(separator=' ', strip=True)
                    logger.info(f"Titre du poste trouvé : {titre_poste}")

                return description, titre_poste

            elif response.status_code == 429:
                logger.warning(f"⚠️ Trop de requêtes (429). Attente de {backoff} secondes avant de réessayer...")
                time.sleep(backoff)
                backoff *= 2  # Exponentiel
                retries += 1

            else:
                logger.error(f"❌ Erreur lors de la requête HTTP. Statut : {response.status_code}")
                return None, None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur lors de la requête HTTP : {e}")
            return None, None

    logger.error("❌ Nombre maximal de tentatives atteint. Impossible de récupérer le contenu de l'annonce.")
    return None, None

# API Models

class ProcessRequest(BaseModel):
    job_url: Optional[str] = None
    manual_description: Optional[str] = None
    manual_title: Optional[str] = None

# API Endpoints

@app.post("/process_cv/")
async def process_cv(
    file: UploadFile = File(...),
    job_url: Optional[str] = Form(None),
    manual_description: Optional[str] = Form(None),
    manual_title: Optional[str] = Form(None)
):
    try:
        # Sauvegarder le CV téléchargé dans un emplacement temporaire
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_cv:
            tmp_cv.write(contents)
            tmp_cv_path = tmp_cv.name
            logger.info(f"CV téléchargé et sauvegardé temporairement à {tmp_cv_path}")

        # Initialiser les variables
        description = ""
        titre_poste = ""

        # Déterminer le mode : automatique ou manuel
        if job_url:
            if not any(job_url.startswith(prefix) for prefix in ALLOWED_URL_PREFIXES):
                os.unlink(tmp_cv_path)
                logger.error("URL fournie non supportée.")
                raise HTTPException(status_code=400, detail="URL fournie non supportée. Utilisez LinkedIn.")

            if "linkedin.com/jobs/view/" in job_url:
                logger.info("Scraping de l'offre d'emploi LinkedIn.")
                description, titre_poste = scraper_offre_linkedin(job_url)

            # Puisque le scraping d'Indeed est désactivé, aucune condition pour "indeed.com/" ici

            if description is None and titre_poste is None:
                os.unlink(tmp_cv_path)
                logger.error("Impossible de récupérer le contenu de l'annonce.")
                raise HTTPException(status_code=500, detail="Impossible de récupérer le contenu de l'annonce.")

        elif manual_description and manual_title:
            description = manual_description
            titre_poste = manual_title
            logger.info("Mode manuel utilisé pour la description et le titre du poste.")
        else:
            os.unlink(tmp_cv_path)
            logger.error("Données insuffisantes fournies.")
            raise HTTPException(status_code=400, detail="Données insuffisantes fournies.")

        # Extraire les mots-clés
        if description:
            mots_cles = extraire_mots_cles(description, N=400)
            logger.info(f"{len(mots_cles)} mots-clés extraits.")
        else:
            mots_cles = []
            logger.warning("Aucune description fournie; aucun mot-clé extrait.")

        # Sanitiser le titre du poste
        if titre_poste and titre_poste != "Titre du poste non trouvé":
            titre_sanitized = sanitize_filename(titre_poste)
        else:
            titre_sanitized = "Titre_Poste"
            logger.warning("Titre du poste non trouvé; utilisation du titre par défaut.")

        # Définir le nom du fichier de sortie
        nom_fichier, extension = os.path.splitext(file.filename)
        sortie_nom = f"{nom_fichier} [{titre_sanitized}]{extension}"
        sortie_path = os.path.join(tempfile.gettempdir(), sortie_nom)
        logger.info(f"Nom du fichier optimisé : {sortie_nom}")

        # Ajouter les mots-clés et le titre au PDF
        try:
            ajouter_mots_cles_et_titre_pdf(tmp_cv_path, mots_cles, titre_poste, sortie_path)
        except Exception as e:
            os.unlink(tmp_cv_path)
            logger.error(f"Erreur lors de la modification du PDF: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        # Supprimer le CV temporaire original
        os.unlink(tmp_cv_path)
        logger.info(f"CV temporaire supprimé de {tmp_cv_path}")

        # Retourner le CV modifié comme fichier téléchargeable avec le nom correct
        headers = {
            'Content-Disposition': f'attachment; filename="{sortie_nom}"'
        }

        return FileResponse(
            path=sortie_path,
            media_type='application/pdf',
            headers=headers,
            filename=sortie_nom  # Ceci devrait suffire, mais ajouter explicitement les headers
        )
    except HTTPException as he:
        logger.error(f"HTTPException: {he.detail}")
        raise he
    except Exception as e:
        logger.exception("Une erreur inattendue est survenue lors du traitement du CV.")
        raise HTTPException(status_code=500, detail="Une erreur interne est survenue.")
