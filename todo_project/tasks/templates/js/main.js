document.addEventListener('DOMContentLoaded', () => {

    /* -----------------------------
       Smooth scrolling (anchors)
    ----------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', e => {
            const targetId = link.getAttribute('href');
            const targetEl = document.querySelector(targetId);

            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    /* -----------------------------
       List item fade-in animation
    ----------------------------- */
    const items = document.querySelectorAll('.list-group-item');

    items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(12px)';

        setTimeout(() => {
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 60);
    });

    /* -----------------------------
       Delete confirmation
    ----------------------------- */
    document.querySelectorAll('a[data-delete]').forEach(link => {
        link.addEventListener('click', e => {
            const confirmed = confirm('Are you sure you want to delete this task?');
            if (!confirmed) e.preventDefault();
        });
    });

    /* -----------------------------
       Simple form validation
    ----------------------------- */
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', e => {
            const titleInput = form.querySelector('input[name="title"]');

            if (titleInput && !titleInput.value.trim()) {
                e.preventDefault();
                titleInput.classList.add('is-invalid');
                titleInput.focus();
            }
        });
    });

});
