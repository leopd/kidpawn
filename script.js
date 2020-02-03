<script>
$(function() {
    function square_from_class(classes_str) {
        // SVG squares
        var classes_list = classes_str.split(' ');
        for (var i in classes_list) {
            if (classes_list[i].length == 2) {
                return classes_list[i]
            }
        }
    }

    $(".square").on('click', function() {
        var sq = $(this);
        var pos = square_from_class(sq.attr('class'));
        $("#movebox").val( $("#movebox").val() + pos )
    })
})
</script>
