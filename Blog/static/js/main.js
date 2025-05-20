// Image Slider
const slider = document.querySelector('.slider');
const slides = document.querySelectorAll('.slide');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const dotsContainer = document.querySelector('.slider-dots');

let currentSlide = 0;
let slideInterval;

// Create dots
slides.forEach((_, index) => {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    if (index === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goToSlide(index));
    dotsContainer.appendChild(dot);
});

const dots = document.querySelectorAll('.dot');

function updateSlider() {
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    updateSlider();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    updateSlider();
}

function goToSlide(index) {
    currentSlide = index;
    updateSlider();
    resetInterval();
}

function resetInterval() {
    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000);
}

// Event listeners
prevBtn.addEventListener('click', () => {
    prevSlide();
    resetInterval();
});

nextBtn.addEventListener('click', () => {
    nextSlide();
    resetInterval();
});

// Start automatic sliding
slideInterval = setInterval(nextSlide, 5000);

// Pause slider on hover
slider.addEventListener('mouseenter', () => clearInterval(slideInterval));
slider.addEventListener('mouseleave', () => slideInterval = setInterval(nextSlide, 5000));

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add animation to post cards when they come into view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.post-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s, transform 0.5s';
    observer.observe(card);
});

// Form validation with better UX
const form = document.querySelector('.post-form');
if (form) {
    const inputs = form.querySelectorAll('input, textarea');
    
    inputs.forEach(input => {
        // Add focus styles
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement.classList.remove('focused');
            }
        });
        
        // Validate on input
        input.addEventListener('input', () => {
            validateInput(input);
        });
    });
    
    form.addEventListener('submit', (e) => {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.parentElement.classList.add('shake');
                    setTimeout(() => {
                        input.parentElement.classList.remove('shake');
                    }, 500);
                }
            });
        }
    });
}

function validateInput(input) {
    const value = input.value.trim();
    const parent = input.parentElement;
    
    if (!value) {
        parent.classList.add('error');
        return false;
    }
    
    parent.classList.remove('error');
    return true;
}

// Add loading animation for images
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.post-image').forEach(img => {
        // Add loading class if image hasn't loaded yet
        if (!img.complete) {
            img.classList.add('loading');
        }
        
        // Handle load event
        img.addEventListener('load', function() {
            this.classList.remove('loading');
        });
        
        // Handle error event
        img.addEventListener('error', function() {
            this.src = '/static/images/fallback.jpg';
            this.classList.remove('loading');
            this.classList.add('error');
        });
    });
});

// Add smooth hover effect to social links
document.querySelectorAll('.social-links a').forEach(link => {
    link.addEventListener('mouseenter', () => {
        link.style.transform = 'translateY(-3px)';
    });
    
    link.addEventListener('mouseleave', () => {
        link.style.transform = 'translateY(0)';
    });
});

// Add scroll to top button
const scrollButton = document.createElement('button');
scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
scrollButton.className = 'scroll-top';
scrollButton.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--primary-color);
    color: white;
    border: none;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s, transform 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
`;

document.body.appendChild(scrollButton);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollButton.style.opacity = '1';
        scrollButton.style.transform = 'translateY(0)';
    } else {
        scrollButton.style.opacity = '0';
        scrollButton.style.transform = 'translateY(20px)';
    }
});

scrollButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Image loading
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.classList.add('loading');
        img.onload = function() {
            this.classList.remove('loading');
        }
        img.onerror = function() {
            this.src = '/static/images/fallback.jpg';
            this.classList.remove('loading');
        }
    });

    // Slider functionality
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        slides[index].classList.add('active');
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    // Show first slide
    showSlide(0);

    // Auto advance slides
    setInterval(nextSlide, 5000);

    // Add click handlers for manual navigation
    document.querySelector('.slider-next')?.addEventListener('click', nextSlide);
    document.querySelector('.slider-prev')?.addEventListener('click', () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    });
}); 