document.querySelectorAll('.add-button').forEach(button => {
    button.addEventListener('click', function() {
        const quantityControls = this.nextElementSibling; // Selects the quantity controls
        quantityControls.style.display = 'flex'; // Show quantity controls
        this.style.display = 'none'; // Hide the Add button
    });
});

document.querySelectorAll('.btn-decrease').forEach(button => {
    button.addEventListener('click', function() {
        const quantitySpan = this.nextElementSibling;
        let quantity = parseInt(quantitySpan.textContent);
        
        if (quantity > 1) {
            quantity--;
            quantitySpan.textContent = quantity; // Update quantity
        } else {
            this.parentElement.style.display = 'none'; // Hide quantity controls
            this.parentElement.previousElementSibling.style.display = 'block'; // Show Add button
        }
    });
});

document.querySelectorAll('.btn-increase').forEach(button => {
    button.addEventListener('click', function() {
        const quantitySpan = this.previousElementSibling;
        let quantity = parseInt(quantitySpan.textContent);
        quantity++;
        quantitySpan.textContent = quantity; // Update quantity
    });
});

// Function to handle "View Cart" click (optional for actual cart view page)
function openCart() {
    alert(`Opening cart with ${totalItems} items and total price: ₹${totalPrice.toFixed(2)}`);
}


