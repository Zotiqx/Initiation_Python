import os
import math
import random
from flask import Flask, render_template, request, url_for, redirect, session, flash
from motif_generator import generer_motif

#Limites MAX
MAX_COTES               = 100
MAX_REPETITION          = 100
FRACTALE_MAX_REPETITION = 6
MAX_TAILLE              = 300
MAX_ANGLE               = 360

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = 'static/motifs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/generateur', methods=['GET', 'POST'])
def generateur():
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
        #Rennomage de fichier
        if 'nom_fichier_existant' in request.form:
            ancien = request.form['nom_fichier_existant']
            nouveau = request.form['nom_nouveau'].strip()
            if ancien and nouveau:
                dossier = os.path.join('static', 'motifs')
                try:
                    os.rename(os.path.join(dossier, ancien), os.path.join(dossier, f"{nouveau}.png"))
                    flash(f"Motif renommé en {nouveau}.png", 'success')
                except Exception as e:
                    flash(f"Erreur renommage: {e}", 'error')
            return redirect(url_for('generateur'))

        #Valeurs aléatoires
        if 'randomize' in request.form:
            context.update({
                'nb_cotes':   random.randint(1, MAX_COTES),
                'repetition': random.randint(1, MAX_REPETITION),
                'taille':     random.randint(1, MAX_TAILLE),
                'angle':      round(random.uniform(0, MAX_ANGLE), 2),
                'couleur':    "#{:06x}".format(random.randint(0, 0xFFFFFF)),
                'type_motif': random.choice(['polygon', 'spiral', 'fractale']),
            })
            return render_template('generateur.html', **context)

        #Récupère les informations saisies
        try:
            nb_cotes   = int(request.form['nb_cotes'])
            repetition = int(request.form['repetition'])
            taille     = int(request.form['taille'])
            angle      = float(request.form['angle'])
            couleur    = request.form['couleur']
            type_motif = request.form.get('type_motif', 'polygon')

            #Vérif des limites
            if not (1 <= nb_cotes <= MAX_COTES):
                context['error'] = f"Nombre de côtés doit être entre 1 et {MAX_COTES}."
            elif not (1 <= taille <= MAX_TAILLE):
                context['error'] = f"Taille doit être entre 1 et {MAX_TAILLE}."
            elif not (0 <= angle <= MAX_ANGLE):
                context['error'] = f"Angle doit être entre 0° et {MAX_ANGLE}°."
            else:
                if type_motif == 'fractale' and repetition > FRACTALE_MAX_REPETITION:
                    repetition = FRACTALE_MAX_REPETITION  #Bloquage a 6répétition pour le fractale
                if type_motif != 'fractale' and not (1 <= repetition <= MAX_REPETITION):
                    context['error'] = f"Répétitions doit être entre 1 et {MAX_REPETITION}."

            if context['error'] is None:
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
        reverse=True  #Affiche dans l'historique du plus récent au plus ancien
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