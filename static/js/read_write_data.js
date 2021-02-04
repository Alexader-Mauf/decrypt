$( document ).ready(function() {
        console.log( "ready!" );

    $( "#decode" ).click(function() {
            var messageText = $("#message").val()
            $.getJSON( "/key/api/secret-msgs/"+messageText+"/" )
            .done(function(data) {
                console.log(data)
                $("#status-message").text("Deine Nachricht ist:")
                $("#content").text(data.message)
                $("#message").val("")
            })
            .fail(function(data) {
                $("#status-message").text("Hoppla")
                $("#content").text("diese Nachricht scheint nicht zu existieren")
            });
            });

    $( "#encode" ).click(function() {
        var messagText = $("#message").val()
        $.post( "/key/api/secret-msgs/" , { "message": messagText })
         .done(function( data ) {
            console.log( data );
            $("#content").text(data.uuid)
            $("#status-message").text("Erfolgreich gespeichert unter:")
            $("#message").val("")
         })
         .fail(function(data) {
                $("#status-message").text("Hoppla")
                $("#content").text("da ist wohl etwas schiefgegangen")
         })
         })

});