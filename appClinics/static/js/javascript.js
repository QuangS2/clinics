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