/**
 * Event Management System - Custom JavaScript
 * Handles sidebar toggle, dark mode, and UI interactions.
 */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- Sidebar Toggle ---------- */
    var sidebar = document.getElementById('sidebar');
    var pageContent = document.getElementById('page-content-wrapper');
    var toggleBtn = document.getElementById('toggle-sidebar');

    if (toggleBtn && sidebar && pageContent) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
            sidebar.classList.toggle('show');
            pageContent.classList.toggle('full-margin');
        });
    }

    /* ---------- Dark Mode Toggle ---------- */
    var darkModeBtn = document.getElementById('darkModeToggle');
    var body = document.body;

    var savedTheme = localStorage.getItem('ems-theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        updateDarkModeIcon(true);
    }

    if (darkModeBtn) {
        darkModeBtn.addEventListener('click', function () {
            body.classList.toggle('dark-mode');
            var isDark = body.classList.contains('dark-mode');
            localStorage.setItem('ems-theme', isDark ? 'dark' : 'light');
            updateDarkModeIcon(isDark);
        });
    }

    function updateDarkModeIcon(isDark) {
        if (!darkModeBtn) return;
        var icon = darkModeBtn.querySelector('i');
        if (icon) {
            icon.className = isDark ? 'bi bi-sun' : 'bi bi-moon';
        }
    }

    /* ---------- Password Toggle ---------- */
    var togglePassword = document.getElementById('togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function () {
            var passwordInput = document.getElementById('password');
            if (passwordInput) {
                var type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                var icon = this.querySelector('i');
                icon.className = type === 'password' ? 'bi bi-eye' : 'bi bi-eye-slash';
            }
        });
    }

    /* ---------- Auto-dismiss Alerts ---------- */
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });

});
