function changeClass(el,cls){
    document.getElementById(el).className = cls;
}
function fade(el,opacity){
    e = document.getElementById(el);
    if (opacity > 0){
        if (el == 'container'){
            e.style.display = "flex";
        }
        else{
            e.style.display = "block";
        }
    }
    e.style.opacity = opacity;
}
function remove(el){
    e = document.getElementById(el);
    e.remove();
}
async function loadpage(){
    setTimeout(() => fade('loading',0),2100);
    setTimeout(() => fade('container',1),3500);
    setTimeout(() => remove('loading'),4000);
    
    // setTimeout(() => changeClass('container','eventsContainer'),4400);
}

document.onreadystatechange = function () {
    if (document.readyState == "complete"){
        loadpage();
    }
}