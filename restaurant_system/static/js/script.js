// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Cart functionality
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    const cartIcon = document.getElementById('cart-icon');
    const cartPanel = document.getElementById('cart-panel');
    const cartCount = document.querySelector('.cart-count');
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total-amount');
    const checkoutBtn = document.getElementById('checkout-btn');
    
    // Update cart display
    function updateCartDisplay() {
        let totalItems = 0;
        let totalAmount = 0;
        
        cartItems.innerHTML = '';
        
        for (const dishId in cart) {
            totalItems += cart[dishId].quantity;
            totalAmount += cart[dishId].quantity * cart[dishId].price;
            
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <h4>${cart[dishId].name}</h4>
                <p>Quantity: ${cart[dishId].quantity}</p>
                <p>Price: $${(cart[dishId].quantity * cart[dishId].price).toFixed(2)}</p>
                <button class="remove-from-cart" data-dish-id="${dishId}">Remove</button>
            `;
            cartItems.appendChild(cartItem);
        }
        
        cartCount.textContent = totalItems;
        cartTotal.textContent = totalAmount.toFixed(2);
        
        // Save to localStorage
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    
    // Add to cart
    function addToCart(dishId, dishName, dishPrice) {
        if (cart[dishId]) {
            cart[dishId].quantity += 1;
        } else {
            cart[dishId] = {
                name: dishName,
                price: dishPrice,
                quantity: 1
            };
        }
        updateCartDisplay();
    }
    
    // Remove from cart
    function removeFromCart(dishId) {
        if (cart[dishId]) {
            delete cart[dishId];
            updateCartDisplay();
        }
    }
    
    // Event listeners for quantity buttons
    document.querySelectorAll('.quantity-btn.plus').forEach(btn => {
        btn.addEventListener('click', function() {
            const dishId = this.dataset.dishId;
            const dishName = this.closest('.dish-card').querySelector('h3').textContent;
            const dishPrice = parseFloat(this.closest('.dish-card').querySelector('.price').textContent.replace('$', ''));
            
            addToCart(dishId, dishName, dishPrice);
            
            // Update quantity display
            const quantityElement = document.getElementById(`quantity-${dishId}`);
            quantityElement.textContent = cart[dishId] ? cart[dishId].quantity : 0;
        });
    });
    
    document.querySelectorAll('.quantity-btn.minus').forEach(btn => {
        btn.addEventListener('click', function() {
            const dishId = this.dataset.dishId;
            
            if (cart[dishId] && cart[dishId].quantity > 0) {
                cart[dishId].quantity -= 1;
                if (cart[dishId].quantity === 0) {
                    delete cart[dishId];
                }
                updateCartDisplay();
                
                // Update quantity display
                const quantityElement = document.getElementById(`quantity-${dishId}`);
                quantityElement.textContent = cart[dishId] ? cart[dishId].quantity : 0;
            }
        });
    });
    
    // Cart panel toggle
    cartIcon.addEventListener('click', function() {
        cartPanel.classList.toggle('show');
    });
    
    // Remove from cart event delegation
    cartItems.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-from-cart')) {
            const dishId = e.target.dataset.dishId;
            removeFromCart(dishId);
            
            // Update quantity display
            const quantityElement = document.getElementById(`quantity-${dishId}`);
            if (quantityElement) {
                quantityElement.textContent = 0;
            }
        }
    });
    
    // Checkout
    checkoutBtn.addEventListener('click', function() {
        if (Object.keys(cart).length === 0) {
            alert('Your cart is empty!');
            return;
        }
        
        const tableNumber = prompt('Please enter your table number:');
        if (!tableNumber) {
            return;
        }
        
        const orderItems = [];
        for (const dishId in cart) {
            orderItems.push({
                dish_id: parseInt(dishId),
                quantity: cart[dishId].quantity
            });
        }
        
        fetch('/api/order/place', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table_number: parseInt(tableNumber),
                items: orderItems
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Order placed successfully!');
                cart = {};
                updateCartDisplay();
                
                // Reset all quantity displays
                document.querySelectorAll('.quantity').forEach(el => {
                    el.textContent = '0';
                });
                
                cartPanel.classList.remove('show');
            } else {
                alert('Failed to place order. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to place order. Please try again.');
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    
    searchBtn.addEventListener('click', function() {
        const searchTerm = searchInput.value.trim();
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('search', searchTerm);
        window.location.href = currentUrl.toString();
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchBtn.click();
        }
    });
    
    // Initialize cart display
    updateCartDisplay();
});