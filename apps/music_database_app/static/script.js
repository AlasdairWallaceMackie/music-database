$(document).ready(function(){
    console.log("Script linked")

    $('#messages').delay(1750).fadeOut();

    console.log(window.location.pathname)
    $('nav').find(`a[href="${window.location.pathname}"]`).addClass("active")

    $('.needs-validation').submit(function(event){
        
        if ( !this.checkValidity() ){
            event.preventDefault();
            event.stopPropagation()
        }

        $(this).addClass('was-validated')
    });


    $('#edit-album').click(function(){
        console.log("Editing album")

        var title = $('#album-title').clone();
        var date = $('#album-release-date').clone();
        
        $('#album-title').replaceWith(
            `<div id="album-title">
                <input class="form-control-lg" type="text" name="title" placeholder="New Album Title">
            </div>`
        )

        $('#album-release-date').replaceWith(
            `<div id="album-release-date">
                <label for="release_date">Change release date:</label>
                <input class="form-control" type="date" name="release_date" id="release_date">
            </div>`
        )

        $('#update-album-form').append(
            `<div id="new-form-elements">
                <br>
                <label for="cover_art">Upload new cover art:</label>
                <input class="form-control" type="file" name="cover_art" id="cover_art">
                <br>
                <button class="btn btn-warning" type="submit">Submit Changes</button>
                <button id="cancel" class="btn btn-secondary" type="button">Cancel</button>
            </div>`
        )

        $('.dropdown-toggle').prop("disabled", true)

        $('#cancel').click(function(){
            console.log("Album edit cancelled");

            $('#album-title').replaceWith(title);
            $('#album-release-date').replaceWith(date);
            $('#new-form-elements').remove();
            $('.dropdown-toggle').prop("disabled", false)
        });
    });

    
    if( $('#update-band').length ){ //if #update-band exists
        $('#update-band').children('label').remove();

        $('#name').removeClass('form-control').addClass('form-control-lg').attr("placeholder", "Change band name")
        $('#genre').removeClass('form-select').addClass('form-select-sm');
        $('#founded').removeClass('form-control').addClass('form-control-sm');
        $('#country-field').removeClass('form-select').addClass('form-select-sm');
        $('#status').removeClass('form-select').addClass('form-select-sm');
    }


    $('#edit-band').click(function(){
        console.log("Trying to edit band")
        
        var band_info = $('#band-info').clone()
        var update_band = $('#update-band').clone()

        var name = $('#band-name').text()
        var genre = $('p:contains("Genre")').children('span').text()
        var founded = $('p:contains("Founded")').children('span').text()
        var country = $('p:contains("Country:")').children('span').text()
        var status = $('p:contains("Status")').children('span').text()

        $('span').empty();
        $(`[selected|=true]`).remove()

        $('#band-name').children('span').html($('#name'))
            $('#band-name').find('input').val(name)

        $('p:contains("Genre")').children('span').html($('#genre'))
            $(`[value|=${genre}]`).attr("selected", true)
            
        $('p:contains("Founded")').children('span').html($('#founded'))
            $('p:contains("Founded")').find('input').val(founded)

        $('p:contains("Country:")').children('span').html($('#country-field'))
            $(`option:contains(${country})`).attr("selected", true)

        $('p:contains("Status")').children('span').html($('#status'))
            $(`option:contains(${status})`).attr("selected", true)

        $('#band-actions-button').hide()

        $('#update-band-form').append( $('#button-group') )

        $('#cancel').click(function(){
            console.log("Cancelling band edit")
            $('#band-info').replaceWith( band_info )
            $('#update-band').replaceWith( update_band )
            $('#band-actions-button').show()
        });
    });


    $('.rating-star').hover(function(){ //Hover in
        var hovered_value = $(this).attr('value')

        //Empty stars
        $('.rating-star').each(function(){
                $(this).removeClass('bi-star-fill').addClass('bi-star')
        });

        //Fill all stars up to and including the hovered star
        $('.rating-star').each(function(){
            if ( parseInt( $(this).attr("value") ) <= hovered_value)
                $(this).removeClass('bi-star').addClass('bi-star-fill')
        });
    },
    function(){ //Hover out        
        emptyStars()
        
        $('.rating-star').each(function(){
            var current_rating = $('#rating').val()
            var this_star_rating = $(this).attr('value')

            if( this_star_rating <= current_rating)
                $(this).removeClass('bi-star').addClass('bi-star-fill')
        });
    });

    $('.rating-star').mousedown(function(){
        new_value = $(this).attr('value')
        $('#rating').val(new_value)
        console.log("User rating changed to: " + new_value)

        $('#submit-rating').attr("disabled", false)

        //Darkening effect feedback when clicked
        $(this).parent().children('.bi-star-fill').css("color", "#AB631E")
    });
    $('.rating-star').mouseup(function(){
        console.log("Mouseup")
        $('.rating-star').each(function(){
            $(this).css("color","")
        });
    });

    $('#cancel-rating').click(function(){
        $('#rating').val("0");
        emptyStars();
    })

    function emptyStars(){
        $('.rating-star').each(function(){
            $(this).removeClass('bi-star-fill').addClass('bi-star')
        });
    }
    function fillStars(){
        $('.rating-star').each(function(){
            $(this).removeClass('bi-star').addClass('bi-star-fill')
        });
    }

    if ($('#user-rating').length){ //if #user_rating exists
        if ($('#user-rating').attr("value") == 0)
            $('#user-rating').empty().append(`<p class="text-success">Rate this album</p>`)
        else{
            for (var i=1; i<=5; i++){
            if ( i <= $('#user-rating').attr("value") )
                $('#user-rating').append( `<i class="bi-star-fill"></i>` )
            else
            $('#user-rating').append( `<i class="bi-star"></i>` )
            }
        }
    }




});