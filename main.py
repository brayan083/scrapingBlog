from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_website(url):
    try:
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
                return "No se encontró el contenido principal en la página."

            # Obtener todo el texto dentro del elemento <article>
            article_text = main_content.get_text(separator='\n', strip=True)
            print(article_text)
            return article_text
        else:
            # Si la solicitud no fue exitosa, imprimir un mensaje de error
            return f"Error al obtener la página: {response.status_code}"
    except Exception as e:
        return f"Error al procesar la URL: {str(e)}"

# Definir una ruta para tu API
@app.route('/scrape', methods=['POST'])
def scrape():
    # Obtener la URL de la solicitud POST
    url = request.args.get('url')
    print(url)

    # Llamar a la función scrape_website con la URL
    result = scrape_website(url)

    # Devolver el resultado como JSON
    return jsonify({'texto_extraido': result}, 201)

@app.route('/hello/<name>')
def name(name):
    print(name)
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)
    

