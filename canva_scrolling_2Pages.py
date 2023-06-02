import tkinter as tk
from tkinter import ttk

def change_page(direction):
    # Función para cambiar de página en el Canvas

    global current_page

    if direction == "forward":
        current_page = 1
    elif direction == "backward":
        current_page = 0

    # Borra todo el contenido actual en el Canvas
    canvas.delete("all")

    # Mostrar el contenido de la página actual en el Canvas
    for widget in pages[current_page]:
        canvas.create_window((0, 0), window=widget, anchor=tk.NW)

    # Configurar el Canvas para que se adapte al contenido
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Cambiar de Página")

# Crear el Frame
frame = ttk.Frame(ventana, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Crear el Canvas dentro del Frame con scrollbars
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Crear un Frame interior en el Canvas
interior_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=interior_frame, anchor=tk.NW)

# Contenido de las diferentes páginas
page1_widgets = [
    ttk.Label(interior_frame, text="Contenido de la Página 1"),
    ttk.Label(interior_frame, text="Texto adicional en la Página 1"),
    ttk.Label(interior_frame, text="Más texto en la Página 1"),
]

page2_widgets = [
    ttk.Label(interior_frame, text="Contenido de la Página 2"),
    ttk.Label(interior_frame, text="Texto adicional en la Página 2"),
    ttk.Label(interior_frame, text="Más texto en la Página 2"),
    ttk.Label(interior_frame, text="Incluso más texto en la Página 2"),
]

pages = [page1_widgets, page2_widgets]
current_page = 0

# Mostrar el contenido de la página actual en el Canvas
for widget in pages[current_page]:
    canvas.create_window((0, 0), window=widget, anchor=tk.NW)

# Crear los botones para cambiar de página
prev_button = ttk.Button(frame, text="Anterior", command=lambda: change_page("backward"))
prev_button.pack(side=tk.LEFT)

next_button = ttk.Button(frame, text="Siguiente", command=lambda: change_page("forward"))
next_button.pack(side=tk.LEFT)

# Configurar el Canvas para que se adapte al contenido
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
