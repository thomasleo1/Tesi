from bluepy import btle
from bluepy.btle import Scanner
import time
import requests
import json


# Scansiona l'area per 5 secondi
def scan_ble_devices():
    scanner = Scanner()
    devices = scanner.scan(5.0)

    device_number = len(devices)

    if device_number == 0:
        print("Nessun dispositivo trovato")
    else:
        # Mostra i dispositivi trovati
        for dev in devices:
            distance = round(calculate_distance(dev.rssi), 2)
            print("Trovato dispositivo con indirizzo {} a {} metri".format(dev.addr, distance))

            if distance <= 1.5:

                message = "Il dispositivo " + dev.addr + " è stato urtato!"
                # send_notification(message)
                send_data_to_server(dev.addr, distance)

            elif distance <= 5:

                warning_message = "ATTENZIONE! È stato trovato il dispositivo " + dev.addr + " a " + str(
                    distance) + " metri!"
                # send_notification(warning_message)


# Calcola la distanza usando RSSI
def calculate_distance(rssi):
    # RSSI = -63 valore ottenuto dalla media di 5 misure alla distanza di 1 metro (-62,-65,-62,-64,-64)
    rssi_ref = -63

    # ipotizzando ambiente interno
    n = 2

    distance = 10 ** ((rssi_ref - rssi) / (10 * n))

    return distance


# Manda una notifica push
def send_notification(message):
    device_address = "F8:C3:9E:AA:8D:D4"
    interface_address = "5C:F3:70:60:E2:A1"
    device = btle.Peripheral(device_address, addrType=btle.ADDR_TYPE_PUBLIC, iface=interface_address)

    notification_uuid = btle.UUID("")
    notification_characteristic = device.getCharacteristics(uuid=notification_uuid)

    notification_message = message
    device.writeCharacteristics(notification_characteristic, notification_message, withResponse=True)

    device.disconnect()


def send_data_to_server(address, distance):
    try:
        server_ip = "192.168.1.2"
        port = 5000
        url = f"http://{server_ip}:{port}/update"
        print(f"URL: {url}")
        data = {"Indirizzo MAC": address, "Distanza": distance}
        print("Prima della richiesta")
        print(f"Data: {data}")

        try:
            print("Sono nel try")
            response = requests.post(url, data=json.dumps(data))
            print("Dopo la richiesta")
            if response.status_code == 200:
                print("Dati inviati con successo")
            else:
                print(f"Errore nell'invio dei dati, codice errore: {response.status_code}")
                print(f"Risposta del server: {response.text}")
        except Exception as e:
            print(f"Errore durante la richiesta: {e}")
    except Exception as e:
        print(f"Errore durante la richiesta: {e}")


print("***Avvio scansione area circostante***")
print("***Premere CTRL + C per uscire***")
try:
    while True:
        print("Scansionando l'area...")
        scan_ble_devices()
        time.sleep(2)
except KeyboardInterrupt:
    pass
