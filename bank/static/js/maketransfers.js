$( document ).ready(function() {
        var accountValues = null;

        $.get( "/bank/api/bank-accounts/", function( data ) {
          var accounts = data[""];

          accountValues = {
          "iban": "kontostand"
          }
          console.log( "Load was performed." );
          console.log($("#iban_from option:selected").text());
        });


            // load iban ausm dict
            // kontostand < ueberweisungssumme
            // alert ausgeben
});
$("amount").change(console.log("spam "))


$("amount").change(function(){
    selecetIban = $("#iban_from option:selected").text();
    console.log("change");
    if(accountValues[selecetIban]<$("#id_amount").val()){
        alert("EVTL nicht genug guthaben")
    };
    });