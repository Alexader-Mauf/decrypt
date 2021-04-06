$(document).ready(function () {
    var accountValues = {};
    var transferValues ;
  $.get("/bank/api/bank-accounts/", function (data) {
    var accounts = data["results"];
    accounts.forEach(function (item) {
      accountValues[item.iban] = parseFloat(item.balance);
    });
  });
  $.get("/bank/api/bank-transfers/", function (data) {
    var transfers = data["results"];
    transfers.forEach(function (item) {
      if (item.is_open){
      transferValues += parseFloat(item.amount);
            }
    });
  });
  console.log("Load was performed.");
  console.log($("#iban_from option:selected").val());
  console.log(accountValues);

  $("#id_amount").keyup(function () {
    //$(".amount").val($("#id_amount").text.replace(",", '.'););
    selectedIban = $("#id_iban_from option:selected").val();
    if (accountValues[selectedIban] < $("#id_amount").val()) {
      alert("Eventuell nicht genug Guthaben.");
    }
    if (accountValues[selectedIban] < transferValues {
      alert("Ihr Kontostand abzüglich offener Überweisungen reicht nicht aus für diese überweisung.");
    }

  });



  console.log("ready on change scipt");

});

// load iban ausm dict
// kontostand < ueberweisungssumme
// alert ausgeben
