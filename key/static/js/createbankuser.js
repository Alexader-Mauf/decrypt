$( document ).ready(function() {
        console.log( "ready!" );

    $( "#login_button" ).click(function() {
            var username = $("#username").val()
            var password = $("#password").val()
            var passwordcheck = $("#password").val()
            var vorname = $("#vorname").val()
            var nachname = $("#name").val()
            var email = $("#email").val()

            $.post( "/bank/api/bank_customers/" , {
             "name": name,
             "vorname":  vorname,
             "email":  email,



             })
            .done(function(data) {
                console.log(data)
                $("#statusmsg").text("Kunde Angelegt:")
                $("#content").text(data.message)
                $("#statusmsg").val("Kunde Angelegt.")
            })
            .fail(function(data) {
                $("#statusmsg").text("Hoppla")
                $("#statusmsg").text("diese Nachricht scheint nicht zu existieren")
            });
            });

});