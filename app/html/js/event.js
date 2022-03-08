function replaceInnerHTML(id,text) { document.getElementById(id).innerHTML = text; }
function modalAction(action,id){
    target = document.getElementById(id)
    switch(action){
        case "open": target.showModal(); break;
        case "close": target.close();
    }
}
function buttonClick(id,url,target="none",progress="no",referrer=false) {
    var a = document.createElement('a');
    if (target && target != "none"){ a.target=target; }
    if (referrer){ url = url.concat('&referrer=').concat(document.referrer); }
    a.href=url;
    if (id && progress && progress == "yes"){
        modalAction('close',id);
        if (typeof id == 'string' || id instanceof String){
            id = id.concat('-progress');
            modalAction('open',id);
            modalContent = id.concat('-content')
            newModalContent = document.getElementById(modalContent)
            newModalContent.innerHTML.concat("<br/>\n This page will refresh to: ",referrer)
        }
        setTimeout(() => {a.click();},2000);
    }
    else{ a.click(); }
  }

document.onclick = function (e) {
    window.parent.document.getElementById('menu').style = "display: hidden;"
}