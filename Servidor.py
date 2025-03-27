import ntplib
import socket
import time


def get_ip():
    return input("Digite o IP para o Servidor: ")


def get_port():
    while True:
        try:
            port = int(input("Digite a porta para o Servidor: "))
            if 1 <= port <= 65535:
                return port
            print("Porta inválida! Escolha entre 1 e 65535.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def get_ntp_time():
    return ntplib.NTPClient().request("gps.ntp.br", version=3).tx_time


def start(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip, port))
    server.settimeout(60)

    try:
        while True:
            # Recebendo solicitação dos clientes
            data, client_addr = server.recvfrom(1024)
            decoded_data = data.decode().strip()

            if decoded_data.lower() == "time":
                ntp_time = str(get_ntp_time()).encode()  # Correção aqui
                server.sendto(ntp_time, client_addr)
                print(f"Solicitação recebida de {client_addr}: {decoded_data}")
                print(f"Hora enviada: {ntp_time.decode()} para {client_addr}")
    except Exception as e:
        print(f"Falha no servidor: {e}")
    finally:
        server.close()


start(get_ip(), get_port())
