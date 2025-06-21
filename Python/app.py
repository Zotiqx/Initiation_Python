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
def generateur():
    if request.method == 'POST':
        if 'nom_fichier_existant' in request.form:
            ancien_nom = request.form['nom_fichier_existant']
            nouveau_nom = request.form['nom_nouveau'].strip()
            if ancien_nom and nouveau_nom:
                dossier = os.path.join('static', 'motifs')
                ancien_chemin = os.path.join(dossier, ancien_nom)
                nouveau_fichier = f"{nouveau_nom}.png"
                nouveau_chemin = os.path.join(dossier, nouveau_fichier)
                if os.path.exists(ancien_chemin):
                    os.rename(ancien_chemin, nouveau_chemin)
                    session['image_path'] = url_for('static', filename=f'motifs/{nouveau_fichier}')
                    session['generated_filename'] = nouveau_fichier
                    return redirect(url_for('generateur'))
        else:
            try:
                nb_cotes = int(request.form['nb_cotes'])
                profondeur = int(request.form['répétition'])
                taille = int(request.form['taille'])
                angle = float(request.form['angle'])
                couleur = request.form['couleur']
                filename = generer_motif(nb_cotes, profondeur, taille, angle, couleur)
                session['image_path'] = url_for('static', filename=f'motifs/{filename}')
                session['generated_filename'] = filename
                return redirect(url_for('generateur'))
            
            except Exception as e:
                return render_template('generateur.html', error=str(e))

    image_path = session.pop('image_path', None)
    generated_filename = session.pop('generated_filename', None)
    return render_template('generateur.html', image_path=image_path, generated_filename=generated_filename)

@app.route('/historique')
def historique():
    chemin = os.path.join('static', 'motifs')
    fichiers = sorted(
        [f for f in os.listdir(chemin) if f.endswith('.png')],
        key=lambda x: os.path.getmtime(os.path.join(chemin, x)),
        reverse=True
    )
    return render_template('historique.html', fichiers=fichiers)


@app.route('/a-propos')
def a_propos():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
