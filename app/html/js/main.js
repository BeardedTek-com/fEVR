const divInstall = document.getElementById('installContainer');
const butInstall = document.getElementById('butInstall');


function hideElement(target,targetClass){
    target.style.transition = "width 1s ease, height 500ms ease"
    target.style.width= 0;
    target.style.height = "0%";
    setTimeout(() => { target.classList.remove(targetClass); }, 500);
}

function slideElement(target,targetClass){

    target.style.transition = "width 500ms ease, height 500ms ease"
    target.style.width = "100px"
    target.classList.add(targetClass);
    target.style.width = target.scrollWidth+"px";
    target.style.height = "auto";
}

function toggleMenu(menuId){
    target = document.getElementById(menuId)
    if (target.style.width == 0 || target.style.width == "0px"){
        slideElement(target,'menuBorder');
    } else {
        hideElement(target,'menuBorder');
    }
}
function clickItem(menuItem){
    document.getElementById('subtitle').innerHTML = titleCase(" ".concat(menuItem.replace('menu_','').replace('_',' ')));
    toggleMenu("menuContainer",750);
}
function titleCase(str) {
    str = str.toLowerCase().split(' ');
    for (var i = 0; i < str.length; i++) {
      str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1); 
    }
    return str.join(' ');
}
function disableBackBtn(){
    window.history.pushState(null, null, window.location.href);
    window.onpopstate = function () {
        window.history.go(1);
    };
}

disableBackBtn()

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/js/service-worker.js');
}
  
  /**
   * Warn the page must be served over HTTPS
   * The `beforeinstallprompt` event won't fire if the page is served over HTTP.
   * Installability requires a service worker with a fetch event handler, and
   * if the page isn't served over HTTPS, the service worker won't load.
   */
if (window.location.protocol === 'http:') {
    const requireHTTPS = document.getElementById('requireHTTPS');
    const link = requireHTTPS.querySelector('a');
    link.href = window.location.href.replace('http://', 'https://');
    requireHTTPS.classList.remove('hidden');
}