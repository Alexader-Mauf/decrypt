$( document ).ready(function() {
        console.log( "ready!" );

    $( "#action" ).click(function() {
            var from = $("#iban_from").val()
            var amount = $("#amount").val()
            var to = $("#iban_to").val()
            var created_by = $("#created_by").val()
            var verwendungszweck = $("verwendungszweck").val()

            // der post rewuest muss überarbeited werden um auch die seiion daten mitzugeben -> sonst ist der request nicht authentifiziert -> 403_FORBIDDEN
            // vielleicht mit einem form machen und kein JQuery verwenden?
            $.post( {% 'create-transfers' %} , {
             "iban_from": from,
             "amount":  amount,
             "iban_to":  to,
             "use_case": verwendungszweck,
             "created_by": created_by,
             })
            .done(function(data) {
                console.log(data)
                $("#statusmsg").text("Überweisung Durchgeführt:")
                $("#statusmsg").val("Überweisung erfolgreich.")
            })
            .fail(function(data) {
                $("#statusmsg").val("Hoppla")
                $("#statusmsg").text("da ist wohl etwas schiefgegangen..")
            });
            });
    //there has to be a redirect on success else ppl could accidentaly transfer their stuff like
    // until they literally oom(out of money)
});