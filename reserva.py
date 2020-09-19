import zmq
import pymongo
import time

# Data de entrada simulada
# pedido = {
#     "codigo": [
#         "I0001", "I0002", "I0003"
#     ],
#     "cantidad": [
#         "10", "20", "30"
#     ]
# }






coleccion = ''

def conexion(password):
    global coleccion
    client = pymongo.MongoClient("mongodb+srv://admin:" + password + "@cluster0.mgzh4.mongodb.net/modulo_compras?retryWrites=true&w=majority")
    ddbb = client.modulo_compras
    coleccion = ddbb.inventario

def consultarStock(pedido):
    pedido_result = {
        "posible": True,
        "estado":[],
        "mensaje":[]
    }

    for i in range(len(pedido.get("codigo"))):
        codigo = pedido.get("codigo")[i]
        cantidad = int(pedido.get("cantidad")[i])

        res = coleccion.find({"codigo":codigo})
        for document in res:
            stock = document.get("cantidad")
            if(stock >= cantidad):
                pedido_result.get("estado").append("HAY_STOCK")
                pedido_result.get("mensaje").append("")
            else:
                pedido_result["posible"] = False
                pedido_result.get("estado").append("NO_HAY_STOCK")
                pedido_result.get("mensaje").append(f"El stock del item {codigo} es de {stock}, no se puede cubrir un pedido de {cantidad}")

    return pedido_result

def reservar(pedido):
    for i in range(len(pedido.get("codigo"))):
        codigo = pedido.get("codigo")[i]
        cantidad = int(pedido.get("cantidad")[i])

        print("\n----------Operacion----------")
        print(f"Codigo: {codigo} | Cantidad: {cantidad}")

        res = coleccion.find({"codigo":codigo})
        for document in res:
            stock = document.get("cantidad")
            stock_final = stock - cantidad
            coleccion.update_one({"codigo": codigo},{"$set": {"cantidad": stock_final}})
            print(f"Stock inicial: {stock} | Stock final: {stock_final}")

def main():
    try:
        conexion("bbddproyectosisdib")
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://*:5555')

        while True:
            print("\nEsperando pedido")
            pedido = socket.recv_json()
            print(f"Pedido recibido: {pedido}")

            pedido_result = consultarStock(pedido)
            print(f"Pedido Result: {pedido_result}")
            if(pedido_result.get("posible")):
                print("Pedido posible")
                reservar(pedido)
                # Enviar un mensaje al siguiente modulo
                socket.send_json(
                    {
                        "posible": True,
                        "estado": ["Hay stock"],
                        "mensaje": ["El pedido es valido"]
                    }
                )
            else:
                print("Pedido imposible")
                socket.send_json(pedido_result)
                continue            
            
    except Exception as e:
        print("\nError: " + format(e))
        input("Presiona enter para salir")

main()