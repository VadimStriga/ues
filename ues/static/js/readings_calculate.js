let main = document.tr.add_readings;
let field = main.elements;
main.addEventListener('input', function(e) {
  if (e.target !== e.currentTarget) {
    var input = document.getElementById("id_readings");
    var row = input.parentNode.parentNode;
    var rowArray = Array.from(row.querySelectorAll('[type=hidden]'));
    rowArray.forEach(function(cel, idx) {
      const base = cel.value;
      let output = cel.nextElementSibling;
      let val = parseFloat(input.value) - parseFloat(base);
      output.value = val;
    });
    field.amount.value = Number(field.dr.value) * Number(field.tc.value);
    field.result_amount.value = Number(field.amount.value) - Number(field.deduction.value) + (Number(field.amount.value) - Number(field.deduction.value))/100*Number(field.losses.value) + Number(field.constant_losses.value);
    
    let resultAmount = Number(field.result_amount.value);
    let tariff1 = Number(field.tariff1.value);
    let tariff2 = Number(field.tariff2.value);
    let tariff3 = Number(field.tariff3.value);
    let margin = Number(field.margin.value);
    if(resultAmount <= 10980) {
      accrued = ((tariff1 + margin) * resultAmount);
    } else if(resultAmount <= 14640) {
      accrued = (((tariff1 + margin) * 10980) + ((tariff2 + margin) * (resultAmount - 10980)));
    } else accrued = (((tariff1 + margin) * 10980) + ((tariff2 + margin) * 3660) + ((tariff3 + margin) * (resultAmount - 14640)));

    field.accrued.value = accrued.toFixed(2);
    field.accrued_NDS.value = (Number(field.accrued.value) * 1.2).toFixed(2);
  }
});