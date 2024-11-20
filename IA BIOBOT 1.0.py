import cv2
import numpy as np
import imutils
from tkinter import *
from PIL import Image, ImageTk


# Detectar objetos pequeños simulando residuos
def detect_small_objects(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Residuo", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame


# Función para mostrar la imagen de prueba en lugar del video
def show_example_image():
    example_img = cv2.imread("setUp/setUp_prueba.png")
    if example_img is None:
        print("Error: La imagen de prueba no se pudo cargar.")
        return None

    example_img_resized = cv2.resize(example_img, (640, 480))
    example_img_rgb = cv2.cvtColor(example_img_resized, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(image=Image.fromarray(example_img_rgb))
    return img


# Función para mostrar solo la imagen izquierda en el apartado PRUEBA
def display_example_image_left():
    example_img_left = cv2.imread("setUp/setUp_pruebaleft.png")

    if example_img_left is None:
        print("Error: La imagen izquierda de prueba no se pudo cargar.")
        return

    # Redimensionar y convertir la imagen
    example_img_left_resized = cv2.resize(example_img_left, (250, 250))
    img_left = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(example_img_left_resized, cv2.COLOR_BGR2RGB)))

    # Mostrar la imagen en la etiqueta correspondiente
    lblimg.configure(image=img_left)
    lblimg.image = img_left


# Función para actualizar las imágenes según el tipo de basura seleccionado
def update_images():
    waste_type = waste_type_var.get()
    if waste_type == 'METAL':
        images(img_metal, img_metaltxt)
    elif waste_type == 'VIDRIO':
        images(img_glass, img_glasstxt)
    elif waste_type == 'PLÁSTICO':
        images(img_plastic, img_plastictxt)
    elif waste_type == 'CARTÓN':
        images(img_carton, img_cartontxt)
    elif waste_type == 'MÉDICO':
        images(img_medical, img_medicaltxt)
    elif waste_type == 'ORGÁNICA':
        images(img_organica, img_organicatxt)
    elif waste_type == 'PRUEBA':
        display_example_image_left()


# Función para mostrar las imágenes
def images(img, imgtxt):
    img = ImageTk.PhotoImage(image=Image.fromarray(img))
    lblimg.configure(image=img)
    lblimg.image = img

    img_txt = ImageTk.PhotoImage(image=Image.fromarray(imgtxt))
    lblimgtxt.configure(image=img_txt)
    lblimgtxt.image = img_txt


# Función para mostrar la imagen de prueba y detener la cámara
def display_example_image():
    global cap
    if cap is not None:
        cap.release()  # Detener la cámara
        cap = None
    example_img = show_example_image()
    if example_img:
        lblVideo.configure(image=example_img)
        lblVideo.image = example_img


# Función para procesar el video
def Scanning():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            frame = detect_small_objects(frame)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))

            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Scanning)


# Función principal
def ventana_principal():
    global cap, lblVideo, img_metal, img_glass, img_plastic, img_carton, img_medical, img_organica
    global img_metaltxt, img_glasstxt, img_plastictxt, img_cartontxt, img_medicaltxt, img_organicatxt
    global lblimg, lblimgtxt, pantalla, waste_type_var

    # Ventana principal
    pantalla = Tk()
    pantalla.title("IA BIOBOT")
    pantalla.geometry("1280x720")

    # Fondo
    imagenF = PhotoImage(file="setUp/setUp_Canva.png")
    background = Label(image=imagenF)
    background.place(x=0, y=0, relwidth=1, relheight=1)

    # Cargar imágenes para cada tipo de basura
    img_metal = cv2.imread("setUp/setUp_metal.png")
    img_glass = cv2.imread("setUp/setUp_vidrio.png")
    img_plastic = cv2.imread("setUp/setUp_plastico.png")
    img_carton = cv2.imread("setUp/setUp_carton.png")
    img_medical = cv2.imread("setUp/setUp_medical.png")
    img_organica = cv2.imread("setUp/setUp_organica.png")
    img_metaltxt = cv2.imread("setUp/setUp_metaltxt.png")
    img_glasstxt = cv2.imread("setUp/setUp_vidriotxt.png")
    img_plastictxt = cv2.imread("setUp/setUp_plasticotxt.png")
    img_cartontxt = cv2.imread("setUp/setUp_cartontxt.png")
    img_medicaltxt = cv2.imread("setUp/setUp_medicaltxt.png")
    img_organicatxt = cv2.imread("setUp/setUp_organicatxt.png")

    # Etiqueta de video
    lblVideo = Label(pantalla)
    lblVideo.place(x=320, y=180)

    # Etiquetas para las imágenes de basura
    lblimg = Label(pantalla)
    lblimg.place(x=75, y=260)

    lblimgtxt = Label(pantalla)
    lblimgtxt.place(x=995, y=310)

    # Desplegable para seleccionar tipo de basura
    waste_type_var = StringVar(value='TIPOS DE BASURA')
    waste_options = ["METAL", "VIDRIO", "PLÁSTICO", "CARTÓN", "MÉDICO", "ORGÁNICA", "PRUEBA"]
    waste_dropdown = OptionMenu(pantalla, waste_type_var, *waste_options, command=lambda _: on_waste_selection())
    waste_dropdown.place(x=100, y=200)

    # Iniciar captura de video
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    Scanning()

    # Ejecutar la ventana principal
    pantalla.mainloop()


# Función para manejar la selección del tipo de basura
def on_waste_selection():
    waste_type = waste_type_var.get()
    if waste_type == "PRUEBA":
        display_example_image()
        display_example_image_left()  # Mostrar solo la imagen izquierda de prueba
    else:
        if cap is None:  # Reactivar la cámara si estaba desactivada
            start_camera()
        update_images()


# Función para reiniciar la cámara cuando se elige una opción diferente de "PRUEBA"
def start_camera():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    Scanning()


# Inicializar la cámara
cap = None

ventana_principal()
