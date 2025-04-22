document.addEventListener('DOMContentLoaded', () => {
    const fadeOutDuration = 500;

    function fadeOutAndNavigate(url) {
        document.body.classList.add('fade-out');
        setTimeout(() => {
            window.location.href = url;
        }, fadeOutDuration);
    }

    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('#') && !link.hasAttribute('target')) {
            link.addEventListener('click', e => {
                e.preventDefault();
                fadeOutAndNavigate(href);
            })
        }
    })

    // document.querySelectorAll('form').forEach(form => {
    //     form.addEventListener('submit', e => {
    //         e.preventDefault();
    //         document.body.classList.add('fade-out');
    //         setTimeout(() => {
    //             form.submit();
    //         }, fadeOutDuration);
    //     })
    // })
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', e => {
            const submitter = e.submitter || form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitter && submitter.classList.contains('get-btn')) {
                // Allow form submission without fade-out animation
                return;
            }
            e.preventDefault();
            document.body.classList.add('fade-out');
            setTimeout(() => {
                form.submit();
            }, fadeOutDuration);
        });
    });
});