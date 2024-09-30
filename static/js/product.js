function toggleQuantitySelector(button) {
    const form = button.closest('form');
    button.style.display = 'none';  // Hide the "Add" button
    const quantitySelector = form.querySelector('.quantity-selector');
    quantitySelector.style.display = 'flex';
    
    const initialQuantity = 1; // Start with 1 product
    updateCart(form, initialQuantity);
    showNotification(initialQuantity);
}

function changeQuantity(button, change) {
    const quantityInput = button.parentElement.querySelector('.quantity-input');
    let currentQuantity = parseInt(quantityInput.value) || 1;
    currentQuantity += change;
    
    // Check if the quantity reaches 0
    if (currentQuantity < 1) {
        currentQuantity = 0; // Set it to 0
    }
    
    const form = button.closest('form');
    
    // If the quantity is 0, show the "Add" button and hide the quantity selector
    if (currentQuantity === 0) {
        const addButton = form.querySelector('.add-button');
        const quantitySelector = form.querySelector('.quantity-selector');
        
        addButton.style.display = 'inline-block';  // Show the "Add" button
        quantitySelector.style.display = 'none';   // Hide the quantity selector
        updateCart(form, 0);  // Update cart to remove the product
    } else {
        updateCart(form, currentQuantity);  // Update cart with the new quantity
    }
    
    quantityInput.value = currentQuantity; // Update the input field
    showNotification(currentQuantity); // Show notification
}

function updateCart(form, quantity) {
    const formData = new FormData(form);
    formData.append('quantity', quantity); // Update with the correct quantity
    const actionURL = form.action; // Get action URL

    fetch(actionURL, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not OK');
        return response.json();
    })
    .then(data => {
        console.log('Product added/updated in cart:', data);
        if (quantity === 0) {
            showNotification("Product removed from cart.");
        } else {
            showNotification(quantity); // Update notification for the correct quantity
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
    });
}

function showNotification(quantity) {
    const notificationContainer = document.querySelector('.notification-container');
    const notification = document.getElementById('notification');
    const productText = quantity === 1 ? 'product' : 'products';
    notification.textContent = `Added ${quantity} ${productText} to cart.`;

    // Show notification by removing 'display: none' and adding the 'show' class
    notificationContainer.style.display = 'flex'; // Change 'none' to 'flex' to display it
    notificationContainer.classList.add('show'); // Add the 'show' class for the animation

    // Add functionality to the 'View Cart' button
    document.getElementById('view-cart-button').onclick = function() {
        window.location.href = '/cart'; // Redirect to cart page
    };

}
