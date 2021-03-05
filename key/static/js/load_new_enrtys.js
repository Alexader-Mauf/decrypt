$( document ).ready(function() {
        console.log( "ready!" );

    $( "#loadnew" ).click(function() {


            $.get( "/bank/api/bank-transfers/" , {

             })
            .done(function(data) {
                console.log(data)
                $("#statusmsg").text("Kunde Angelegt:")
                $("#statusmsg").val("Kunde Angelegt.")
            })
            // was ist die id der Felder?
            // die Felder werden genereiert für
            .fail(function(data) {
                $("#statusmsg").val("Hoppla")
                $("#statusmsg").text("diese Nachricht scheint nicht zu existieren")
            });
            });

});

