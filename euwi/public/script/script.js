$(function() {

    $(document).on("click", '.searchCardInput img', function(e) {

        let query = $('.searchCardInput input').val();

        if(query) {

            window.location = window.location.origin + "/search/" + query;

        }

    });

    $(".searchCardInput input").on("keypress", function(e){

        if(e.which == 13){

            let query = $('.searchCardInput input').val();

            if(query) {

                window.location = window.location.origin + "/search/" + query;

            }

        }

    });

});