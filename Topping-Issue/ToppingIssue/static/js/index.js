// Select category
$(document).ready(function () {
    // main-category
    $("select#main-category").change(function () {
        var main_category = $(this).children("option:selected").text();
        $(this).siblings("label").text(main_category);

    // sub-category
        $.ajax({
            type: 'GET',
            url: '/categoryData',
            dataType: 'json',
            success: function(data){
                for (var key in data) {
                    if (main_category == key){
                        $("select#sub-category").find('option').remove();
                        $("select#sub-category").append('<option hidden></option>');
                        for (var i = 0; i < data[key].length; i++){
                            $("select#sub-category").append('<option value="'+ data[key][i][1] + '">' + data[key][i][0] + '</option>');
                        }
                        break;
                    }
                }
            }
        })

        $("select#sub-category").change(function () {
            var sub_category = $(this).children("option:selected").text();
            $(this).siblings("label").text(sub_category);
        });
    });
});