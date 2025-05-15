from flask import Flask, render_template_string
import threading
import tkinter as tk
import os

app = Flask(__name__)
bloqueado = True

def exibir_tela_bloqueio():
    def loop_bloqueio():
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        root.attributes('-topmost', True)

        label = tk.Label(root, text="🔒\n MÁQUINA BLOQUEADA", font=("Arial", 50), fg="white", bg="black")
        label.pack(expand=True)

        def verificar_bloqueio():
            if not bloqueado:
                root.destroy()
            else:
                root.after(1000, verificar_bloqueio)

        root.after(1000, verificar_bloqueio)
        root.mainloop()

    threading.Thread(target=loop_bloqueio).start()

@app.route('/bloquear')
def bloquear():
    global bloqueado
    bloqueado = True
    exibir_tela_bloqueio()
    return "Bloqueio ativado"

@app.route('/liberar')
def liberar():
    global bloqueado
    bloqueado = False
    return "Máquina liberada"

def iniciar_servidor():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=iniciar_servidor).start()
    exibir_tela_bloqueio()
