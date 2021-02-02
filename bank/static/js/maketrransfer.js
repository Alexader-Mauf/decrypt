$( document ).ready(function() {
        console.log( "ready!" );

    $( "#action" ).click(function() {
            var from = $("#iban_from").val()
            var amount = $("#amount").val()
            var to = $("#iban_to").val()


            $.post( "/bank/api/bank-transfers/" , {
             "iban_from": from,
             "amount":  amount,
             "iban_to":  to,
    // this is wrong but it is also wrong in the test since I am struggeling to find
    // the correct syntax


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