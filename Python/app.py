import os
import math
import random
from flask import Flask, render_template, request, url_for, redirect, session, flash
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
    # Contexte pour préremplissage
    context = {
        'nb_cotes':    '',
        'repetition':  '',
        'taille':      '',
        'angle':       '',
        'couleur':     '',
        'type_motif':  'polygon',
        'image_path':  None,
        'generated_filename': None,
        'error':       None
    }

    if request.method == 'POST':
        # Renommage
        if 'nom_fichier_existant' in request.form:
            ancien_nom = request.form['nom_fichier_existant']
            nouveau_nom = request.form['nom_nouveau'].strip()
            if ancien_nom and nouveau_nom:
                dossier = os.path.join('static', 'motifs')
                ancien_chemin = os.path.join(dossier, ancien_nom)
                nouveau_fichier = f"{nouveau_nom}.png"
                nouveau_chemin = os.path.join(dossier, nouveau_fichier)
                try:
                    os.rename(ancien_chemin, nouveau_chemin)
                    flash(f"Motif renommé en {nouveau_fichier}", 'success')
                except Exception as e:
                    flash(f"Erreur renommage: {e}", 'error')
                return redirect(url_for('generateur'))

        # Randomize sans JS
        if 'randomize' in request.form:
            context.update({
                'nb_cotes':   random.randint(3, 12),
                'repetition': random.randint(5, 60),
                'taille':     random.randint(20, 200),
                'angle':      round(random.uniform(5, 90), 2),
                'couleur':    "#{:06x}".format(random.randint(0, 0xFFFFFF)),
                'type_motif': random.choice(['polygon', 'spiral', 'fractale']),
            })
            return render_template('generateur.html', **context)

        # Génération de motif
        try:
            nb_cotes   = int(request.form['nb_cotes'])
            repetition = int(request.form['repetition'])
            taille     = int(request.form['taille'])
            angle      = float(request.form['angle'])
            couleur    = request.form['couleur']
            type_motif = request.form.get('type_motif', 'polygon')

            filename = generer_motif(nb_cotes, repetition, taille, angle, couleur, type_motif)
            context['image_path']         = url_for('static', filename=f'motifs/{filename}')
            context['generated_filename'] = filename
        except Exception as e:
            context['error'] = str(e)

    return render_template('generateur.html', **context)

@app.route('/historique')
def historique():
    chemin = os.path.join('static', 'motifs')
    fichiers = sorted(
        [f for f in os.listdir(chemin) if f.endswith('.png')],
        key=lambda x: os.path.getmtime(os.path.join(chemin, x)),
        reverse=True
    )
    return render_template('historique.html', fichiers=fichiers)

@app.route('/supprimer/<filename>', methods=['POST'])
def supprimer(filename):
    chemin = os.path.join('static', 'motifs', filename)
    if os.path.exists(chemin):
        os.remove(chemin)
    return redirect(url_for('historique'))

@app.route('/a-propos')
def a_propos():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
