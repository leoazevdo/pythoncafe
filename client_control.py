import requests

def bloquear_maquina(ip):
    try:
        requests.get(f'http://{ip}:8080/bloquear', timeout=2)
    except:
        pass

def liberar_maquina(ip):
    try:
        requests.get(f'http://{ip}:8080/liberar', timeout=2)
    except:
        pass
