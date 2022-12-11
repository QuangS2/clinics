//$("#btn-non-legit").click(function(){
//    console.log("A");
//    $("#tb-non-legit").css("display","none");
//});
function getPatients() { // => list result
    let kw = document.getElementById('kw-rp').value;

    if(!kw) kw = "ALL"
    fetch(`/api/patient/${kw}`, {
        method: "get"
    })
    .then(res => res.json()).then((patients) => {
        console.info(patients)
        let i = 0, len = patients.length;
        e = document.getElementById('search-rs');
        if(len==0){
            e.innerHTML = '<i>Không tìm thầy kết quả</i>' ;
        }
        else
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
            e.innerHTML += `<tr onclick= "testrun(${patients[i].apm_id})">
                <td>${patients[i].user_data.name}</td>
                <td>${patients[i].user_data.birthday}</td>
                <td>${patients[i].user_data.gender}</td>
                <td>${patients[i].user_data.address}</td>
                <td>${patients[i].user_data.CCCD}</td>
                <td>${patients[i].user_data.phone}</td>
            </tr>`

            i++;
        }
    }) // promise
}
function getMedicine(){
    let kw = document.getElementById('kw-medicine').value;
    if (!kw) kw = "ALL"
    fetch(`/api/medicine/${kw}`, {
        method: "get"
    }).then(res => res.json()).then((medicines) => {
//        console.info(medicines)
        let i = 0, len = medicines.length;
        e = document.getElementById('search-rs');

        })
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
function testrun(i){
    console.log(i);
}
function getUserById(user_id){
     fetch(`/api/apm/${apm_id}`, {
        method: "get"
    })
}
