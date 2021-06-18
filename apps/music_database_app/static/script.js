$(document).ready(function(){
    console.log("Script linked")

    $('#messages').delay(2250).fadeOut();

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

        $('#cancel').click(function(){
            console.log("Album edit cancelled");

            $('#album-title').replaceWith(title);
            $('#album-release-date').replaceWith(date);
            $('#new-form-elements').remove();
        });
    });

    if( $('#update-band-form').length ){
        $('#update-band-form').children('label').remove();

        $('#name').removeClass('form-control').addClass('form-control-lg').attr("placeholder", "New band name")
        $('#genre').removeClass('form-select').addClass('form-select-sm');
        $('#founded').removeClass('form-control').addClass('form-control-sm');
        $('#country').removeClass('form-select').addClass('form-select-sm');
        $('#status').removeClass('form-select').addClass('form-select-sm');
    }

    $('#edit-band').click(function(){
        console.log("Trying to edit band")
        
        var band_info = $('#band-info').clone()

        $('span').empty();

        $('h1').children('span').html($('#name'))
        $('p:contains("Genre")').children('span').html($('#genre'))
        $('p:contains("Founded")').children('span').html($('#founded'))
        $('p:contains("Country")').children('span').html($('#country'))
        $('p:contains("Status")').children('span').html($('#status'))

        $('band-info').append('.btn')

        // $('#band-info').replaceWith( $('#update-band').html() )

        // $('#cancel').click(function(){
        //     console.log("Band edit cancelled")
            
        //     $('form').first().replaceWith(band_info)
        // })
    });

});