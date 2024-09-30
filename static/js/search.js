function showSuggestions() {
    var query = document.getElementById('search-input').value;

    if (query.length > 0) {
        fetch(`/search_suggestions?q=${query}`)
            .then(response => response.json())
            .then(data => {
                var dropdown = document.getElementById('suggestions-dropdown');
                dropdown.innerHTML = '';

                data.forEach(item => {
                    var suggestion = document.createElement('div');
                    suggestion.className = 'suggestion-item';

                    var name = document.createElement('div');
                    name.textContent = item.name;
                    name.className = 'suggestion-name';

                    var category = document.createElement('div');
                    category.textContent = `in ${item.category}`;
                    category.className = 'suggestion-category';

                    // Append the name and category to the suggestion item
                    suggestion.appendChild(name);
                    suggestion.appendChild(category);

                    // Set the onclick event to redirect to the product details page
                    suggestion.onclick = function() {
                        window.location.href = `/product/${item.id}`; // Change this to your product details page URL
                    };

                    dropdown.appendChild(suggestion);
                });

                var viewAll = document.createElement('div');
                viewAll.className = 'suggestion-item view-all';
                viewAll.textContent = 'VIEW ALL';
                viewAll.onclick = function() {
                    window.location.href = `/catalog?search=${query}`;
                };
                dropdown.appendChild(viewAll);

                dropdown.style.display = 'block';
            });
    } else {
        document.getElementById('suggestions-dropdown').style.display = 'none';
    }
}
// Hide dropdown on clicking outside
document.addEventListener('click', function(event) {
    var dropdown = document.getElementById('suggestions-dropdown');
    var searchContainer = document.querySelector('.search-container');

    if (!searchContainer.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});