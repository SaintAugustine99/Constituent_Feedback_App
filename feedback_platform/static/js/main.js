// Main JavaScript for Constituent Feedback Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Auto-dismiss alerts
    const autoAlerts = document.querySelectorAll('.alert-auto-dismiss');
    autoAlerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Handle file input display
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = this.files[0]?.name;
            const label = this.nextElementSibling;
            if (label && fileName) {
                label.textContent = fileName;
            }
        });
    });
    
    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = document.querySelector(this.getAttribute('data-target'));
            if (passwordInput) {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                
                // Toggle icon
                this.querySelector('i').classList.toggle('fa-eye');
                this.querySelector('i').classList.toggle('fa-eye-slash');
            }
        });
    });
    
    // Handle dynamic form fields
    function setupDynamicFormFields() {
        const addFieldButtons = document.querySelectorAll('.add-field-button');
        addFieldButtons.forEach(button => {
            button.addEventListener('click', function() {
                const fieldContainer = document.querySelector(this.getAttribute('data-container'));
                const template = document.querySelector(this.getAttribute('data-template'));
                
                if (fieldContainer && template) {
                    const newField = template.cloneNode(true);
                    newField.classList.remove('d-none');
                    newField.removeAttribute('id');
                    
                    // Setup remove button
                    const removeButton = newField.querySelector('.remove-field-button');
                    if (removeButton) {
                        removeButton.addEventListener('click', function() {
                            newField.remove();
                        });
                    }
                    
                    fieldContainer.appendChild(newField);
                }
            });
        });
    }
    
    setupDynamicFormFields();
    
    // Location services for feedback form
    const getLocationBtn = document.getElementById('getLocationBtn');
    if (getLocationBtn) {
        getLocationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latInput = document.getElementById('id_location_lat');
                    const lngInput = document.getElementById('id_location_lng');
                    const addressInput = document.getElementById('id_location_address');
                    const mapContainer = document.getElementById('location_map');
                    
                    if (latInput && lngInput) {
                        latInput.value = position.coords.latitude;
                        lngInput.value = position.coords.longitude;
                        
                        if (addressInput) {
                            addressInput.value = "Lat: " + position.coords.latitude + 
                                                ", Lng: " + position.coords.longitude;
                        }
                        
                        if (mapContainer) {
                            mapContainer.style.display = 'block';
                            // Here you would typically initialize a map
                            // This is a placeholder for map initialization
                            mapContainer.innerHTML = `
                                <div class="alert alert-info">
                                    Location captured at coordinates: (${position.coords.latitude}, ${position.coords.longitude})
                                </div>
                            `;
                        }
                    }
                }, function(error) {
                    console.error("Error getting location: ", error);
                    alert("Error getting your location. Please try again or enter your address manually.");
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        });
    }
    
    // Data table initialization (if DataTables is included)
    const dataTables = document.querySelectorAll('.datatable');
    if (typeof $.fn.DataTable !== 'undefined' && dataTables.length > 0) {
        dataTables.forEach(table => {
            $(table).DataTable({
                responsive: true,
                language: {
                    search: "_INPUT_",
                    searchPlaceholder: "Search records"
                }
            });
        });
    }
});