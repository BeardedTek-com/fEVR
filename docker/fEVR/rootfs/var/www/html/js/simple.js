const divInstall = document.getElementById('installContainer');
const butInstall = document.getElementById('butInstall');
function hideElement(target,targetClass){
    target.style.transition = "width 500ms ease"
    target.style.width= 0;
    target.classList.remove(targetClass);
}

function slideElement(target,targetClass){

    target.style.transition = "width 500ms ease"
    target.classList.add(targetClass);
    target.style.width = target.scrollWidth+"%";
}

function toggleMenu(menuId,contentId){
    target = document.getElementById(menuId)
    menu = document.getElementById(contentId)
    if (target.style.width == 0 || target.style.width == "0px" || target.style.width == "0%"){
        slideElement(target,'menuOpen');
    } else {
        hideElement(target,'menuOpen');

    }
}
function hideMenu(){
    menu = document.querySelector("#menu");
    hideElement(menu,'menuOpen');
}
function expandMenu(target){
    menu = document.querySelector(target)
    if (menu.classList.contains('submenu-show')){
        menu.classList.remove('submenu-show')
    }
    else
    {
        menu.classList.add('submenu-show')
    }
}
document.onclick = function (e) {
    if (e.target.id !== 'menu') {
        if (e.target.offsetParent && e.target.offsetParent.id !== 'menu')
            hideMenu()
    }
}
function changeSubTitle(subtitle){
    document.getElementById('subtitle').innerHTML = titleCase(" ".concat(subtitle.replace('menu_','').replace('_',' ')))
}
function clickItem(menuItem){
    changeSubTitle(menuItem);
    toggleMenu("menu",750);
}

function closeError(target,menuItem){
    changeSubTitle(menuItem)
    document.querySelector(target).close()
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
window.addEventListener('beforeinstallprompt', (event) => {
    // Prevent the mini-infobar from appearing on mobile.
    event.preventDefault();
    console.log('👍', 'beforeinstallprompt', event);
    // Stash the event so it can be triggered later.
    window.deferredPrompt = event;
    // Remove the 'hidden' class from the install button container.
    divInstall.classList.toggle('hidden', false);
});
butInstall.addEventListener('click', async () => {
    console.log('👍', 'butInstall-clicked');
    const promptEvent = window.deferredPrompt;
    if (!promptEvent) {
      // The deferred prompt isn't available.
      return;
    }
    // Show the install prompt.
    promptEvent.prompt();
    // Log the result
    const result = await promptEvent.userChoice;
    console.log('👍', 'userChoice', result);
    // Reset the deferred prompt variable, since
    // prompt() can only be called once.
    window.deferredPrompt = null;
    // Hide the install button.
    divInstall.classList.toggle('hidden', true);
});
window.addEventListener('appinstalled', (event) => {
    console.log('👍', 'appinstalled', event);
    // Clear the deferredPrompt so it can be garbage collected
    window.deferredPrompt = null;
});
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
