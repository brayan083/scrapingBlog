import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Realizar la solicitud GET al sitio web
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página web
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar el contenedor principal que contiene el contenido del blog
        main_content = soup.find("article")

        # Si no se encuentra el contenedor principal, intentar buscar por otras etiquetas comunes
        if not main_content:
            main_content = soup.find("div", {"id": "content"})
        if not main_content:
            main_content = soup.find("div", {"class": "entry-content"})
        if not main_content:
            print("No se encontró el contenido principal en la página.")
            return None

        # Obtener todo el texto dentro del elemento <article>
        article_text = main_content.get_text(separator='\n', strip=True)

        return article_text
    else:
        # Si la solicitud no fue exitosa, imprimir un mensaje de error
        print("Error al obtener la página:", response.status_code)
        return None

# Ejemplo de uso
url = 'https://www.asisa.es/preguntas-frecuentes/preguntas/necesito-un-medico/salud-dental/56-que-servicios-bucodentales-incluye-mi-poliza-privada-de-salud-asisa'
texto_extraido = scrape_website(url)
print(texto_extraido)

