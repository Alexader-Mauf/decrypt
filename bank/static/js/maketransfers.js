$(document).ready(function () {

  $.get("/bank/api/bank-accounts/", function (data) {

  }).done(function (data) {var accounts = data["results"];
    accounts.forEach(function (item) {
      accountValues[item.iban] = parseFloat(item.balance);
    })
        console.log("Load was performed.");
    };
    )
    .fail(var accountValues = {
    'selectedIban' => null
     };
    var transferValues = parseFloat(0););


  console.log($("#iban_from option:selected").val());$.get("/bank/api/bank-transfers/", function (data) {
    var transfers = data["results"];
    transfers.forEach(function (item) {
      if (item.is_open){
      transferValues += parseFloat(item.amount);
            }
    });
  });
  console.log(accountValues);

  $("id=['id_amount']").keyup(function () {
    //$(".amount").val($("#id_amount").text.replace(",", '.'););
    var selectedIban = $("#id_iban_from option:selected").val();
    var amount = $("#id_amount").val().parseFloat();
    var bankAmount = accountValues[selectedIban].parseFloat();
    var transferAmount = transferValues.parseFloat();

    if (!isNaN(amount) && !isNaN(bankAmount)) {
        if (accountValues[selectedIban] < amount) {
          alert("Eventuell nicht genug Guthaben.");
        }
    }

    if(!isNaN(bankAmount) && !isNaN(transferAmount)) {
        alert("Ihr Kontostand abzüglich offener Überweisungen reicht nicht aus für diese überweisung.");
    }
    else {
      console.error('Fehler beim anlden der Kontoinformationen. accountValues');
    }



  });



  console.log("ready on change scipt");

});

// load iban ausm dict
// kontostand < ueberweisungssumme
// alert ausgeben
