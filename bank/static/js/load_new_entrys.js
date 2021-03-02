$(document).ready(function () {
  console.log("loadnewrdy!");

  var ibans = [];
  var offset = 0;
  var limit = 5;
  var newtransfers =
    "/bank/api/bank-transfers/?ordering=-created_at&offset=" +
    String(offset) +
    "&limit=" +
    String(limit);
  var count = $.getJSON("/bank/api/bank-transfers/", function (data) {
    count = data.count;
  });

  //console.log(ibans);

  $.getJSON("/bank/api/bank-accounts/", function (data) {
    console.log(data);
    ibans = data.results.map((el) => {
      return el.iban;
    });
    //console.log(ibans);
  });

  //console.log(ibans);

  $(loadnew).hide();

  function buildurl(offset,limit){
        return("/bank/api/bank-transfers/?ordering=-created_at&offset=" +
      String(offset) +
      "&limit=" +
      String(limit))
  }

  function showtransfers(data){
        $("#transactions").empty();
      // die folgende Zeile ist vergleichbar mit: "for el in data.results:"
      data.results.forEach((el) => {
        var row = `
            <li class="list-group-item d-flex justify-content-between lh-sm">
            <div>
            <h6 class="my-0">${String(el.use_case)}</h6>
            <small class="text-muted">Datum der Überweisung: ${dayjs(
              el.execute_datetime
            ).format("MMM. DD, YYYY, hh:mm a")}</small>
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
              `<small class="text-danger">Fehlgeschlagen</small>
                       <br>
                       <small class="text-muted">log: ${el.executionlog}</small>`;
          } else {
            row = row + `<small class="text-success">Erfolgreich</small>`;
          }
        } else {
          row = row + `<small class="text-muted">pending</small>`;
        }
        row = row + `</div>`;
  }

  function round(value, exp) {
    if (typeof exp === "undefined" || +exp === 0) return Math.round(value);

    value = +value;
    exp = +exp;
    if (isNaN(value) || !(typeof exp === "number" && exp % 1 === 0)) return NaN;

    // Shift
    value = value.toString().split("e");
    value = Math.round(+(value[0] + "e" + (value[1] ? +value[1] + exp : exp)));

    //Shift Back
    value = value.toString().split("e");
    return +(value[0] + "e" + (value[1] ? +value[1] - exp : -exp));
  }

  $(loadnew).click(function () {
    offset = offset - limit;
    console.log(offset);
    newtransfers = buildurl(offset,limit);
    $.getJSON(newtransfers, function (data) {
      // Hier muss ein check hin ob es noch ergebnisse gibt
      console.log(data);

      $("#transactions").empty();
      // die folgende Zeile ist vergleichbar mit: "for el in data.results:"
      data.results.forEach((el) => {
        var row = `
         <li class="list-group-item d-flex justify-content-between lh-sm">
         <div>
         <h6 class="my-0">${String(el.use_case)}</h6>
         <small class="text-muted">Datum der Überweisung: ${dayjs(
           el.execute_datetime
         ).format("MMM. DD, YYYY, hh:mm a")}</small>
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
              `<small class="text-danger">Fehlgeschlagen</small>
                    <br>
                    <small class="text-muted">log: ${el.executionlog}</small>`;
          } else {
            row = row + `<small class="text-success">Erfolgreich</small>`;
          }
        } else {
          row = row + `<small class="text-muted">pending</small>`;
        }
        row = row + `</div>`;
        if (ibans.includes(el.iban_to)) {
          row =
            row +
            `<span class="text-success">+${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        } else {
          row =
            row +
            `<span class="text-danger">-${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        }
        $("#transactions").append(row);
      });
      if (data.previous === null) {
        //  button ausgrauen
        $(loadnew).hide();
      }

      if (data.next != null) {
        $(loadolder).show();
      }
    });
  });

  $(loadolder).click(function () {
    offset = offset + limit;
    console.log(offset);
    newtransfers = buildurl(offset,limit);
    $.getJSON(newtransfers, function (data) {
      console.log(data);
      console.log(data.next);

      $("#transactions").empty();
      // die folgende Zeile ist vergleichbar mit: "for el in data.results:"
      data.results.forEach((el) => {
        var row = `
            <li class="list-group-item d-flex justify-content-between lh-sm">
            <div>
            <h6 class="my-0">${String(el.use_case)}</h6>
            <small class="text-muted">Datum der Überweisung: ${dayjs(
              el.execute_datetime
            ).format("MMM. DD, YYYY, hh:mm a")}</small>
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
              `<small class="text-danger">Fehlgeschlagen</small>
                       <br>
                       <small class="text-muted">log: ${el.executionlog}</small>`;
          } else {
            row = row + `<small class="text-success">Erfolgreich</small>`;
          }
        } else {
          row = row + `<small class="text-muted">pending</small>`;
        }
        row = row + `</div>`;
        if (ibans.includes(el.iban_to)) {
          row =
            row +
            `<span class="text-success">+${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        } else {
          row =
            row +
            `<span class="text-danger">-${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        }
        $("#transactions").append(row);
      });

      if (data.next === null) {
        //  button ausgrauen
        $(loadolder).hide();
      }

      if (data.previous != null) {
        $(loadnew).show();
      }
    });
  });

  $(buttonfirst).click(function () {
    offset = 0;
    newtransfers = buildurl(offset,limit);
    $.getJSON(newtransfers, function (data) {
      $("#transactions").empty();
      // die folgende Zeile ist vergleichbar mit: "for el in data.results:"
      data.results.forEach((el) => {
        var row = `
            <li class="list-group-item d-flex justify-content-between lh-sm">
            <div>
            <h6 class="my-0">${String(el.use_case)}</h6>
            <small class="text-muted">Datum der Überweisung: ${dayjs(
              el.execute_datetime
            ).format("MMM. DD, YYYY, hh:mm a")}</small>
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
              `<small class="text-danger">Fehlgeschlagen</small>
                       <br>
                       <small class="text-muted">log: ${el.executionlog}</small>`;
          } else {
            row = row + `<small class="text-success">Erfolgreich</small>`;
          }
        } else {
          row = row + `<small class="text-muted">pending</small>`;
        }
        row = row + `</div>`;
        if (ibans.includes(el.iban_to)) {
          row =
            row +
            `<span class="text-success">+${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        } else {
          row =
            row +
            `<span class="text-danger">-${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        }
        $("#transactions").append(row);
      });

      if (data.next != null) {
        //  button ausgrauen
        $(loadolder).show();
      }

      if (data.previous === null) {
        $(loadnew).hide();
      }
    });
  });

  $(buttonlast).click(function () {
    // offset muss gleich von count - (der rest von  count / limit) sein
    offset = 42 - (count % limit);

    newtransfers = buildurl(offset,limit);
    $.getJSON(newtransfers, function (data) {
      $("#transactions").empty();
      // die folgende Zeile ist vergleichbar mit: "for el in data.results:"
      data.results.forEach((el) => {
        var row = `
            <li class="list-group-item d-flex justify-content-between lh-sm">
            <div>
            <h6 class="my-0">${String(el.use_case)}</h6>
            <small class="text-muted">Datum der Überweisung: ${dayjs(
              el.execute_datetime
            ).format("MMM. DD, YYYY, hh:mm a")}</small>
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
              `<small class="text-danger">Fehlgeschlagen</small>
                       <br>
                       <small class="text-muted">log: ${el.executionlog}</small>`;
          } else {
            row = row + `<small class="text-success">Erfolgreich</small>`;
          }
        } else {
          row = row + `<small class="text-muted">pending</small>`;
        }
        row = row + `</div>`;
        if (ibans.includes(el.iban_to)) {
          row =
            row +
            `<span class="text-success">+${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        } else {
          row =
            row +
            `<span class="text-danger">-${round(el.amount, 2).toFixed(
              2
            )}€</span>`;
        }
        $("#transactions").append(row);
      });

      if (data.next === null) {
        //  button ausgrauen
        $(loadolder).hide();
      }

      if (data.previous != null) {
        $(loadnew).show();
      }
    });
  });
});
