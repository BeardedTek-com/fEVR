function replaceInnerHTML(id,text) {
    document.getElementById(id).innerHTML = text
}

function modalAction(action,id){
    target = document.getElementById(id)
    if (action == "open"){
        target.showModal();
    }
    if (action == "close"){
        target.close();
    }
}
/*
function buttonClick(link){
    location.href=link;
}
*/
function buttonClick(url,target="none") {
    var a = document.createElement('a');
    if (target != "none"){
        a.target=target;
    }
    a.href=url;
    a.click();
  }