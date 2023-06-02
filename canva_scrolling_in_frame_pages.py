import tkinter as tk
from tkinter import ttk


def change_page(page_num):
    # Función para cambiar de página en el Canvas

    # Borra todo el contenido actual en el Canvas
    canvas.delete("all")

    if page_num == 1:
        # Contenido de la primera página
        label1 = ttk.Label(canvas, text="Contenido 1")
        label1.pack()

        label2 = ttk.Label(canvas, text="Contenido 2")
        label2.pack()

        label3 = ttk.Label(canvas, text="Contenido 3")
        label3.pack()

    elif page_num == 2:
        # Contenido de la segunda página
        for i in range(20):
            label = ttk.Label(canvas, text=f"Contenido adicional {i+1}")
            label.pack()

    # Configurar el Canvas para que se adapte al contenido
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Crear la ventana principal
ventana = tk.Tk()

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

# Botones para cambiar de página
button_frame = ttk.Frame(ventana)
button_frame.pack(pady=10)

button1 = ttk.Button(button_frame, text="Página 1", command=lambda: change_page(1))
button1.grid(row=0, column=0, padx=10)

button2 = ttk.Button(button_frame, text="Página 2", command=lambda: change_page(2))
button2.grid(row=0, column=1, padx=10)

# Establecer la primera página como la página inicial
change_page(1)

# Ejecutar el bucle principal
ventana.mainloop()
