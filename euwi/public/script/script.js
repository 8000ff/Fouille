$(function() {

    $(document).on("click", '.searchCard .searchCardInput img', function(e) {

        let query = $('.searchCard .searchCardInput input').val();

        if(query) {

            window.location.href = "search/" + query;

        }

    });

    $("div.searchCardInput input").on("keypress", function(e){

        if(e.which == 13){

            let query = $('.searchCard .searchCardInput input').val();

            if(query) {

                window.location.href = "search/" + query;

            }

        }

    });

});