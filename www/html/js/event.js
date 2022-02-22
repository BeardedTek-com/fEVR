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
function buttonClick(id,url,progress="no",target="none") {
    var a = document.createElement('a');
    if (target != "none"){
        a.target=target;
    }
    a.href=url;
    if (progress == "yes"){
        modalAction('close',id)
        switch (id){
            case "delete":
                modalAction('open','deleting');
                break;
            case "refresh":
                modalAction('open','refreshing');
                break;
        }
        setTimeout(() => {a.click();},2000);

    }
    else{
       a.click(); 
    }
  }