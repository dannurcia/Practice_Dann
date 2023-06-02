import tkinter as tk
from tkinter import ttk

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

# Agregar widgets al Frame interior
label1 = ttk.Label(interior_frame, text="Contenido 1")
label1.pack()

label2 = ttk.Label(interior_frame, text="Contenido 2")
label2.pack()

label3 = ttk.Label(interior_frame, text="Contenido 3")
label3.pack()

# Agregar más contenido para que sea necesario el desplazamiento vertical
for i in range(20):
    label = ttk.Label(interior_frame, text=f"Contenido adicional {i+1}")
    label.pack()

# Configurar el Canvas para que se adapte al contenido
interior_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Ejecutar el bucle principal
ventana.mainloop()
