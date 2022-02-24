function replaceInnerHTML(id,text) { document.getElementById(id).innerHTML = text; }
function modalAction(action,id){
    target = document.getElementById(id)
    switch(action){
        case "open": target.showModal(); break;
        case "close": target.showModal();
    }
}
function buttonClick(id,url,target="none",progress="no",referrer) {
    var a = document.createElement('a');
    if (target || target != "none"){ a.target=target; }
    if (referrer){ a.href=referrer; } else { a.href=url; }
    if (id || progress || progress == "yes"){
        modalAction('close',id);
        if (typeof id == 'string' || id instanceof String){
            id = id.concat('-refresh');
            modalAction('open',id);
        }
        setTimeout(() => {a.click();},2000);
    }
    else{ a.click(); }
  }