document.addEventListener("DOMContentLoaded", function() {
    const categoryOptions = document.querySelectorAll('input[name="product_category"]');
    const subcategoryContainer = document.getElementById('subcategoryContainer');
    const brandContainer = document.getElementById('brandContainer');
    
    const subcategoryOptions = document.querySelectorAll('input[name="subcategory"]');
    const brandOptions = document.querySelectorAll('input[name="brand"]');

    function updateSubcategories(selectedCategoryId) {
        subcategoryOptions.forEach(option => {
            const subcategoryCategoryId = option.parentElement.getAttribute('data-category');
            option.parentElement.style.display = (selectedCategoryId === subcategoryCategoryId) ? 'block' : 'none';
        });
        
        const anySubcategoriesVisible = Array.from(subcategoryOptions).some(opt => opt.parentElement.style.display === 'block');
        document.getElementById('subcategoryContainer').style.display = anySubcategoriesVisible ? 'block' : 'none';
        
        // Reset brands when category changes
        updateBrands(''); 
    }

    function updateBrands(selectedSubcategoryId) {
        brandOptions.forEach(option => {
            const brandSubcategoryId = option.parentElement.getAttribute('data-subcategory');
            option.parentElement.style.display = (selectedSubcategoryId === brandSubcategoryId) ? 'block' : 'none';
        });
    
        const anyBrandsVisible = Array.from(brandOptions).some(opt => opt.parentElement.style.display === 'block');
        document.getElementById('brandContainer').style.display = anyBrandsVisible ? 'block' : 'none';
    }

    // In the subcategory change event
    subcategoryOptions.forEach(option => {
        option.addEventListener('change', function() {
            const selectedSubcategoryId = this.value;
            updateBrands(selectedSubcategoryId);
        });
    });
    

    categoryOptions.forEach(option => {
        option.addEventListener('change', function() {
            const selectedCategoryId = this.value;
            updateSubcategories(selectedCategoryId);
        });
    });
    

    // Automatically show subcategories and brands for the default category on page load
    const defaultCategoryId = '1'; // Set your default category ID
    const defaultCategoryOption = document.querySelector(`input[name="product_category"][value="${defaultCategoryId}"]`);
    if (defaultCategoryOption) {
        defaultCategoryOption.checked = true;
        updateSubcategories(defaultCategoryId);
    }
    // Initial setup if a category is preselected
    const initialSelectedCategory = document.querySelector('input[name="product_category"]:checked');
    if (initialSelectedCategory) {
        updateSubcategories(initialSelectedCategory.value);
    }
});
