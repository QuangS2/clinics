//$("#btn-non-legit").click(function(){
//    console.log("A");
//    $("#tb-non-legit").css("display","none");
//});

function ab(){
    console.log("A");
    let elm = document.getElementById('tb-non-legit');
    if(elm.style.display == "none")
        elm.style.display = "table";
    else elm.style.display = "none"
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}
function date_choosen(){
    return new Date (document.getElementById('date_apm').value).toLocaleDateString('en-GB');
}
function set_modal_date(){
    document.getElementById('modal-date').innerHTML  = 'Ngày khám: ' + date_choosen();
}