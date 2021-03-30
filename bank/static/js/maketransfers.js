$(document).ready(function () {
    var accountValues = {};

  $.get("/bank/api/bank-accounts/", function (data) {
    var accounts = data["results"];
    accounts.forEach(function (item) {
      accountValues[item.iban] = parseFloat(item.balance);
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
  });

  console.log("ready on change scipt");

});

// load iban ausm dict
// kontostand < ueberweisungssumme
// alert ausgeben
