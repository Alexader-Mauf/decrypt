$(document).ready(function () {
  function isValidIBANNumber(input) {
    var CODE_LENGTHS = {
        AD: 24, AE: 23, AT: 20, AZ: 28, BA: 20, BE: 16, BG: 22, BH: 22, BR: 29,
        CH: 21, CR: 21, CY: 28, CZ: 24, DE: 22, DK: 18, DO: 28, EE: 20, ES: 24,
        FI: 18, FO: 18, FR: 27, GB: 22, GI: 23, GL: 18, GR: 27, GT: 28, HR: 21,
        HU: 28, IE: 22, IL: 23, IS: 26, IT: 27, JO: 30, KW: 30, KZ: 20, LB: 28,
        LI: 21, LT: 20, LU: 20, LV: 21, MC: 27, MD: 24, ME: 22, MK: 19, MR: 27,
        MT: 31, MU: 30, NL: 18, NO: 15, PK: 24, PL: 28, PS: 29, PT: 25, QA: 29,
        RO: 24, RS: 22, SA: 24, SE: 24, SI: 19, SK: 24, SM: 27, TN: 24, TR: 26,   
        AL: 28, BY: 28, CR: 22, EG: 29, GE: 22, IQ: 23, LC: 32, SC: 31, ST: 25,
        SV: 28, TL: 23, UA: 29, VA: 22, VG: 24, XK: 20
    };
    var iban = String(input).toUpperCase().replace(/[^A-Z0-9]/g, ''), // keep only alphanumeric characters
            code = iban.match(/^([A-Z]{2})(\d{2})([A-Z\d]+)$/), // match and capture (1) the country code, (2) the check digits, and (3) the rest
            digits;
    // check syntax and length
    if (!code || iban.length !== CODE_LENGTHS[code[1]]) {
        return false;
    }
    // rearrange country code and check digits, and convert chars to ints
    digits = (code[3] + code[1] + code[2]).replace(/[A-Z]/g, function (letter) {
        return letter.charCodeAt(0) - 55;
    });
    // final check
    return mod97(digits);
  }

  function mod97(string) {
    var checksum = string.slice(0, 2), fragment;
    for (var offset = 2; offset < string.length; offset += 7) {
        fragment = String(checksum) + string.substring(offset, offset + 7);
        checksum = parseInt(fragment, 10) % 97;
    }
    return(checksum);
  }

  var accountValues = {};
  var transferValues = 0.0;

  // Laden der Bankaccounts + parsen Kontostand
  $.get("/bank/api/bank-accounts/")
    .done(function (data) {
      var accounts = data["results"];

      console.log(accounts);
      accounts.forEach(function (item) {
        accountValues[item.iban] = parseFloat(item.balance);
      });
    })
    .fail(function () {
      alert("Kein Konto gefunden.");
      accountValues = {
        selectedIban: null,
      };
    });


  // noch offenen Transaktionen die kommen können anrechnen
  $.get("/bank/api/bank-transfers/")
    .done(
        function (data) {
            var transfers = data["results"];
            transfers.forEach(function (item) {
                if (item.is_open == true) {
                    console.log("true", item.iban_to, $("#id_iban_from option:selected").val() )
                    if (item.iban_to == $('#id_iban_from').val()) {
                        transferValues = transferValues - parseFloat(item.amount);
                    }
                    if (item.iban_from == $('#id_iban_from').val()) {
                        transferValues = transferValues + parseFloat(item.amount);
                    }
                }
            });
        })
    .fail(function () {
            alert('kein anladen möglich')
    });


  console.log(accountValues);


  $('#id_amount').on("keyup" ,function () {
    var selectedIban = $("#id_iban_from option:selected").val();
    var todoAmount = parseFloat($("#id_amount").val());
    var selectedAccountAmount = parseFloat(accountValues[selectedIban]);
    var opentransferAmount = parseFloat(transferValues);


    $('#id_amount').removeClass('error');
    $('#id_amount').removeClass('correct');
    if (isNaN(todoAmount)){
      $("#id_amount").addClass('error');
      alert("bitte eine Zahl eingeben");

    }

    if (!isNaN(todoAmount) && !isNaN(selectedAccountAmount)) {
      if (selectedAccountAmount < todoAmount) {
        $('#id_amount').addClass('error');
        alert("Eventuell nicht genug Guthaben.");
        return
        }
    }

    if (!isNaN(selectedAccountAmount) && !isNaN(opentransferAmount) && !isNaN(todoAmount)) {
      if (selectedAccountAmount<(opentransferAmount+todoAmount)) {
        $("#id_amount").addClass('error');
        alert(
          "Ihr Kontostand abzüglich offener Überweisungen reicht nicht aus für diese überweisung."
        );
        return
      }
    } else {
      console.error(
        "Fehler beim anladen der Kontoinformationen. accountValues"
      );
    }
    if (selectedAccountAmount>todoAmount){
        $("#id_amount").addClass('correct');
    }
  });

  $("#id_iban_to").on('focusout', function () {
    var iban_to = $("#id_iban_to").val();
    if (isValidIBANNumber(iban_to)!=1){
      $('#id_iban_to').removeClass('correct');
      $('#id_iban_to').addClass('warning');
      return
    }
    $('#id_iban_to').removeClass('warning');
    if (isValidIBANNumber(iban_to)==1){
      $('#id_iban_to').addClass('correct');
    }
  });

  $("#id_verwendungszweck").on("change keyup",function(){
    if($(this).val().length == 0 ){
      $('#id_verwendungszweck').removeClass('correct');
      $('#id_verwendungszweck').addClass('error');
      console.log("its 0")      
    }
    console.log(($(this).val()));
    console.log($(this).val().length);
    if ($(this).val().length > 0){
      $('#id_verwendungszweck').removeClass('error');
      $('#id_verwendungszweck').addClass('correct');
    }
  })

  console.log("ready on change scipt");
});
