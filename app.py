from flask import Flask, render_template, request, send_file
from pytubefix import YouTube
import os

app = Flask(__name__)

# Directorio donde se almacenarán los archivos descargados
DOWNLOAD_FOLDER = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form.get("link")

    try:
        # Descargar el video de YouTube usando pytubefix
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()

        # Crear la carpeta de descargas si no existe
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)

        # Descargar el video al directorio
        file_path = ys.download(output_path=DOWNLOAD_FOLDER)

        # Devolver el archivo descargado como una descarga en el navegador
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Error al descargar el video: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
