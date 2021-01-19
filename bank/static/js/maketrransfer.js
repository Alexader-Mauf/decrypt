$( document ).ready(function() {
        console.log( "ready!" );

    $( "#action" ).click(function() {
            var from = $("#iban_from").val()
            var amount = $("#amount").val()
            var to = $("#iban_to").val()


            $.post( "/bank/api/bank_transfers/" , {
             "iban_from": from,
             "amount":  amount,
             "iban_to":  to,



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

});