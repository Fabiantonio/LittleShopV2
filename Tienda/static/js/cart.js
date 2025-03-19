// Cart functionality with AJAX
document.addEventListener('DOMContentLoaded', function() {
    // Cart toggle functionality
    const carritoBtn = document.getElementById('btnMostrarCarrito');
    const carritoContainer = document.getElementById('carrito2');
    const carritoCerrarBtn = document.getElementById('carrito-cerrar');
    
    // Mostrar carrito al hacer clic en el botón
    if (carritoBtn && carritoContainer) {
        carritoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            carritoContainer.classList.add('show');
        });
    }
    
    // Cerrar carrito al hacer clic en el botón de cerrar
    if (carritoCerrarBtn && carritoContainer) {
        carritoCerrarBtn.addEventListener('click', function(e) {
            e.preventDefault();
            carritoContainer.classList.remove('show');
        });
    }
    
    // Cerrar carrito al hacer clic fuera del carrito
    document.addEventListener('click', function(e) {
        if (carritoContainer && carritoContainer.classList.contains('show')) {
            // Si el clic no fue dentro del carrito ni en el botón de mostrar carrito
            if (!carritoContainer.contains(e.target) && e.target !== carritoBtn && !carritoBtn.contains(e.target)) {
                carritoContainer.classList.remove('show');
            }
        }
    });
    
    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    if (addToCartButtons.length > 0) {
        addToCartButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.getAttribute('data-product-id');
                
                fetch('/agregar_al_carrito/' + productId + '/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateCartCount(data.cart_count);
                        showMessage('Producto agregado al carrito', 'success');
                        // Show cart after adding product
                        if (carritoContainer) {
                            carritoContainer.classList.add('show');
                            // Reload cart contents
                            window.location.reload();
                        }
                    } else {
                        showMessage('Error al agregar el producto', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error en la solicitud', 'error');
                });
            });
        });
    }

    // Update quantity functionality
    const quantityButtons = document.querySelectorAll('.update-quantity');
    if (quantityButtons.length > 0) {
        quantityButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.getAttribute('data-product-id');
                const action = this.getAttribute('data-action');
                
                fetch('/actualizar_cantidad/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        product_id: productId,
                        action: action
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the quantity display
                        const quantityElement = document.querySelector(`.quantity-${productId}`);
                        if (quantityElement) {
                            quantityElement.textContent = data.quantity;
                        }
                        
                        // Update the subtotal
                        const subtotalElement = document.querySelector(`.subtotal-${productId}`);
                        if (subtotalElement) {
                            subtotalElement.textContent = '$' + data.subtotal;
                        }
                        
                        // Update the cart total
                        const totalElement = document.querySelector('.cart-total');
                        if (totalElement) {
                            totalElement.textContent = '$' + data.total;
                        }
                        
                        updateCartCount(data.cart_count);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error en la solicitud', 'error');
                });
            });
        });
    }

    // Remove item functionality
    const removeButtons = document.querySelectorAll('.remove-item');
    if (removeButtons.length > 0) {
        removeButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const productId = this.getAttribute('data-product-id');
                
                fetch('/eliminar_del_carrito/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        product_id: productId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove the row from the table
                        const row = this.closest('tr');
                        if (row) {
                            row.remove();
                        }
                        
                        // Update the cart total
                        const totalElement = document.querySelector('.cart-total');
                        if (totalElement) {
                            totalElement.textContent = '$' + data.total;
                        }
                        
                        updateCartCount(data.cart_count);
                        
                        // If cart is empty, show empty cart message
                        if (data.cart_count === 0) {
                            const cartItems = document.querySelector('.cart-items');
                            if (cartItems) {
                                cartItems.innerHTML = '<div class="empty-cart"><p>Tu carrito está vacío</p><a href="/" class="btn btn-primary">Ir a comprar</a></div>';
                            }
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error en la solicitud', 'error');
                });
            });
        });
    }

    // Clear cart functionality
    const clearCartButton = document.querySelector('.clear-cart');
    if (clearCartButton) {
        clearCartButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            fetch('/limpiar_carrito/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Replace cart items with empty cart message
                    const cartContainer = document.querySelector('.cart-container');
                    if (cartContainer) {
                        cartContainer.innerHTML = `
                            <h2>Carrito de Compras</h2>
                            <div class="empty-cart">
                                <p>Tu carrito está vacío</p>
                                <a href="/" class="btn btn-primary">Ir a comprar</a>
                            </div>
                        `;
                    }
                    
                    updateCartCount(0);
                    showMessage('Carrito limpiado', 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error en la solicitud', 'error');
            });
        });
    }

    // Helper function to get CSRF token
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

    // Helper function to update cart count in the UI
    function updateCartCount(count) {
        const cartCountElement = document.querySelector('.badge');
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    }

    // Helper function to show messages
    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} message-alert`;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(messageDiv);
            }, 500);
        }, 2000);
    }
});