document.addEventListener("DOMContentLoaded", function() {
    // Select all category options (radio buttons or checkboxes)
    const categoryOptions = document.querySelectorAll('input[name="vitamins_category"]'); // Updated name
    const brandContainer = document.getElementById('brandContainer');
    const brandOptions = document.querySelectorAll('input[name="vitamins_brand"]'); // Updated name

    // Function to update brands based on selected category
    function updateBrands(selectedCategoryId) {
        brandOptions.forEach(option => {
            const brandCategoryId = option.parentElement.getAttribute('data-category');
            // Show or hide brands based on the selected category
            option.parentElement.style.display = (selectedCategoryId === brandCategoryId) ? 'block' : 'none';
        });

        // Check if any brand is visible
        const anyBrandsVisible = Array.from(brandOptions).some(opt => opt.parentElement.style.display === 'block');
        // Show or hide the brand container
        brandContainer.style.display = anyBrandsVisible ? 'block' : 'none';
    }

    // Add event listeners to category options
    categoryOptions.forEach(option => {
        option.addEventListener('change', function() {
            const selectedCategoryId = this.value;
            updateBrands(selectedCategoryId);
        });
    });

    // Automatically show brands for the default category on page load
    const defaultCategoryId = '1'; // Set your default category ID
    const defaultCategoryOption = document.querySelector(`input[name="vitamins_category"][value="${defaultCategoryId}"]`);
    if (defaultCategoryOption) {
        defaultCategoryOption.checked = true;
        updateBrands(defaultCategoryId);
    }

    // Initial setup if a category is preselected
    const initialSelectedCategory = document.querySelector('input[name="vitamins_category"]:checked');
    if (initialSelectedCategory) {
        updateBrands(initialSelectedCategory.value);
    }
});
