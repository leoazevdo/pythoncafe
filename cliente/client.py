import time
import requests
import subprocess

SERVIDOR_URL = "http://10.161.3.195:5000"  # Altere para IP do seu servidor
BLOQUEADO = False
PROCESSO = None

while True:
    try:
        resposta = requests.get(SERVIDOR_URL)
        dados = resposta.json()

        if dados['status'] == 'bloqueado' and not BLOQUEADO:
            print("Bloqueando máquina...")
            PROCESSO = subprocess.Popen(["xterm", "-fullscreen", "-e", "bash", "-c", "while true; do echo 'Máquina Bloqueada'; sleep 1; done"])
            BLOQUEADO = True

        elif dados['status'] == 'liberado' and BLOQUEADO:
            print("Liberando máquina...")
            subprocess.run(["pkill", "xterm"])
            BLOQUEADO = False

    except Exception as e:
        print("Erro ao conectar ao servidor:", e)

    time.sleep(5)
