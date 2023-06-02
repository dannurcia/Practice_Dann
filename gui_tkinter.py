import tkinter as tk
from tkinter import ttk

# Creacion de la ventana de aplicación a través del objeto tk.Tk
root = tk.Tk()
# Creacion del frame contenedor
container = ttk.Frame(root)
# Creacion del canvas (lienzo)
canvas = tk.Canvas(container)
# Barra de desplazamiento (scrollbar)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
# Frame que se convertirá en scrollbar frame
scrollable_frame = ttk.Frame(canvas)

# Función  que se llamará cada vez que cambie el contenido del frame desplazable
# y que le dirá al canvas qué tan grande será el frame para que sepa cuanto se va a desplazar
scrollable_frame.bind(
    '<Configure>',
    lambda e: canvas.configure(
        scrollregion=canvas.bbox('all')
    )
)

# Diciendole al canvas que dibuje su interior actual
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
# Configurando el canvas para que se desplace cuando su posicion Y cambie
canvas.configure(yscrollcommand=scrollbar.set)


for i in range(50):
    ttk.Label(scrollable_frame, text='Muestra de etiqueta desplazable').pack()

container.pack()
canvas.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

root.mainloop()





