import os
import matplotlib.pyplot as plt
from datetime import datetime
import math

COULEURS_FR = {
    "rouge": "red",
    "bleu": "blue",
    "vert": "green",
    "jaune": "yellow",
    "noir": "black",
    "blanc": "white",
    "violet": "purple",
    "rose": "pink",
    "orange": "orange",
    "gris": "gray",
    "cyan": "cyan",
    "marron": "#8B4513",
}

def generer_motif(nb_cotes, profondeur, taille, angle, couleur):
    couleur = couleur.strip().lower()
    couleur = COULEURS_FR.get(couleur, couleur)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    x, y = 0, 0
    direction = 0  # angle en degrés

    points = []

    for _ in range(profondeur):
        for _ in range(nb_cotes):
            rad = math.radians(direction)
            new_x = x + taille * math.cos(rad)
            new_y = y + taille * math.sin(rad)
            points.append(((x, y), (new_x, new_y)))
            x, y = new_x, new_y
            direction += 360 / nb_cotes
        direction += angle

    for start, end in points:
        ax.plot([start[0], end[0]], [start[1], end[1]], color=couleur, linewidth=1)

    nom_fichier = f"motif_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    chemin = os.path.join("static/motifs", nom_fichier)
    plt.savefig(chemin, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close(fig)

    return nom_fichier
