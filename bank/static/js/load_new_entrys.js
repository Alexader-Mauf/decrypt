$(document).ready(function () {
  console.log("loadnewrdy!");

  var ibans = [];
  var offset = 10;
  var limit = 5;
  var newtransfers = "http://127.0.0.1:8000/bank/api/bank-transfers/?ordering=-created_at&offset="+ String(offset) + "&limit=" + String(limit)

  $.getJSON("/bank/api/bank-accounts/", function (data) {
    console.log(data);
    ibans = data.results.map((el) => {
      return el.iban;
    });
    //console.log(ibans);
  });

  //console.log(ibans);




  function round(value, exp) {
     if (typeof exp === 'undefined' || +exp=== 0)
        return Math.round(value);

     value = +value;
     exp = +exp;
     if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0))
        return NaN;

     // Shift
     value = value.toString().split('e');
     value = Math.round(+(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp)));

     //Shift Back
     value = value.toString().split('e');
     return +(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp));
  }

  $(loadnew).click(function () {
    //console.log(offset);
    var newtransfers = "http://127.0.0.1:8000/bank/api/bank-transfers/?ordering=-created_at&offset="+ String(offset) + "&limit=" + String(limit)
    $.getJSON(
      newtransfers,
      function (data) {
        offset = offset + limit
        //console.log(offset);
        // console.log(data);
        var own_iban = $.getJSON(
          "/bank/api/bank-transfers/?ordering=-created_at",
          // die folgende Zeile ist vergleichbar mit: "for el in data.results:"
          data.results.forEach((el) => {
            var row = `
         <li class="list-group-item d-flex justify-content-between lh-sm">
         <div>
         <h6 class="my-0">${String(el.use_case)}</h6>
         <small class="text-muted">Datum der Überweisung: ${dayjs(el.execute_datetime).format('MMM. DD, YYYY, hh:mm a')}</small>
         <br>
         <small class="text-muted">Absender: ${el.iban_from_username}</small>
         <br>
         <small class="text-muted">${el.iban_from} </small>
         <br>
         <small class="text-muted">Empfänger: ${el.iban_to_username}</small>
         <br>
         <small class="text-muted">${el.iban_to}</small>
         <small class="text-muted">Status:</small>`;
            if (el.is_open === false) {
              if (el.is_success === false) {
                row =
                  row +
                  `<small class="text-muted">Fehlgeschlagen</small>
                    <br>
                    <small class="text-muted">log: ${el.executionlog}</small>`;
              } else {
                row = row + `<small class="text-muted">Erfolgreich</small>`;
              }
            } else {
              row = row + `<small class="text-muted">pending</small>`;
            }
         row = row + `</div>`
            if (ibans.includes(el.iban_to)) {
              row = row + `<span class="text-success">+${round(el.amount,2).toFixed(2)}€</span>`;
            } else {
              row = row + `<span class="text-danger">-${round(el.amount,2).toFixed(2)}€</span>`;
            }
            $("#transactions").append(row);
          })
        );
      }
    );
  });
});
