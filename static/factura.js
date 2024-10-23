// script.js

document.addEventListener("DOMContentLoaded", () => {
    const productos = [];
    const facturaDiv = document.getElementById("factura");
    const guardarFacturaBtn = document.getElementById("guardar_factura");
    const telefonoContainer = document.getElementById("telefono_container");
    const numeroWspInput = document.getElementById("numero_wsp");
    const cambio_mlc = parseFloat(document.getElementById("id_cambio_mlc").value);
    const cambio_cup = parseFloat(document.getElementById("id_cambio_cup").value);

    document.getElementById("producto-form").addEventListener("submit", (event) => {
        event.preventDefault(); // Evita que el formulario se envíe de forma tradicional

        const nombreProducto = document.getElementById("id_nombre_producto").value.trim();
        const enlaceTemu = document.getElementById("id_enlace_temu").value;
        const cantidad = parseInt(document.getElementById("id_cantidad").value);
        const precio = parseFloat(document.getElementById("id_precio").value);
        const peso = parseFloat(document.getElementById("id_peso").value);
        const tipoPago = document.getElementById("id_tipo_pago").value;
        const nota = document.getElementById("id_nota").value.trim();
        
        
        

        if (nombreProducto && cantidad > 0 && precio >= 0) {
            const producto = {
                nombre: nombreProducto,
                enlace_temu: enlaceTemu,
                cantidad: cantidad,
                precio: precio,
                peso: peso,
                tipo_pago: tipoPago,
                total: cantidad * precio,
                nota: nota,
                cambio_cup: cambio_cup,
                cambio_mlc: cambio_mlc           
            };

            productos.push(producto);
            mostrarFactura();
            limpiarCampos();
        } else {
            alert("Por favor, complete todos los campos correctamente.");
        }
    });

    guardarFacturaBtn.addEventListener("click", () => {
        telefonoContainer.style.display = 'block';
    });

    numeroWspInput.addEventListener("change", () => {
        const numeroWsp = numeroWspInput.value;

        if (numeroWsp) {
            guardarFactura(numeroWsp);
        }
    });

    function mostrarFactura() {
        
        
        facturaDiv.innerHTML = ""; // Limpiar la factura anterior
        let totalFactura = 0;
        let totalCambio = 0;


        productos.forEach((producto) => {
            const productoDiv = document.createElement("div");
            productoDiv.innerHTML = `${producto.cantidad} <b>${producto.nombre}</b> - <a href="${producto.enlace_temu}">${producto.enlace_temu}</a><br> 
            <small>Peso: ${producto.peso.toFixed(2)} lb - Subtotal: $${producto.total.toFixed(2)} USD</small>`;
            facturaDiv.appendChild(productoDiv);
            totalFactura += producto.total;
            
        });
        const tipoCambio = document.querySelector('input[name="cambio_radio"]:checked'); // Asegúrate de que este sea el nombre correcto de tus inputs de radio
        if (tipoCambio) {
            if (tipoCambio.value === "CUP") {
                totalCambio = totalFactura * cambio_cup; // Multiplica por el cambio CUP
            } 
            if (tipoCambio.value === "MLC") {
                totalCambio = totalFactura * cambio_mlc; // Multiplica por el cambio MLC
            }
        }
        const totalDiv = document.createElement("div");
        if (tipoCambio) {    
            totalDiv.innerHTML = `
            <hr><strong>Total de la factura:</strong><br>
            <small>$${totalFactura.toFixed(2)} USD</small><br>
            <small>$${totalCambio.toFixed(2)} ${tipoCambio.value}</small>
            `;}
        else {
            totalDiv.innerHTML = `
            <hr><strong>Total de la factura:</strong><br>
            <small>$${totalFactura.toFixed(2)} USD</small><br>`;
        }
        facturaDiv.appendChild(totalDiv);
    }

    function limpiarCampos() {
        document.getElementById("id_nombre_producto").value = "";
        document.getElementById("id_enlace_temu").value = "";
        document.getElementById("id_cantidad").value = "1";
        document.getElementById("id_precio").value = "0.00";
        document.getElementById("id_peso").value = "0.00";
        document.getElementById("id_nota").value = "";
    }

    function guardarFactura(numeroWsp) {
        const data = {
            numero_wsp: numeroWsp,
            productos: productos
        };

        fetch('/factura/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Asegúrate de incluir el token CSRF
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('successModal').style.display = 'block';
                // Limpiar productos y ocultar el campo de teléfono
                productos.length = 0;
                facturaDiv.innerHTML = "";
                telefonoContainer.style.display = 'none';
                numeroWspInput.value = "";
            } else {
                alert("Hubo un error al guardar la factura.");
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Si esta cookie comienza con el nombre que buscamos
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
