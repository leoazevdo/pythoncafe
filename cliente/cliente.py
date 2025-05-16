from flask import Flask
import threading
import tkinter as tk
import subprocess
import os
import signal

app = Flask(__name__)
bloqueado = True
xtrlock_proc = None

def exibir_tela_bloqueio():
    def loop_bloqueio():
        global xtrlock_proc

        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        root.attributes('-topmost', True)
        root.protocol("WM_DELETE_WINDOW", lambda: None)

        label = tk.Label(root, text="🔒\n MÁQUINA BLOQUEADA", font=("Arial", 50), fg="white", bg="black")
        label.pack(expand=True)

        # Inicia xtrlock para bloquear teclado/mouse
        try:
            xtrlock_proc = subprocess.Popen(['xtrlock'])
        except Exception as e:
            print("Erro ao iniciar xtrlock:", e)

        def verificar_bloqueio():
            if not bloqueado:
                if xtrlock_proc:
                    xtrlock_proc.terminate()
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
