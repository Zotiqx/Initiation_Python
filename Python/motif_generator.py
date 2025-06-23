import os
import math
import matplotlib.pyplot as plt
from datetime import datetime

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

def generer_motif(nb_cotes, profondeur, taille, angle, couleur, type_motif="polygon"):
    c = couleur.strip().lower()
    couleur = COULEURS_FR.get(c, c)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    def draw_polygon():
        x, y, dir_deg = 0, 0, 0
        segments = []
        for _ in range(profondeur):
            for _ in range(nb_cotes):
                rad = math.radians(dir_deg)
                nx = x + taille * math.cos(rad)
                ny = y + taille * math.sin(rad)
                segments.append(((x, y), (nx, ny)))
                x, y = nx, ny
                dir_deg += 360 / nb_cotes
            dir_deg += angle
        for (x1,y1),(x2,y2) in segments:
            ax.plot([x1,x2],[y1,y2], color=couleur)


    def draw_spiral():
        x, y, dir_deg = 0, 0, 0
        length = taille
        segments = []
        inc = taille / max(1, profondeur)
        for _ in range(profondeur):
            rad = math.radians(dir_deg)
            nx = x + length * math.cos(rad)
            ny = y + length * math.sin(rad)
            segments.append(((x, y), (nx, ny)))
            x, y = nx, ny
            dir_deg += angle
            length += inc
        for (x1,y1),(x2,y2) in segments:
            ax.plot([x1,x2],[y1,y2], color=couleur)

    if type_motif == "spiral":
        draw_spiral()
    else:
        draw_polygon()

    nom = f"{type_motif}_{datetime.now():%Y%m%d%H%M%S}.png"
    chemin = os.path.join("static/motifs", nom)
    plt.savefig(chemin, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close(fig)
    return nom
