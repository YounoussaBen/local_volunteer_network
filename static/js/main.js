/**
 * LocalVolunteer Network - Main JavaScript
 * Handles interactive elements, animations and functional components
 */

'use strict';

// Wrap everything in an IIFE (Immediately Invoked Function Expression)
(function() {
    // DOM Elements
    const body = document.body;
    const preloader = document.getElementById('preloader');
    const navbar = document.getElementById('mainNav');
    const backToTop = document.querySelector('.back-to-top');
    const toasts = document.querySelectorAll('.toast');
    const searchForm = document.getElementById('opportunity-search-form');
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    const opportunityCards = document.querySelectorAll('.opportunity-card');
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    const tooltipTriggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const animatedCounters = document.querySelectorAll('.animated-counter');
    
    /**
     * Initialize when DOM is fully loaded
     */
    document.addEventListener('DOMContentLoaded', function() {
        // Remove preloader after page load
        setTimeout(removePreloader, 800);
        
        // Initialize interactive elements
        initializeTooltips();
        initializeToasts();
        initializePasswordToggle();
        initializeFormValidation();
        initializeConfirmButtons();
        
        // Handle scroll events
        handleNavbarScroll();
        handleBackToTop();
        
        // Handle specific page functionality
        handleSearchForm();
        handleOpportunityCards();
        
        // Initialize animated counters
        initializeCounters();
        
        // Initialize datetime inputs
        initializeDateTimeInputs();
        
        // Initialize dropdowns
        initializeDropdowns();
    });

    /**
     * Remove preloader with fade effect
     */
    function removePreloader() {
        if (preloader) {
            preloader.style.opacity = '0';
            setTimeout(function() {
                preloader.style.display = 'none';
            }, 500);
        }
    }

    /**
     * Initialize Bootstrap tooltips
     */
    function initializeTooltips() {
        if (tooltipTriggers.length > 0) {
            tooltipTriggers.forEach(function(element) {
                new bootstrap.Tooltip(element);
            });
        }
    }

    /**
     * Auto-hide toast messages after delay
     */
    function initializeToasts() {
        if (toasts.length > 0) {
            toasts.forEach(function(toast) {
                // Create Bootstrap toast instance
                const bsToast = new bootstrap.Toast(toast, {
                    autohide: true,
                    delay: 5000
                });
                
                // Ensure it's shown
                bsToast.show();
            });
        }
    }

    /**
     * Handle navbar color change on scroll
     */
    function handleNavbarScroll() {
        if (navbar) {
            // Initial check
            toggleNavbarClass();
            
            // Listen for scroll events
            window.addEventListener('scroll', toggleNavbarClass);
        }
    }

    /**
     * Toggle navbar class based on scroll position
     */
    function toggleNavbarClass() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    }

    /**
     * Handle back to top button visibility and functionality
     */
    function handleBackToTop() {
        if (backToTop) {
            // Show/hide based on scroll position
            window.addEventListener('scroll', function() {
                if (window.scrollY > 100) {
                    backToTop.classList.add('active');
                } else {
                    backToTop.classList.remove('active');
                }
            });
            
            // Smooth scroll to top when clicked
            backToTop.addEventListener('click', function(e) {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }

    /**
     * Handle password visibility toggle
     */
    function initializePasswordToggle() {
        if (togglePasswordButtons.length > 0) {
            togglePasswordButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    const targetId = this.getAttribute('data-target');
                    const passwordField = document.getElementById(targetId);
                    
                    if (passwordField.type === 'password') {
                        passwordField.type = 'text';
                        this.innerHTML = '<i class="fas fa-eye-slash"></i>';
                    } else {
                        passwordField.type = 'password';
                        this.innerHTML = '<i class="fas fa-eye"></i>';
                    }
                });
            });
        }
    }

    /**
     * Add custom validation to forms
     */
    function initializeFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        if (forms.length > 0) {
            Array.from(forms).forEach(function(form) {
                form.addEventListener('submit', function(event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    
                    form.classList.add('was-validated');
                }, false);
            });
        }
    }

    /**
     * Handle confirmation dialogs
     */
    function initializeConfirmButtons() {
        if (confirmButtons.length > 0) {
            confirmButtons.forEach(function(button) {
                button.addEventListener('click', function(event) {
                    const message = button.getAttribute('data-confirm');
                    if (!window.confirm(message)) {
                        event.preventDefault();
                    }
                });
            });
        }
    }

    /**
     * Handle search form submission
     */
    function handleSearchForm() {
        if (searchForm) {
            searchForm.addEventListener('submit', function(event) {
                // Remove empty fields before submitting to clean up the URL
                const inputs = searchForm.querySelectorAll('input, select');
                inputs.forEach(function(input) {
                    if (input.value === '' || input.value === null) {
                        input.disabled = true;
                    }
                });
            });
        }
    }

    /**
     * Apply hover effects to opportunity cards
     */
    function handleOpportunityCards() {
        if (opportunityCards.length > 0) {
            opportunityCards.forEach(function(card) {
                card.addEventListener('mouseenter', function() {
                    this.classList.add('shadow');
                });
                
                card.addEventListener('mouseleave', function() {
                    this.classList.remove('shadow');
                });
            });
        }
    }

    /**
     * Initialize animated counters with IntersectionObserver
     */
    function initializeCounters() {
        if (animatedCounters.length > 0 && 'IntersectionObserver' in window) {
            const options = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };
            
            const observer = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const counter = entry.target;
                        const target = parseInt(counter.getAttribute('data-target'), 10);
                        let count = 0;
                        const duration = 2000; // 2 seconds
                        const increment = Math.ceil(target / (duration / 16)); // 60fps approx
                        
                        const updateCount = function() {
                            count += increment;
                            if (count >= target) {
                                counter.innerText = target.toLocaleString();
                                return;
                            }
                            counter.innerText = count.toLocaleString();
                            requestAnimationFrame(updateCount);
                        };
                        
                        updateCount();
                        observer.unobserve(counter);
                    }
                });
            }, options);
            
            animatedCounters.forEach(function(counter) {
                observer.observe(counter);
            });
        }
    }

    /**
     * Initialize date and time inputs with custom formatting
     */
    function initializeDateTimeInputs() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        const timeInputs = document.querySelectorAll('input[type="time"]');
        
        // Add placeholders to date inputs
        if (dateInputs.length > 0) {
            dateInputs.forEach(function(input) {
                if (!input.hasAttribute('placeholder')) {
                    input.setAttribute('placeholder', 'YYYY-MM-DD');
                }
            });
        }
        
        // Add placeholders to time inputs
        if (timeInputs.length > 0) {
            timeInputs.forEach(function(input) {
                if (!input.hasAttribute('placeholder')) {
                    input.setAttribute('placeholder', 'HH:MM');
                }
            });
        }
    }

    /**
     * Initialize custom dropdowns
     */
    function initializeDropdowns() {
        const dropdownToggles = document.querySelectorAll('.custom-dropdown-toggle');
        
        if (dropdownToggles.length > 0) {
            dropdownToggles.forEach(function(toggle) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('data-target'));
                    
                    if (target) {
                        if (target.classList.contains('show')) {
                            target.classList.remove('show');
                        } else {
                            // Close all other open dropdowns first
                            document.querySelectorAll('.custom-dropdown-menu.show').forEach(function(menu) {
                                menu.classList.remove('show');
                            });
                            
                            target.classList.add('show');
                        }
                    }
                });
            });
            
            // Close dropdowns when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.custom-dropdown')) {
                    document.querySelectorAll('.custom-dropdown-menu.show').forEach(function(menu) {
                        menu.classList.remove('show');
                    });
                }
            });
        }
    }

})();