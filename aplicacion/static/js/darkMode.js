document.addEventListener("DOMContentLoaded", () => {
    const darkModeToggle = document.querySelectorAll(".theme-icon");

    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
    }

    darkModeToggle.forEach(element => {
        element.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            enableDarkMode();
            localStorage.setItem('darkMode', 'enabled');
        } else {
            disableDarkMode();
            localStorage.setItem('darkMode', 'disabled');
        }
    });
    })

    function enableDarkMode() {
        document.body.classList.add('dark-mode');
        darkModeToggle.forEach(element => {
            const icon = element.querySelector('i');
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        })

        document.body.style.transition = 'all 0.5s ease-in'

        const nav = document.querySelectorAll(".navbar");
        nav.forEach((nav) => {
            nav.classList.add("dark-mode");
            nav.style.transition = 'all 0.5s ease-in';
        });

        const table = document.querySelectorAll('.table');
        table.forEach((table) => {
            table.classList.add('dark-mode');
            table.style.transition = 'all 0.5s ease-in';

            if (table.classList.contains('border-dark')) {
                table.classList.replace('border-dark', 'border-white');
            }
        })

        const navList = document.querySelectorAll('.nav-list');
        navList.forEach((list) => {
            list.classList.add('dark-mode');
            list.style.transition = 'all 0.5s ease-in';
        });

        const statsCard = document.querySelectorAll('.info-card');
        statsCard.forEach((card) => {
            card.classList.add('dark-mode');
            card.style.transition = 'all 0.5s ease-in';
        });

        const tableHorario = document.querySelectorAll('.table-horario');
        tableHorario.forEach((table) => {
            table.classList.add('dark-mode');
        })

        const modal = document.querySelectorAll('.modal-content');
        modal.forEach(modal => modal.classList.add('dark-mode'));

        const graficosContainer = document.querySelectorAll('.grafico__container');
        graficosContainer.forEach(container => container.classList.add('dark-mode'));
    }

    function disableDarkMode() {
        document.body.classList.remove('dark-mode');
        darkModeToggle.forEach(element => {
            const icon = element.querySelector('i');
            icon.classList.add("fa-moon");
            icon.classList.remove("fa-sun");
        })

        document.body.style.transition = 'all 0.5s ease-out'

        const nav = document.querySelectorAll(".navbar");
        nav.forEach((nav) => {
            nav.classList.remove("dark-mode");
            nav.style.transition = 'all 0.5s ease-out';
        });

        const table = document.querySelectorAll('.table');
        table.forEach((table) => {
            table.classList.remove('dark-mode');
            table.style.transition = 'all 0.5s ease-out';

            if (table.classList.contains('border-white')) {
                table.classList.replace('border-white', 'border-dark');
            }
        })

        const navList = document.querySelectorAll('.nav-list');
        navList.forEach((list) => {
            list.classList.remove('dark-mode');
            list.style.transition = 'all 0.5s ease-out';
        });

        const statsCard = document.querySelectorAll('.info-card');
        statsCard.forEach((card) => {
            card.classList.remove('dark-mode');
            card.style.transition = 'all 0.5s ease-out';
        });

        const tableHorario = document.querySelectorAll('.table-horario');
        tableHorario.forEach((table) => {
            table.classList.remove('dark-mode');
        });

        const modal = document.querySelectorAll('.modal-content');
        modal.forEach(modal => modal.classList.remove('dark-mode'));

        const graficosContainer = document.querySelectorAll('.grafico__container');
        graficosContainer.forEach(container => container.classList.remove('dark-mode'));
    }
});