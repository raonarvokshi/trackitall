"use strict"

document.addEventListener('DOMContentLoaded', function () {
    const productToggle = document.querySelector('.dropdown-submenu > a');

    productToggle.addEventListener('click', function (e) {
        e.preventDefault();
        const submenu = this.nextElementSibling;
        const isShown = submenu.style.display === 'block';

        // Close all open submenus
        const allSubmenus = document.querySelectorAll('.dropdown-submenu .dropdown-menu');
        allSubmenus.forEach(function (menu) {
            menu.style.display = 'none';
        });

        // Toggle the clicked submenu
        submenu.style.display = isShown ? 'none' : 'block';
    });
});


// NAVBAR DROPDOWN ANIMATION
$(document).ready(function () {
    // Kur klikohet në elementin me klasën 'dropdown-toggle'
    $('.dropdown-toggle').click(function () {
        // Kalo nëpër të gjitha elementet në dropdown
        $(this).next('.dropdown-menu').slideToggle();
    });
});

$(document).ready(function () {
    $("#example").DataTable({
        "lengthMenu": [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        colReorder: true,
        stateSave: true,
        language: {
            searchPanes: {
                clearMessage: 'Obliterate Selections',
                collapse: { 0: 'Filters', _: 'Filters (%d)' }
            }
        },
        buttons: [
            {
                extend: "excelHtml5",
                text: "<i class='fa-solid fa-file-excel text-white'></i>",
                titleAttr: "Export To Excel",
                title: "Products",
                className: "excel-btn d-none d-md-inline-block",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6]
                },
            },
            {
                extend: "pdfHtml5",
                text: "<i class='fa-solid fa-file-pdf text-white'></i>",
                titleAttr: "Export To PDF",
                title: "Products",
                className: "pdf-btn d-none d-md-inline-block",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6,]
                },
                // FONT SIZE and optimization
                customize: function (doc) {
                    doc.styles.tableHeader.alignment = "center"; // HEADER POSITION
                    doc.styles.tableBodyOdd.alignment = "center"; // BODY POSITION 1 (grey color)
                    doc.styles.tableBodyEven.alignment = "center"; // BODY POSITION 2 (white color)
                    doc.styles.tableHeader.fontSize = 7; // HEADER FONT SIZE
                    doc.defaultStyle.fontSize = 6; // BODY FONT SIZE
                    // GET THE 100% WIDTH OF THE TABLE
                    doc.content[1].table.widths = Array(doc.content[1].table.body[1].length + 1).join("*").split("");
                    // doc.styles.tableBodyEven.fillColor = "red"; // CHANGE COLOR TO RED 
                    // doc.styles.tableBodyEven.color = "#fff"; // CHANGE COLOR TO RED 
                }
            },
            {
                extend: "print",
                text: "<i class='fa-solid fa-print text-white'></i>",
                titleAttr: "Print",
                title: "Products",
                className: "print-btn d-none d-md-inline-block",
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6,]
                },
            },

            {
                extend: 'colvis',
                text: "Column Visibility",
                titleAttr: "Column Visibility",
                className: "primary-btn d-none d-md-inline-block ms-5",
            },

            {
                extend: 'pageLength',
                className: "primary-btn d-none d-md-inline-block ms-1",
            },
        ],
        layout: {
            topStart: "buttons",
            topEnd: {
                search: {
                    placeholder: "Search here...",
                    text: "",
                }
            },
            top1: {
                searchPanes: {
                    initCollapsed: true
                }
            }
        },
        columnDefs: [
            {
                searchPanes: {
                    show: true,
                    initCollapsed: true
                },
                targets: [0, 1, 2, 3, 4, 5]
            }
        ],
        responsive: {
            details: {
                display: DataTable.Responsive.display.modal({
                    header: function (row) {
                        const data = row.data();
                        return 'Details for ' + data[0] + ' ' + data[1];
                    }
                }),
                renderer: DataTable.Responsive.renderer.tableAll({
                    tableClass: 'table'
                })
            }
        },
    });
});