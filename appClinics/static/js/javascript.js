//$("#btn-non-legit").click(function(){
//    console.log("A");
//    $("#tb-non-legit").css("display","none");
//});
function getUser() { // => list result
    let kw = document.getElementById('kw-rp').value;

    if(!kw) kw = "ALL"
    fetch(`/api/users/${kw}`, {
        method: "get"
    })
    .then(res => res.json()).then((data) => {
        console.info(data)
        let i = 0, len = data.length;
        e = document.getElementById('search-rs');
        if(len==0){
            e.innerHTML = '<i>Không tìm thầy kết quả</i>' ;
        }else
        {
            e.innerHTML = `<table class="table table-bordered table-hover">
        <thead>
        <tr>
            <!--          <th>#</th>-->
            <th>Tên</th>
            <th>Năm sinh</th>
            <th>Giới tính</th>
            <th>Địa chỉ</th>
            <th>CCCD</th>
            <th>Số điện thoại</th>
        </tr>
        </thead>
        <tbody id="list-patient">

        </tbody>
    </table>`;
        }
        e = document.getElementById('list-patient');

        while(i<len)
        {
            e.innerHTML += `<tr onclick= "testrun()">
                <td>${data[i].name}</td>
                <td>${data[i].birthday}</td>
                <td>${data[i].gender}</td>
                <td>${data[i].address}</td>
                <td>${data[i].CCCD}</td>
                <td>${data[i].phone}</td>
            </tr>`
            i++;
        }
    }) // promise
}

function legitbtn(){
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
function testrun(){
    console.log("run");
}
