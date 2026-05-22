// Main JavaScript for Resume Screening AI

// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('resumeFile');
    const fileLabel = document.getElementById('fileLabel');
    const fileName = document.getElementById('fileName');
    const jobDescription = document.getElementById('jobDescription');
    const charCount = document.getElementById('charCount');
    
    // Character counter for job description
    if (jobDescription && charCount) {
        jobDescription.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count;
            
            // Change color based on length
            if (count > 1000) {
                charCount.classList.add('text-orange-500');
                charCount.classList.remove('text-gray-500');
            } else {
                charCount.classList.remove('text-orange-500');
                charCount.classList.add('text-gray-500');
            }
        });
        
        // Initial count
        charCount.textContent = jobDescription.value.length;
    }
    
    // File upload area click
    if (uploadArea) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Drag and drop
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('border-indigo-500', 'bg-indigo-50');
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('border-indigo-500', 'bg-indigo-50');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('border-indigo-500', 'bg-indigo-50');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });
    }
    
    // File input change
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                handleFileSelect(this.files[0]);
            }
        });
    }
    
    function handleFileSelect(file) {
        // Validate file type
        if (file.type !== 'application/pdf') {
            showNotification('Please upload a PDF file', 'error');
            fileInput.value = '';
            return;
        }
        
        // Validate file size (5MB = 5 * 1024 * 1024 bytes)
        if (file.size > 5 * 1024 * 1024) {
            showNotification('File size must be less than 5MB', 'error');
            fileInput.value = '';
            return;
        }
        
        // Show selected file name
        if (fileName) {
            fileName.textContent = `✓ Selected: ${file.name}`;
            fileName.classList.remove('hidden');
        }
        
        if (fileLabel) {
            fileLabel.textContent = file.name;
            fileLabel.classList.add('text-indigo-600', 'font-medium');
        }
        
        showNotification('File uploaded successfully!', 'success');
    }
    
    // Form validation
    const analyzeForm = document.querySelector('form');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            const file = fileInput?.files[0];
            const jd = jobDescription?.value.trim();
            
            if (!file) {
                e.preventDefault();
                showNotification('Please upload a CV/resume file', 'error');
                return;
            }
            
            if (!jd) {
                e.preventDefault();
                showNotification('Please enter the job description', 'error');
                return;
            }
            
            if (jd.length < 50) {
                e.preventDefault();
                showNotification('Job description seems too short. Please provide more details for accurate analysis.', 'error');
                return;
            }
            
            // Show loading state
            const submitBtn = analyzeForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.textContent = 'Analyzing... Please wait';
                submitBtn.classList.add('btn-loading');
                submitBtn.disabled = true;
            }
        });
    }
    
    // Notification function
    function showNotification(message, type = 'info') {
        // Check if notification container exists, if not create it
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'fixed top-20 right-4 z-50 space-y-2';
            document.body.appendChild(container);
        }
        
        // Create notification element
        const notification = document.createElement('div');
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500'
        };
        
        notification.className = `${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 opacity-0 translate-x-full`;
        notification.textContent = message;
        
        container.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('opacity-0', 'translate-x-full');
            notification.classList.add('opacity-100', 'translate-x-0');
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('opacity-100', 'translate-x-0');
            notification.classList.add('opacity-0', 'translate-x-full');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Copy results to clipboard (if on result page)
    const copyButton = document.getElementById('copyResults');
    if (copyButton) {
        copyButton.addEventListener('click', function() {
            const results = document.querySelector('.results-content');
            if (results) {
                const text = results.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    showNotification('Results copied to clipboard!', 'success');
                });
            }
        });
    }
});

// Animate score on scroll
const observerOptions = {
    threshold: 0.5
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const scoreElement = entry.target.querySelector('.score-value');
            if (scoreElement) {
                const finalScore = parseInt(scoreElement.dataset.score);
                animateValue(scoreElement, 0, finalScore, 1500);
            }
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            clearInterval(timer);
            current = end;
        }
        element.textContent = Math.round(current);
    }, 16);
}