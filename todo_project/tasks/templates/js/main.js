// Custom JavaScript for the to-do list app

   document.addEventListener('DOMContentLoaded', function() {
       // Add smooth scrolling
       document.querySelectorAll('a[href^="#"]').forEach(anchor => {
           anchor.addEventListener('click', function (e) {
               e.preventDefault();
               const target = document.querySelector(this.getAttribute('href'));
               if (target) {
                   target.scrollIntoView({ behavior: 'smooth' });
               }
           });
       });

       // Add animation to newly added tasks
       const listItems = document.querySelectorAll('.list-group-item');
       listItems.forEach((item, index) => {
           item.style.opacity = '0';
           item.style.transform = 'translateY(20px)';
           setTimeout(() => {
               item.style.transition = 'all 0.3s ease';
               item.style.opacity = '1';
               item.style.transform = 'translateY(0)';
           }, index * 50);
       });

       // Confirm before deleting
       const deleteLinks = document.querySelectorAll('a[href*="delete"]');
       deleteLinks.forEach(link => {
           if (!link.closest('form')) {  // Don't add to form submit buttons
               link.addEventListener('click', function(e) {
                   if (!confirm('Are you sure you want to delete this task?')) {
                       e.preventDefault();
                   }
               });
           }
       });

       // Form validation feedback
       const forms = document.querySelectorAll('form');
       forms.forEach(form => {
           form.addEventListener('submit', function(e) {
               const titleInput = form.querySelector('input[name="title"]');
               if (titleInput && !titleInput.value.trim()) {
                   e.preventDefault();
                   titleInput.classList.add('is-invalid');
                   alert('Please enter a task title');
               }
           });
       });
   });