//$( document ).ready(function() {
//        var accountValues = null;
//
//        $.get( "/api/bank-accounts", function( data ) {
//          var accounts = data[""]
//
//          accountValues = {
//          "iban": "kontostand"
//          }
//          alert( "Load was performed." );
//        });
//
//        $.change("amount"){
//            selecetIban = $("#iban_from option:selected").text();
//            if(accountValues[iban]<$("#id_amount").val()){
//                alert("EVTL nicht genug guthaben")
//            };
//            }
//            // load iban ausm dict
//            // kontostand < ueberweisungssumme
//            // alert ausgeben
//});