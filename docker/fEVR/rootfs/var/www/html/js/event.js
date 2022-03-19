function replaceInnerHTML(id,text) { document.getElementById(id).innerHTML = text; }
function modalAction(action,id){
    switch(action){
        case "open": modalActionOpen(id); break;
        case "close": modalActionClose(id);
    }
}
function modalActionOpen(id){
    var ua = navigator.userAgent.toLowerCase(); 
    if (ua.indexOf('safari') != -1) { 
        if (ua.indexOf('chrome') > -1) {
            document.getElementById(id).classList.remove('hidden')
            document.getElementById(id).showModal()
        } else {
            document.getElementById(id).classList.remove('hidden')
            document.getElementById(id).style="height: 80vh; width: 90vw; margin-left: 5vw; margin-top: 10vh;"
        }
    }
}
function modalActionClose(id){
    var ua = navigator.userAgent.toLowerCase(); 
    if (ua.indexOf('safari') != -1) { 
        if (ua.indexOf('chrome') > -1) {
            document.getElementById(id).classList.add('hidden')
            document.getElementById(id).close()
        } else {
            document.getElementById(id).classList.add('hidden')
        }
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