document.addEventListener('DOMContentLoaded', () => {
    const categoryItems = document.querySelectorAll('.sidebar li');
    const productItems = document.querySelectorAll('.product-item');
    const viewAllButtons = document.querySelectorAll('.view-all');

    // Function to filter products based on category
    function filterProducts(category) {
        productItems.forEach(product => {
            if (product.getAttribute('data-category') === category || category === 'All') {
                product.classList.add('active');
            } else {
                product.classList.remove('active');
            }
        });

        // Show or hide the correct "View All" button based on the category
        viewAllButtons.forEach(button => {
            if (button.getAttribute('data-category') === category) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });
    }

    // Add click event to category items
    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            const category = item.getAttribute('data-category');
            filterProducts(category);
        });
    });

    // Show 'Personal Care' category by default
    filterProducts('Personal Care');
});

