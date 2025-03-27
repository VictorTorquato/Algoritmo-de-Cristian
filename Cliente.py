import socket
import time
import datetime

def float_to_hms(seconds):
    tempo = datetime.timedelta(seconds=seconds)
    return str(tempo).split(", ")[-1].split(".")[0]

def decreases_two_seconds(timestamp: float) -> float:
    time.sleep(1)
    return max(0, timestamp - 2) 

def increase_two_seconds(timestamp: float) -> float:
    time.sleep(1)
    return timestamp + 2

def get_ip():
    return input("Digite o IP para o Servidor de tempo: ")


def get_port():
    while True:
        try:
            port = int(input("Digite a porta para o Servidor de tempo: "))
            if 1 <= port <= 65535:
                return port
            print("Porta inválida! Escolha entre 1 e 65535.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def get_time(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5)

    while True:
        t1 = time.time()

        try:
            client.sendto("time".encode(), (ip, port))

            data, _ = client.recvfrom(1024)
            decoded_data = data.decode().strip()  
            received_time = float(decoded_data)  
            t4 = time.time()

            sync_time = received_time + ((t4 - t1) / 2)

            cliente_time = time.time() - 10 #Simulando atraso de 10 segundos para poder sincronizar

            print(f"\n\n-----------------------------------------------\n")
            print(f"T1: {t1}")
            print(f"T4: {t4}") 
            print(f"RTT: {t4 - t1}")
            print(f"Média do RTT: {(t4 - t1) / 2}")
            print(f"Hora do cliente: {cliente_time} - {float_to_hms(cliente_time)}")
            print(f"Hora recebida: {received_time} - {float_to_hms(received_time)}")
            print(f"Hora a sincronizar: {sync_time} - {float_to_hms(sync_time)}")

            maior = False
            if cliente_time > sync_time:
                maior = True

            print(f"\n\n-----------------------------------------------\n\nSincronizando...\n")

            while cliente_time != sync_time:
                if maior:
                    if decreases_two_seconds(cliente_time) > sync_time:
                        cliente_time = decreases_two_seconds(cliente_time)
                    else:
                        cliente_time = sync_time
                else:
                    if increase_two_seconds(cliente_time) < sync_time:
                        cliente_time = increase_two_seconds(cliente_time)
                    else:
                        cliente_time = sync_time
                print(f"Hora atual: {cliente_time} - {float_to_hms(cliente_time)}")
                
            print(f"\n\n-----------------------------------------------\n")
            print(f"Sincronização concluída: {cliente_time} - {float_to_hms(cliente_time)}")
            print(f"\n-----------------------------------------------\n")

        except Exception as e:
            print(f"Erro no cliente: {e}")
        finally:
            print("10 segundos até a próxima solicitação...\n")
            time.sleep(10)


get_time(get_ip(), get_port())
