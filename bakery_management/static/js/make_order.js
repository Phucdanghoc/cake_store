document.addEventListener('DOMContentLoaded', () => {
    const productSearchInput = document.getElementById('productSearch');
    const productTableBody = document.querySelector('table tbody');
    const paymentBtn = document.getElementById('paymentBtn');

    paymentBtn.addEventListener('click', handlePayment);
    // Event listener for product search
    productSearchInput.addEventListener('input', () => {
        fetchProducts(productSearchInput.value);
    });

    // Function to fetch products from the API
    function fetchProducts(query) {
        if (query.trim() !== "") {
            fetch(`/api/products?name=${query}`)
            .then(response => response.json())
            .then(products => {
                displayProducts(products);
            })
            .catch(error => {
                console.error('Error fetching products:', error);
            });
        }
    }

    // Function to display products in the table
    function displayProducts(products) {
        productTableBody.innerHTML = '';  // Clear current table content
        products.forEach(product => {
            const row = document.createElement('tr');
            row.dataset.productId = product.id;  // Store product ID in the row for easy access
            
            row.innerHTML = `
                <td><img src="${product.image_url}" alt="${product.name}" width="50" height="50"></td>
                <td>${product.name}</td>
                <td>${product.category}</td>
                <td>${product.flavor}</td>
                <td>${product.price}</td>
                <td>${product.availability}</td>
            `;
            
            row.addEventListener('click', () => handleProductSelect(product)); // Bind click event to row
            productTableBody.appendChild(row);
        });
    }

    // Function to handle product selection
    function handleProductSelect(product) {
        const selectedProductsContainer = document.querySelector('.selected-products');
        
        const selectedProductCard = document.createElement('div');
        selectedProductCard.classList.add('product-item', 'card', 'mb-2');
        selectedProductCard.dataset.productId = product.id; // Store product ID for later removal
        selectedProductCard.innerHTML = `
            <div class="card-body d-flex align-items-center justify-content-between">
                <div class="d-flex flex-column w-75">
                    <h5 class="product-name">${product.name}</h5>
                    <div class="d-flex justify-content-between">
                        <span class="product-price">${product.price.toLocaleString()} VND</span>
                        <span class="product-category">${product.category}</span>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span class="product-flavor">${product.flavor}</span>
                        <span class="product-stock">${product.stock > 0 ? "In Stock" : "Out of Stock"}</span>
                    </div>
                    <input type="number" class="form-control mt-1 product-quantity" min="1" value="1" onchange="updateQuantity(this, ${product.price}, ${product.id})" />
                    <span class="product-total-price">Total: ${product.price} VND</span>
                </div>
                <button class="btn btn-danger remove-product-btn">Remove</button>
            </div>
        `;
        
        // Add event listener to "Remove" button
        selectedProductCard.querySelector('.remove-product-btn').addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent the card click handler from firing
            removeProduct(product.id); // Remove product on click
        });

        selectedProductsContainer.appendChild(selectedProductCard);
        updateTotalPrice();
    }
    
    // Function to update the quantity of a product
    function updateQuantity(input, price, productId) {
        const quantity = parseInt(input.value);
        const totalPrice = quantity * price;
        const productCard = document.querySelector(`.product-item[data-product-id='${productId}']`);
        
        if (productCard) {
            productCard.querySelector('.product-total-price').innerText = `Total: ${totalPrice} VND`;
            updateTotalPrice();
        }
    }

    // Function to remove a product from the order
    function removeProduct(productId) {
        const productItem = document.querySelector(`.product-item[data-product-id='${productId}']`);
        if (productItem) {
            productItem.remove();
            updateTotalPrice();
        }
    }

    function updateTotalPrice() {
        let total = 0;
        document.querySelectorAll('.selected-products .product-item').forEach(item => {
            const quantity = parseInt(item.querySelector('.product-quantity').value);
            const price = parseInt(item.querySelector('.product-price').innerText.replace(' VND', '').replace(',', ''));
            total += quantity * price;
        });
        document.querySelector('.total-card h5').innerText = `Total: ${total.toLocaleString()} VND`;
    }
    function handlePayment() {
        const selectedProducts = [];
        document.querySelectorAll('.selected-products .product-item').forEach(item => {
            const productId = item.dataset.productId;
            const quantity = parseInt(item.querySelector('.product-quantity').value);
            selectedProducts.push({
                product: productId,
                quantity: quantity
            });
        });
    
        if (selectedProducts.length === 0) {
            alert("Please select at least one product to proceed.");
            return;
        }
        const orderData = {
            status: "pending",
            items: selectedProducts
        };
    
        // Get the CSRF token
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            alert("CSRF token not found. Please refresh the page and try again.");
            return;
        }
    
        // Send the POST request to create the order
        fetch('/api/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Send the CSRF token for security
            },
            body: JSON.stringify(orderData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to create order. Please try again.");
            }
            return response.json();
        })
        .then(data => {
            if (data.id) {
                alert("Order created successfully!");
                window.location.reload(); // Optionally reload or redirect to an order summary page
            } else {
                alert("Failed to create order. Please try again.");
                console.error("Order creation error:", data);
            }
        })
        .catch(error => {
            console.error("Error during order creation:", error);
            alert("An error occurred. Please try again.");
        });
    }
    
    function getCsrfToken() {
        const csrfTokenCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfTokenCookie ? csrfTokenCookie.split('=')[1] : null;
    }
    
    
});
