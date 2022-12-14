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
//        console.info(patients)
        let i = 0, len = patients.length;
        e = document.getElementById('patients-rs');
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
            e.innerHTML += `<tr onclick= "getReport(${patients[i].apm_id})">
                <td>${patients[i].user_data.name}</td>
                <td>${patients[i].user_data.birthday}</td>
                <td>${patients[i].user_data.gender}</td>
                <td>${patients[i].user_data.address}</td>
                <td>${patients[i].user_data.CCCD}</td>
                <td>${patients[i].user_data.phone}</td>
            </tr>`;

            i++;
        }
    }) // promise
}
function getMedicine(choice){
    data = [];
    let kw = document.getElementById('kw-medicine').value;
    if (!kw) kw = "ALL"
    fetch(`/api/medicines/${kw}`, {
        method: "get"
    }).then(res => res.json()).then((medicines) => {
//        console.info(medicines)
        let i = 0, len = medicines.length;
//        e = document.getElementById('medicine-rs');
        if(len==0){
            document.getElementById('no-rs').style.display = 'block';
            document.getElementById('table-medicine').style.display = "none";
           ;
        }
        else
        {
            data = medicines;
            document.getElementById('no-rs').style.display = 'none';
            document.getElementById('table-medicine').style.display = "table";
            e = document.getElementById('medicine-item');
            e.innerHTML = "";

            while(i<len)
            {
                html = `<tr>
                <td>${medicines[i].name}</td>
                <td>${medicines[i].price} VNĐ</td>
                <td>${medicines[i].unit}</td>`;
                if(choice==1)
                html+=`<td>
                    <button type="button" class="btn btn-success float-end" onclick = "addMedicine(${medicines[i].id})">Thêm vào toa</button>
                    <button type="button" class="btn btn-info float-end">Chi tiết</button>
                </td>`;
                html+=`</tr>`;
                e.innerHTML+=html;
                i++;
            }
        }
        });
}
function getMedicineById(id){
    fetch(`/api/medicine/${id}`, {
        method: "get"
    }).then(res => res.json()).then((medicine) => {
        return medicine;
    });
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
} // yyyy/mm/dd

function getReport(apm_id){
    document.querySelector(".search-area").style.display = "none";
    document.querySelector(".report-area").style.display = "block";
    fetch(`/api/report/${apm_id}`, {
        method: "put"
    }).then(res => res.json()).then((rp) => {
        document.querySelector("#rp-name").innerHTML=`Họ tên: ${rp.patient.name}`;
        document.querySelector("#rp-date").innerHTML=`Ngày khám: ${formatDate(new Date)}`;
        document.querySelector("#hint").innerHTML=`Họ tên: ${rp.patient.name}`;
        document.querySelector(".report-area").value = rp.id;
        i = 0;
        len = rp.prescribes.length;
        while(i<len)
        {
//            console.log(rp);
            htmlMedicineRp(rp.prescribes[i]);
            i++;
        }
    });
}
function createReport(){
   rp_id = document.querySelector(".report-area").value;
   fetch(`/api/report/${rp_id}`, {
        method: "post",
        body: JSON.stringify({
            "rp_id": rp_id,
            "medicine_id":medicine_id
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
}
function getUserById(user_id){
     fetch(`/api/apm/${apm_id}`, {
        method: "get"
    });
}
function addMedicine(medicine_id){
    rp_id = document.querySelector(".report-area").value;
    fetch(`/api/report/add_medicine`, {
        method: "post",
        body: JSON.stringify({
            "rp_id": rp_id,
            "medicine_id":medicine_id
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json()).then((prescribe) => {
        htmlMedicineRp(prescribe);
    });
}
function htmlMedicineRp(prescribe){
    // medicine_id, userManual, amount, id
    e = document.querySelector(`#pr-${prescribe.id}`);
//    console.log(prescribe.id);
    if (e){
//        console.log(prescribe.medicine.id)
        document.querySelector(`#amount-${prescribe.medicine.id}`).value = prescribe.amount
    }
    else{
      e = document.getElementById('add-medicines');
        e.innerHTML +=`
      <tr id="pr-${prescribe.id}">
        <td>${prescribe.medicine.name}</td>
        <td>${prescribe.medicine.unit}</td>
        <td>
            <input type="number" class="form-control" id="amount-${prescribe.medicine.id}" min= 1, value = ${prescribe.amount}>
        </td>
        <td>
            <input type="text" class="form-control" id="use-${prescribe.medicine.id}" value=${prescribe.userManual}>
        </td>
        <td>
            <button type="button" class="btn btn-danger btn-sm" onclick="deletePrescribe(${prescribe.id})"><i class="fas fa-remove"></i></button>
        </td>
      </tr>
      `;
    }

}
function deletePrescribe(prescribe_id){
     if (confirm("Bạn chắc chắn xóa không?") == true){
        fetch(`/api/prescribe/${prescribe_id}`, {
            method: "delete"
        }).then(res => res.json()).then((data) => {
            const e = document.querySelector(`#pr-${prescribe_id}`)
            e.remove();
        });
     }
}
function date_choosen(){
    return new Date (document.getElementById('date_apm').value).toLocaleDateString('en-GB');
}
function set_modal_date(){
    document.getElementById('modal-date').innerHTML  = 'Ngày khám: ' + date_choosen();
}
function testrun(i){
//    console.log(i);
}

