console.log("ElectroMart main.js loaded.");

// Future JavaScript for dynamic interactions will go here.
// For example:
// - AJAX calls to add items to cart
// - Form validation
// - Interactive UI elements

// Handle flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Handle quantity inputs
document.querySelectorAll('.quantity-form input[type="number"]').forEach(input => {
    input.addEventListener('change', function() {
        const max = parseInt(this.getAttribute('max'));
        const min = parseInt(this.getAttribute('min'));
        let value = parseInt(this.value);

        if (value > max) this.value = max;
        if (value < min) this.value = min;
    });
});

// Format credit card input
document.querySelectorAll('input[name="card_number"]').forEach(input => {
    input.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s/g, '');
        let formattedValue = value.replace(/(\d{4})/g, '$1 ').trim();
        e.target.value = formattedValue;
    });
});

// Format expiry date input
document.querySelectorAll('input[name="expiry_date"]').forEach(input => {
    input.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length >= 2) {
            value = value.slice(0,2) + '/' + value.slice(2);
        }
        e.target.value = value;
    });
});

// Handle mobile navigation
const mobileMenuButton = document.querySelector('.mobile-menu-button');
const nav = document.querySelector('nav ul');

if (mobileMenuButton && nav) {
    mobileMenuButton.addEventListener('click', () => {
        nav.classList.toggle('show');
    });
}

// Handle form validation
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});

// Handle image loading errors
document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', function() {
        this.src = '/static/images/placeholder.png';
    });
});

// Handle sort and filter changes
const sortSelect = document.getElementById('sort-select');
if (sortSelect) {
    sortSelect.addEventListener('change', function() {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('sort', this.value);
        window.location.search = urlParams.toString();
    });
}

// Set current sort value
document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        const urlParams = new URLSearchParams(window.location.search);
        const sortValue = urlParams.get('sort');
        if (sortValue) {
            sortSelect.value = sortValue;
        }
    }
});

// Handle add to cart animation
document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const button = this.querySelector('button[type="submit"]');
        if (button) {
            button.textContent = 'Added!';
            button.classList.add('added');
            setTimeout(() => {
                button.textContent = 'Add to Cart';
                button.classList.remove('added');
            }, 2000);
        }
    });
});