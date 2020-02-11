<script>
// Simple jquery program so that when you click a square,
// it puts the name of the square in the "movebox" input field.
$(function() {
    function square_from_class(classes_str) {
        // This takes a list of classes for an SVG square like
        // "square light g2" and parses out just "g2"
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
