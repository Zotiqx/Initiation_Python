import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

#Couleurs en francais
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
    #Convertit la couleur si elle est rentré en francais
    c = couleur.strip().lower()
    couleur = COULEURS_FR.get(c, c)

    #crée la figure
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

        for (x1, y1), (x2, y2) in segments:
            ax.plot([x1, x2], [y1, y2], color=couleur)

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

        for (x1, y1), (x2, y2) in segments:
            ax.plot([x1, x2], [y1, y2], color=couleur)

    def draw_fractale():
        #Récursivité pour les séquences du fractale
        def fractale_seq(length, depth):
            if depth == 0:
                return [(length, 0)]
            seq = []
            seq += fractale_seq(length/3, depth-1)
            seq.append((0, 60))
            seq += fractale_seq(length/3, depth-1)
            seq.append((0, -120))
            seq += fractale_seq(length/3, depth-1)
            seq.append((0, 60))
            seq += fractale_seq(length/3, depth-1)
            return seq

        segments = []
        x, y, dir_deg = 0, 0, 0

        #On fait 3cotés pour fermer la figure
        for _ in range(3):
            for length, turn in fractale_seq(taille, profondeur):
                rad = math.radians(dir_deg)
                nx = x + length * math.cos(rad)
                ny = y + length * math.sin(rad)
                segments.append(((x, y), (nx, ny)))
                x, y = nx, ny
                dir_deg += turn
            dir_deg += 120

        for (x1, y1), (x2, y2) in segments:
            ax.plot([x1, x2], [y1, y2], color=couleur)

    #appelle la fonction du type choisi
    if type_motif == "spiral":
        draw_spiral()
    elif type_motif == "fractale":
        draw_fractale()
    else:
        draw_polygon()

    nom = f"{type_motif}_{datetime.now():%Y%m%d%H%M%S}.png" #nom motif+date
    chemin = os.path.join("static/motifs", nom)
    plt.savefig(chemin, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close(fig)
    return nom