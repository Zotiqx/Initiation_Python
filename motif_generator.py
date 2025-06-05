import turtle
import os
import time
from datetime import datetime
from PIL import Image

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

    screen = turtle.Screen()
    screen.bgcolor("white")
    turtle_obj = turtle.Turtle()
    turtle_obj.hideturtle()
    turtle_obj.speed(0)
    turtle_obj.color(couleur)

    def dessiner_repetition(n):
        for _ in range(profondeur):
            for _ in range(n):
                turtle_obj.forward(taille)
                turtle_obj.right(360 / n)
            turtle_obj.right(angle)

    dessiner_repetition(nb_cotes)

    filename = f"motif_{datetime.now().strftime('%Y%m%d%H%M%S')}.eps"
    eps_path = os.path.join("static/motifs", filename)
    canvas = screen.getcanvas()
    canvas.postscript(file=eps_path)

    turtle_obj.clear()
    screen.bye()
    time.sleep(0.5)

    img = Image.open(eps_path)
    png_filename = filename.replace(".eps", ".png")
    img.save(os.path.join("static/motifs", png_filename))
    os.remove(eps_path)

    return png_filename
