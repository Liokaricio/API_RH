import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil

def iniciar_api():
    global proceso_api
    if not obtener_pid():
        proceso_api = subprocess.Popen(['python', 'api.py'])
        mensaje_estado("API iniciada")
    else:
        mensaje_estado("La API ya está en ejecución")

def detener_api():
    pid = obtener_pid()
    if pid:
        proceso = psutil.Process(pid)
        proceso.terminate()
        mensaje_estado("API detenida")
    else:
        mensaje_estado("La API no está en ejecución")

def obtener_pid():
    for proceso in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proceso.info['cmdline'] and 'api.py' in proceso.info['cmdline']:
            return proceso.info['pid']
    return None

def mensaje_estado(mensaje):
    estado_label.config(text=mensaje)
    messagebox.showinfo("Estado", mensaje)

# Crear ventana
root = tk.Tk()
root.title("Control de API Flask")
root.geometry("300x200")

# Botones
btn_iniciar = tk.Button(root, text="Iniciar API", command=iniciar_api)
btn_iniciar.pack(pady=10)

btn_detener = tk.Button(root, text="Detener API", command=detener_api)
btn_detener.pack(pady=10)

# Estado
estado_label = tk.Label(root, text="API no iniciada", fg="red")
estado_label.pack(pady=10)

root.mainloop()
