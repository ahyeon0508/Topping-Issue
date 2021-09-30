// Select main-category
$(document).ready(function () {
    var select = $("select#main-category");
    select.change(function () {
        var select_name = $(this).children("option:selected").text();
        $(this).siblings("label").text(select_name);
    });
});

// Change sub-category
$(document).ready(function () {
    var select = $("select#sub-category");
    select.change(function () {
        var select_name = $(this).children("option:selected").text();
        $(this).siblings("label").text(select_name);
    });
});