function changeClass(el,cls){
    document.getElementById(el).className = cls;
}
function fade(el,targetOpacity){
    e = document.getElementById(el);
    e.style.opacity = targetOpacity;
}
function remove(el){
    e = document.getElementById(el);
    e.remove();
}
async function loadpage(){
    setTimeout(() => fade('loading'),1000);
    setTimeout(() => remove('loading'),2250);
    setTimeout(() => changeClass('container','eventsContainer'),2500);
}

document.onreadystatechange = function () {
    if (document.readyState == "complete"){
        loadpage();
    }
}