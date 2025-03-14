/**
 * Интерактивность для древовидной структуры отделов
 */
document.addEventListener('DOMContentLoaded', function() {
    // Функционал для сворачивания/разворачивания дерева
    const toggles = document.querySelectorAll('.toggle-icon');

    toggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const departmentId = this.getAttribute('data-department');
            const subDepartments = document.querySelector(`.subdepartments-${departmentId}`);
            const icon = this.querySelector('i');

            if (subDepartments.classList.contains('collapsed')) {
                subDepartments.classList.remove('collapsed');
                icon.classList.remove('bi-plus-square');
                icon.classList.add('bi-dash-square');
            } else {
                subDepartments.classList.add('collapsed');
                icon.classList.remove('bi-dash-square');
                icon.classList.add('bi-plus-square');
            }
        });
    });
});