import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Éditeur d'Images avec Tkinter")
root.geometry("900x600")

# Variables globales
current_image = None  # Image actuellement chargée
original_image = None  # Copie de l'image originale

# Fonction pour charger une image
def upload_image():
    global current_image, original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if file_path:
        original_image = Image.open(file_path)
        current_image = original_image.copy()
        display_image(current_image)

# Fonction pour afficher l'image sur l'interface
def display_image(image):
    image.thumbnail((600, 400))  # Redimensionner pour l'affichage
    img_tk = ImageTk.PhotoImage(image)
    canvas.image = img_tk  # Empêche la suppression de l'objet image
    canvas.create_image(300, 200, image=img_tk)

# Fonction pour appliquer un filtre noir et blanc
def apply_black_white():
    global current_image
    if current_image:
        current_image = current_image.convert("L")
        display_image(current_image)

# Fonction pour ajuster la luminosité
def adjust_brightness(value):
    global current_image, original_image
    if original_image:
        enhancer = ImageEnhance.Brightness(original_image)
        current_image = enhancer.enhance(float(value))
        display_image(current_image)

# Fonction pour ajuster le contraste
def adjust_contrast(value):
    global current_image, original_image
    if original_image:
        enhancer = ImageEnhance.Contrast(original_image)
        current_image = enhancer.enhance(float(value))
        display_image(current_image)

# Fonction pour appliquer des filtres prédéfinis
def apply_filter(filter_type):
    global current_image
    if current_image:
        if filter_type == "BLUR":
            current_image = current_image.filter(ImageFilter.BLUR)
        elif filter_type == "CONTOUR":
            current_image = current_image.filter(ImageFilter.CONTOUR)
        elif filter_type == "DETAIL":
            current_image = current_image.filter(ImageFilter.DETAIL)
        elif filter_type == "EMBOSS":
            current_image = current_image.filter(ImageFilter.EMBOSS)
        elif filter_type == "SHARPEN":
            current_image = current_image.filter(ImageFilter.SHARPEN)
        display_image(current_image)

# Fonction pour sauvegarder l'image modifiée
def save_image():
    global current_image
    if current_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            current_image.save(file_path)

# Création des fenêtres secondaires pour l'upload et la correction
def open_upload_window():
    upload_window = tk.Toplevel(root)
    upload_window.title("Fenêtre d'Upload")
    upload_window.geometry("400x200")
    btn_upload = tk.Button(upload_window, text="Uploader Image", command=upload_image)
    btn_upload.pack(pady=20)

def open_correction_window():
    correction_window = tk.Toplevel(root)
    correction_window.title("Fenêtre de Correction")
    correction_window.geometry("400x400")

    # Boutons pour ajuster l'image
    btn_black_white = tk.Button(correction_window, text="Noir et Blanc", command=apply_black_white)
    btn_black_white.pack(pady=5)

    # Sliders pour ajuster la luminosité et le contraste
    brightness_slider = ttk.Scale(correction_window, from_=0.5, to=2.0, orient=tk.HORIZONTAL, command=adjust_brightness)
    brightness_slider.set(1.0)
    brightness_slider.pack(pady=5)
    tk.Label(correction_window, text="Luminosité").pack()

    contrast_slider = ttk.Scale(correction_window, from_=0.5, to=2.0, orient=tk.HORIZONTAL, command=adjust_contrast)
    contrast_slider.set(1.0)
    contrast_slider.pack(pady=5)
    tk.Label(correction_window, text="Contraste").pack()

    # Filtres prédéfinis
    filter_frame = tk.LabelFrame(correction_window, text="Filtres")
    filter_frame.pack(pady=10)
    filters = ["BLUR", "CONTOUR", "DETAIL", "EMBOSS", "SHARPEN"]
    for f in filters:
        btn = tk.Button(filter_frame, text=f, command=lambda ft=f: apply_filter(ft))
        btn.pack(pady=2)

# Création des widgets de l'interface principale
frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.LEFT, padx=10, pady=10)

# Boutons de commande pour ouvrir les fenêtres secondaires
btn_upload_window = tk.Button(frame_controls, text="Fenêtre Upload", command=open_upload_window)
btn_upload_window.pack(pady=5)

btn_correction_window = tk.Button(frame_controls, text="Fenêtre Correction", command=open_correction_window)
btn_correction_window.pack(pady=5)

# Bouton pour sauvegarder l'image modifiée
btn_save = tk.Button(frame_controls, text="Sauver Image", command=save_image)
btn_save.pack(pady=5)

# Zone d'affichage de l'image
canvas = tk.Canvas(root, width=600, height=400, bg="gray")
canvas.pack(side=tk.RIGHT, padx=10, pady=10)

# Boucle principale
root.mainloop()
