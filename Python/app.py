import os
from flask import Flask, render_template, request, url_for, redirect, session
from motif_generator import generer_motif

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = 'static/motifs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/generateur', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            nb_cotes = int(request.form['nb_cotes'])
            profondeur = int(request.form['répétition'])
            taille = int(request.form['taille'])
            angle = float(request.form['angle'])
            couleur = request.form['couleur']
            filename = generer_motif(nb_cotes, profondeur, taille, angle, couleur)
            session['image_path'] = url_for('static', filename=f'motifs/{filename}')
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('generateur.html', error=str(e))
    
    image_path = session.pop('image_path', None)
    return render_template('generateur.html', image_path=image_path)


@app.route('/a-propos')
def a_propos():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
