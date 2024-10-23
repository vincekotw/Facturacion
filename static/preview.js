document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btn-preview').addEventListener('click', function(event) {
        event.preventDefault();

        // Capturando los valores de los campos del formulario
        const nombreProducto = document.getElementById('id_nombre_producto').value;
        const imagenProducto = document.getElementById('id_imagen_producto').value;
        const precio = document.getElementById('id_precio').value;
        const moneda = document.getElementById('id_moneda_producto').value;
        const tamanno = document.getElementById('id_tamanno').value;

        // Creando el HTML del card usando clases de Bootstrap
        const cardHTML = `
            <div class='card mt-3' style='width: 18rem;'>
                <img src='${imagenProducto}' class='card-img-top' alt='${nombreProducto}'>
                <div class='card-body'>
                    <h5 class='card-title'>${nombreProducto}</h5>
                    <p class='card-text'>Precio: ${precio} ${moneda}</p>
                    <small class='card-text'>Tamaño: ${tamanno} cm</small>
                </div>
            </div>`;

        // Insertando el card en el div de preview
        const previewDiv = document.getElementById('preview');
        previewDiv.innerHTML = cardHTML;

        document.getElementById('btn-reset').addEventListener('click', function() {
            previewDiv.innerHTML = "";
            nombreProducto.value = "";
            imagenProducto.value = "";
            precio.value = 0.00;
            moneda.value = "";
            tamanno.value = 0.0;
        });
        // Agregando evento al botón "Añadir al Catálogo"
        document.getElementById('addToCatalog').addEventListener('click', function() {
            if(nombre_producto!="" || imagen_producto!=""){
                fetch('/annadir-catalogo/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),  // Asegúrate de incluir el token CSRF
                    },
                    body: JSON.stringify({
                        nombre_producto: nombreProducto,
                        imagen_producto: imagenProducto,
                        precio: precio,
                        moneda_producto: moneda,
                        tamanno: tamanno
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('successModal').style.display = 'block';
                        previewDiv.innerHTML = "";
                        nombreProducto.value = "";
                        imagenProducto.value = "";
                        precio.value = 0.00;
                        moneda.value = "";
                        tamanno.value = 0.0;
                    } else {
                        alert("Hubo un error al guardar el producto");
                    }
                })
                .catch(error => console.error('Error:', error));
            }
            
        });
    });
});

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
