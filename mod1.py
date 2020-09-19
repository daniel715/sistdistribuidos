import zmq
import json
import time
context = zmq.Context()

# Data simulada
pedido = {
    "nombre": "Renzo Macalupu",
    "documento": "74742441",
    "codigo":["I0001","I0002","I0003"],
    "cantidad":["10","20","300000"],
    "precio": []
}

print('Conectando al servidor')
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

# Envia la data al servidor
socket.send_json(pedido)

# Recibe la data del servidor
respuesta = socket.recv_json()
if(respuesta.get("posible")):
    print(f"Respuesta: {respuesta.get('mensaje')[0]}")
else:
    print("El pedido no es posible")
    for i in range(len(respuesta.get("estado"))):
        if(respuesta.get("estado")[i] == "NO_HAY_STOCK"):
            print(respuesta.get("mensaje")[i])

input("Presiona enter para salir")