document.addEventListener("DOMContentLoaded", () => {
    const clientListItems = document.querySelectorAll("#client-list .btn-outline-success");
    const productosContainer = document.getElementById("productos-container");

    clientListItems.forEach(item => {
        item.addEventListener("click", () => {
            const numeroWsp = item.getAttribute("data-numero-wsp");
            cargarProductos(numeroWsp);
        });
    });

    function cargarProductos(numeroWsp) {
        productosContainer.innerHTML = "<p>Cargando productos...</p>"; // Mostrar mensaje de carga

        fetch('/clientes/', {  // Cambia esta URL según tu configuración de URL en Django
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Asegúrate de incluir el token CSRF
            },
            body: JSON.stringify({ 
                numero_wsp: numeroWsp,
                form_name: 'form1' // Añadir el campo form_name aquí
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los productos');
            }
            return response.json();
        })
        .then(data => {
            mostrarProductos(data,numeroWsp);
        })
        .catch(error => {
            console.error('Error:', error);
            productosContainer.innerHTML = "<p>Error al obtener los productos. Inténtalo de nuevo más tarde.</p>";
        });
    }

    function mostrarProductos(data, numeroWsp) {
        productosContainer.innerHTML = ""; // Limpiar el contenedor de productos
        if (data.length === 0) {
            productosContainer.innerHTML = "<p>No hay productos para este cliente.</p>";
            return;
        }
        const contactoDiv = document.createElement("div");
        contactoDiv.classList.add("col-md-10");
        const staticUrl = '/static/'
        contactoDiv.innerHTML = `
        <a href="tel:+53${numeroWsp}">
            <button class="btn btn-outline-primary float-end"><b>Llamar</b><img src="${staticUrl}1F4DE_black.png" alt="Call" height="25"></button>
        </a>
        <a href="http://wa.me/53${numeroWsp}" target="_blank">
        <button class="btn btn-outline-success float-end me-2"><b>Contactar</b> <img src="${staticUrl}wsplogo.png" alt="Via WhatApp" height="25"></button></a>
        <a href="${numeroWsp}" class="btn btn-outline-secondary"><img src="${staticUrl}1159633.png" alt="Editar Contacto" height="25"> Editar Contacto</a>
        `;
        productosContainer.appendChild(contactoDiv);
        // Agrupar productos por fecha
        const productosPorFecha = {};
        data.forEach(producto => {
            const fecha = producto.fecha; // Obtener solo la fecha (sin hora)
            if (!productosPorFecha[fecha]) {
                productosPorFecha[fecha] = [];
            }
            productosPorFecha[fecha].push(producto);
        });

        // Mostrar productos agrupados por fecha
        let ultimaFechaMostrada = null; // Variable para almacenar la última fecha mostrada
        for (const fecha in productosPorFecha) {
            // Solo mostrar la fecha si es diferente de la última fecha mostrada
            if (fecha !== ultimaFechaMostrada) {
                const fechaDiv = document.createElement("div");
                fechaDiv.classList.add("fecha-producto", "col-md-10");
                fechaDiv.innerHTML = `
                <br><h4>${fecha}</h4>
                `;
                const tableDivDiv = document.createElement("div");
                tableDivDiv.classList.add("table-responsive");
                
                const tableDiv = document.createElement("table");
                tableDiv.classList.add("table", "align-middle")
                tableDiv.innerHTML = `
                <tr><th scope="col"><strong>Productos: </strong></th><th scope="col">
                <b>Enlace:</b></th><th scope="col">
                <b>Cantidad:</b></th><th scope="col">
                <b>Precio:</b></th><th scope="col">
                <b>Total:</b></th><th scope="col">
                <b>Estado:</b></th></tr>
                `;
                
                let totalPorFecha = 0;
                productosPorFecha[fecha].forEach(producto => {
                    const productoDiv = document.createElement("tr");
                    productoDiv.style.overflowWrap = "break-word"; 
                    productoDiv.style.whiteSpace = "normal";
                    const precio = parseFloat(producto.precio); 
                    const subtotal = parseFloat(producto.total); 
                    totalPorFecha += subtotal;
                    var estado = "No encargado";
                    if (producto.encargado)
                        estado = "Encargado"
                    if (producto.recibido)
                        estado = "Recibido"
                    if (producto.entregado)
                        estado = "Entregado"
                    productoDiv.innerHTML = `   
                    <td>${producto.nombre_producto}</td><td> 
                        <a href="${producto.enlace_temu}" style="padding-top: 0.0rem;">${producto.enlace_temu}</a></td><td>  
                        ${producto.cantidad}</td><td>  
                        $${isNaN(precio) ? '0.00' : precio.toFixed(2)}</td><td> 
                        <b>$${isNaN(subtotal) ? '0.00' : subtotal.toFixed(2)}</b></td>
                        <td>${estado}</td> 
                    `;
                    tableDiv.appendChild(productoDiv);
                    tableDivDiv.appendChild(tableDiv);
                });
                
                const totalDiv = document.createElement("tr");
                totalDiv.innerHTML = `
                <td colspan="4" style="text-align: right;"><strong>Total por fecha:</strong></td>
                <td><b>$${totalPorFecha.toFixed(2)}</b></td>
                <td></td>
                `;
                const bottonDiv = document.createElement("tr");
                bottonDiv.innerHTML = `
                <td colspan="6" style="text-align: right;"><a href="${numeroWsp}/${fecha}/" class="btn btn-outline-secondary btn-sm float-end mt-2"><img src="${staticUrl}1159633.png" alt="Editar Factura" height="25"> Modificar Factura</a><h4 class="mt-2"></td>
                `
                
                tableDiv.appendChild(totalDiv);
                tableDiv.appendChild(bottonDiv);
                fechaDiv.appendChild(tableDiv);
                productosContainer.appendChild(fechaDiv);
                ultimaFechaMostrada = fecha; // Actualizar la última fecha mostrada
            }
            
        }
        
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
