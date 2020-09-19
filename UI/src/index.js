function agregar() {
    const arreglo = document.getElementsByClassName('form-control');

    var nombre = arreglo[0].value;
    var documento = arreglo[1].value;
    var codigo = arreglo[2].value;
    var cantidad = arreglo[3].value;
    var precio = arreglo[4].value;

    const obj = {
        nombre,
        documento,
        codigo,
        cantidad,
        precio
    }
}