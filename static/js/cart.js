function updateQuantity(productId, change, stock, price) {
    const quantityInput = document.getElementById(`quantity-${productId}`);
    let currentQuantity = parseInt(quantityInput.value) || 0;
    
    // Calculate new quantity
    const newQuantity = currentQuantity + change;

    // Check if the new quantity is within allowed limits
    if (newQuantity < 1 || newQuantity > stock) {
        alert("Invalid quantity");
        return;
    }

    // Update the quantity in the input field
    quantityInput.value = newQuantity;

    // Update the total price for this product
    const productTotalElement = document.getElementById(`total-${productId}`);
    const newTotalPrice = price * newQuantity;
    productTotalElement.innerHTML = `₹${newTotalPrice.toFixed(2)}`;

    // Update the cart total
    updateCartTotal();
    
    // Send AJAX request to update the quantity in the session (optional)
    fetch(`/update_cart/${productId}/${newQuantity}`, { method: 'POST' });
}

function updateCartTotal() {
    const totalElements = document.querySelectorAll('.product-total');
    let grandTotal = 0;
    totalElements.forEach(element => {
        const total = parseFloat(element.innerText.replace('₹', ''));
        grandTotal += total;
    });
    document.getElementById('cart-total').innerText = `₹${grandTotal.toFixed(2)}`;
}
