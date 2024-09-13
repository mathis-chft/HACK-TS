"""
                                                                       
@@@  @@@   @@@@@@    @@@@@@@  @@@  @@@  @@@@@@@   @@@@@@   
@@@  @@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@  @@@@@@@   
@@!  @@@  @@!  @@@  !@@       @@!  !@@    @@!    !@@       
!@!  @!@  !@!  @!@  !@!       !@!  @!!    !@!    !@!       
@!@!@!@!  @!@!@!@!  !@!       @!@@!@!     @!!    !!@@!!    
!!!@!!!!  !!!@!!!!  !!!       !!@!!!      !!!     !!@!!!   
!!:  !!!  !!:  !!!  :!!       !!: :!!     !!:         !:!  
:!:  !:!  :!:  !:!  :!:       :!:  !:!    :!:        !:!   
::   :::  ::   :::   ::: :::   ::  :::     ::    :::: ::   
 :   : :   :   : :   :: :: :   :   :::     :     :: : :    
                                                                       
"""

import fitz  # PyMuPDF
import yake
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import re
import time
import argparse
import tempfile
import subprocess
import sys

# Initialiser colorama
init(autoreset=True)

# Définir le nom du fichier CV ici
NOM_CV = "CV - Mathis CHOUFFOT.pdf"

def extraire_mots_cles(text, N=200):
    """
    Extrait les N mots-clés les plus pertinents du texte donné en utilisant YAKE!.
    """
    language = "fr"  # Langue du texte
    max_ngram_size = 2
    deduplication_threshold = 0.95
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
    Supprime ou remplace les caractères invalides dans un nom de fichier.
    """
    # Remplacer les caractères invalides par un tiret
    return re.sub(r'[\\/:"*?<>|]+', '-', filename)

def ajouter_mots_cles_et_titre_pdf(path_pdf, mots_cles, titre_poste, sortie_path):
    """
    Ajoute les mots-clés au PDF sans modifier le contenu existant.
    Les mots-clés sont répartis discrètement sur les pages existantes.
    Ajoute également le titre du poste à la fin des mots-clés sur la dernière page.
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

            if not mots_page:
                continue

            mots_par_ligne = 15
            lignes = [" ".join(mots_page[i:i + mots_par_ligne]) for i in range(0, len(mots_page), mots_par_ligne)]
            ligne_spacing = font_size - 5

            for ligne in lignes:
                page.insert_text(
                    (x, y),
                    ligne,
                    fontname=font_name,
                    fontsize=font_size,
                    color=couleur,
                    overlay=False
                )
                y += ligne_spacing

        # # Insérer le titre du poste à la fin des mots-clés sur la dernière page
        # if titre_poste and titre_poste != "Titre du poste non trouvé":
        #     derniere_page = doc[-1]
        #     rect = derniere_page.rect

        #     # Définir les propriétés du texte du titre
        #     titre_font_size = 16  # Taille de police plus grande pour le titre
        #     titre_font_name = "helv"
        #     titre_couleur = (0, 0, 0)  # Noir en RGB

        #     # Définir la position pour le titre du poste (par exemple, après les mots-clés)
        #     # Vous pouvez ajuster 'y_position' selon vos besoins
        #     y_position = rect.height  # Ajustez cette valeur si nécessaire

        #     derniere_page.insert_text(
        #         (50, y_position),
        #         titre_poste,
        #         fontname=titre_font_name,
        #         fontsize=titre_font_size,
        #         color=titre_couleur,
        #         overlay=False
        #     )

        # Sauvegarder le document modifié
        doc.save(sortie_path)
        doc.close()
        print(Fore.GREEN + f"\n✅ CV optimisé sauvegardé sous : {sortie_path}\n")

    except Exception as e:
        print(Fore.RED + f"\n❌ Une erreur est survenue lors de la modification du PDF : {e}\n")

def scraper_offre_linkedin(url, max_retries=5):
    """
    Scrape la description de l'offre d'emploi et l'intitulé du poste depuis LinkedIn à partir de l'URL fournie.
    Gère les erreurs 429 avec des retraits exponentiels.
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
                    print(Fore.YELLOW + "⚠️ Le module contenant la description de l'annonce n'a pas été trouvé.\n")
                    description = ""
                else:
                    # Extraire le texte de la description
                    description = module_description.get_text(separator='\n', strip=True)

                # Trouver le div contenant le titre du poste
                module_titre = soup.find('div', class_='t-24 job-details-jobs-unified-top-card__job-title')

                if not module_titre:
                    # Tenter de trouver le titre du poste via une autre méthode
                    h1 = soup.find('h1')
                    if h1:
                        titre_poste = h1.get_text(separator=' ', strip=True)
                        print(Fore.CYAN + f"Titre du poste trouvé : {titre_poste}\n")
                    else:
                        titre_poste = "Titre du poste non trouvé"
                        print(Fore.YELLOW + "⚠️ Le titre du poste n'a pas été trouvé.\n")
                else:
                    h1 = module_titre.find('h1')
                    if not h1:
                        print(Fore.YELLOW + "⚠️ Le titre du poste n'a pas été trouvé dans le div.\n")
                        titre_poste = "Titre du poste non trouvé"
                    else:
                        titre_poste = h1.get_text(separator=' ', strip=True)
                        print(Fore.CYAN + f"Titre du poste trouvé : {titre_poste}\n")

                return description, titre_poste

            elif response.status_code == 429:
                print(Fore.YELLOW + f"⚠️ Trop de requêtes (429). Attente de {backoff} secondes avant de réessayer..." + Style.RESET_ALL)
                time.sleep(backoff)
                backoff *= 2  # Exponentiel
                retries += 1

            else:
                print(Fore.RED + f"\n❌ Erreur lors de la requête HTTP. Statut : {response.status_code}\n")
                return None, None

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"\n❌ Erreur lors de la requête HTTP : {e}\n")
            return None, None

    print(Fore.RED + "\n❌ Nombre maximal de tentatives atteint. Impossible de récupérer le contenu de l'annonce.\n")
    return None, None

def scraper_manuel():
    """
    Offre à l'utilisateur le choix entre deux méthodes pour saisir la description de l'annonce :
    1. Saisie directe via le terminal (Ctrl+D pour terminer)
    2. Utilisation d'un éditeur de texte temporaire
    Demande ensuite le titre du poste.
    """
    print(Fore.BLUE + "\n📝 Mode Manuel Activé.\n" + Style.RESET_ALL)
    
    # Choisir la méthode de saisie
    print(Fore.CYAN + "🔍 Choisissez la méthode de saisie de la description de l'annonce :" + Style.RESET_ALL)
    print(Fore.CYAN + "1. Saisie directe (pressez Ctrl+D pour terminer)" + Style.RESET_ALL)
    print(Fore.CYAN + "2. Utiliser un éditeur de texte temporaire" + Style.RESET_ALL)
    
    choix = input(Fore.CYAN + "🔗 Entrez 1 ou 2 : " + Style.RESET_ALL).strip()
    
    if choix == '1':
        # Méthode 1 : Saisie directe via sys.stdin.read()
        print(Fore.CYAN + "\n🔍 Entrez la description de l'annonce. Pressez Ctrl+D (EOF) sur une nouvelle ligne pour terminer la saisie :" + Style.RESET_ALL)
        try:
            description = sys.stdin.read()
        except KeyboardInterrupt:
            print(Fore.RED + "\n❌ Saisie interrompue par l'utilisateur.\n")
            sys.exit(1)
    elif choix == '2':
        # Méthode 2 : Utiliser un éditeur de texte temporaire
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmpfile:
                tmpfile_path = tmpfile.name
                print(Fore.CYAN + "🔍 L'éditeur de texte s'ouvre maintenant. Écrivez ou collez la description de l'annonce, puis sauvegardez et fermez l'éditeur." + Style.RESET_ALL)
                subprocess.call(['nano', tmpfile_path])  # Remplacez 'nano' par votre éditeur préféré si nécessaire
                tmpfile.seek(0)
                description = tmpfile.read()
        except KeyboardInterrupt:
            print(Fore.RED + "\n❌ Saisie interrompue par l'utilisateur.\n")
            sys.exit(1)
        finally:
            # Supprimer le fichier temporaire si il existe
            if os.path.exists(tmpfile_path):
                os.unlink(tmpfile_path)
    else:
        print(Fore.RED + "\n❌ Choix invalide. Veuillez exécuter à nouveau le script et choisir 1 ou 2.\n")
        sys.exit(1)
    
    # Demander à l'utilisateur d'entrer le titre de l'annonce
    try:
        titre_poste = input(Fore.CYAN + "🔍 Entrez le titre du poste : " + Style.RESET_ALL).strip()
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Saisie interrompue par l'utilisateur.\n")
        sys.exit(1)
    
    return description, titre_poste

def main():
    # Configuration de argparse pour gérer les arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Optimisation de votre CV avec les Mots-Clés LinkedIn ou Mode Manuel.")
    parser.add_argument('-m', '--manuel', action='store_true', help='Mode manuel : fournir la description et le titre de l\'annonce manuellement.')
    args = parser.parse_args()

    # Afficher l'art ASCII
    print(Fore.YELLOW + """
@@@  @@@   @@@@@@    @@@@@@@  @@@  @@@  @@@@@@@   @@@@@@   
@@@  @@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@  @@@@@@@   
@@!  @@@  @@!  @@@  !@@       @@!  !@@    @@!    !@@       
!@!  @!@  !@!  @!@  !@!       !@!  @!!    !@!    !@!       
@!@!@!@!  @!@!@!@!  !@!       @!@@!@!     @!!    !!@@!!    
!!!@!!!!  !!!@!!!!  !!!       !!@!!!      !!!     !!@!!!   
!!:  !!!  !!:  !!!  :!!       !!: :!!     !!:         !:!  
:!:  !:!  :!:  !:!  :!:       :!:  !:!    :!:        !:!   
::   :::  ::   :::   ::: :::   ::  :::     ::    :::: ::   
 :   : :   :   : :   :: :: :   :   :::     :     :: : :    
""" + Style.RESET_ALL)

    print(Fore.BLUE + Style.BRIGHT + "\n=== Optimisation de votre CV avec les Mots-Clés LinkedIn ===\n" + Style.RESET_ALL)
    
    try:
        # Définir le chemin du CV à la racine du dossier contenant le script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path_pdf = os.path.join(script_dir, NOM_CV)
        
        if not os.path.isfile(path_pdf):
            print(Fore.RED + f"\n❌ Le fichier CV '{NOM_CV}' n'a pas été trouvé dans le répertoire {script_dir}.\n")
            return

        # Déterminer le mode d'exécution
        if args.manuel:
            # Mode Manuel
            description, titre_poste = scraper_manuel()
        else:
            # Mode Automatique (LinkedIn)
            # Demander à l'utilisateur d'entrer l'URL de l'annonce LinkedIn
            url_annonce = input(Fore.CYAN + "🔗 Entrez l'URL de l'annonce LinkedIn : " + Style.RESET_ALL).strip()

            if not url_annonce.startswith("https://www.linkedin.com/jobs/view/"):
                print(Fore.RED + "\n❌ L'URL fournie ne semble pas être une URL d'annonce LinkedIn valide.\n")
                return

            print(Fore.BLUE + "\n🔍 Scraping de l'annonce LinkedIn..." + Style.RESET_ALL)
            description, titre_poste = scraper_offre_linkedin(url_annonce)

            if description is None and titre_poste is None:
                print(Fore.RED + "❌ Impossible de récupérer le contenu de l'annonce.\n")
                return

        # Extraire les mots-clés de la description
        if description:
            mots_cles = extraire_mots_cles(description, N=200)
            print(Fore.GREEN + f"✅ Mots-clés extraits ({len(mots_cles)}): {', '.join(mots_cles[:20])}...\n" + Style.RESET_ALL)
        else:
            mots_cles = []
            print(Fore.YELLOW + "⚠️ Aucun mot-clé extrait car la description est vide.\n" + Style.RESET_ALL)

        # Vérifier si le titre du poste a été trouvé
        if titre_poste and titre_poste != "Titre du poste non trouvé":
            print(Fore.GREEN + f"✅ Titre du poste extrait : {titre_poste}\n" + Style.RESET_ALL)
        else:
            titre_poste = "Titre du poste non trouvé"
            print(Fore.YELLOW + "⚠️ Aucun titre de poste trouvé.\n" + Style.RESET_ALL)

        # Définir le chemin de sortie avec le titre du poste
        if titre_poste != "Titre du poste non trouvé":
            titre_sanitized = sanitize_filename(titre_poste)
        else:
            titre_sanitized = "Titre_Poste"

        nom_fichier, extension = os.path.splitext(NOM_CV)
        sortie_nom = f"[{nom_fichier}] [{titre_sanitized}]{extension}"
        sortie_path = os.path.join(script_dir, sortie_nom)

        # Ajouter les mots-clés et le titre du poste au PDF
        ajouter_mots_cles_et_titre_pdf(path_pdf, mots_cles, titre_poste, sortie_path)

        print(Fore.BLUE + "🎉 Processus terminé avec succès !" + Style.RESET_ALL + "\n")

    except KeyboardInterrupt:
        print(Fore.RED + "\n\n❌ Processus interrompu par l'utilisateur (Ctrl+C).\n" + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    main()
