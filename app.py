import os
from flask import Flask, render_template, request, url_for, redirect
from motif_generator import generer_motif

app = Flask(__name__)
UPLOAD_FOLDER = 'static/motifs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_path = None
    if request.method == 'POST':
        try:
            nb_cotes = int(request.form['nb_cotes'])
            profondeur = int(request.form['profondeur'])
            taille = int(request.form['taille'])
            angle = float(request.form['angle'])
            couleur = request.form['couleur']
            filename = generer_motif(nb_cotes, profondeur, taille, angle, couleur)
            image_path = url_for('static', filename=f'motifs/{filename}')
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html', image_path=image_path)

@app.route('/a-propos')
def a_propos():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)


