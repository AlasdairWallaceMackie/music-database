$(document).ready(function(){
    console.log("Script linked")

    $('#messages').delay(2250).fadeOut();

    $('#edit-album').click(function(){
        console.log("Editing album")

        var title = $('#album-title').clone();
        var date = $('#album-release-date').clone();
        
        $('#album-title').replaceWith(
            `<div id="album-title">
                <input class="form-control" type="text" name="title" placeholder="New Album Title">
            </div>`
        )

        $('#album-release-date').replaceWith(
            `<div id="album-release-date">
                <label for="release_date">Change release date:</label>
                <input class="form-control" type="date" name="release_date" id="release_date">
            </div>`
        )

        $('form').append(
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


});