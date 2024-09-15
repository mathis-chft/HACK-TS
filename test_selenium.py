from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Options pour exécuter Chrome en mode headless (sans interface graphique)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Facultatif, supprimez cette ligne si vous voulez voir le navigateur

# Chemin vers chromedriver (si nécessaire)
# Remplacez 'path/to/chromedriver' par le chemin réel si chromedriver n'est pas dans le PATH
driver = webdriver.Chrome(options=chrome_options)  # Ou webdriver.Chrome(executable_path='path/to/chromedriver', options=chrome_options)

try:
    driver.get('https://www.google.com')
    print("Titre de la page :", driver.title)
finally:
    driver.quit()
