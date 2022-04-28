function clickIt(id){
    /* calls modalsActionOpen(id) or modalActionClose(id) from modal.js */
    if ( document.querySelector(id).classList.contains('hidden') ){
        modalActionOpen(id)
    }
    else{
        modalActionClose(id)
    }
}

function shareButton(id,btn,el){
    shareIcons = document.querySelector(id)
    shareDiv = document.querySelector(el)
    shareBtn = document.getElementById(btn)
    closeBtn = document.getElementById('closeBtn')
    if (window.getComputedStyle(shareIcons).getPropertyValue("opacity") == 0){
        shareIcons.style="opacity:1;"
        shareIcons.classList.remove('hidden')
        //shareDiv.style="background-color:rgba(240,255,255,0.3);border: solid 1px rgb(28,62,211); border-radius:2.5em;"
        shareBtn.classList.add('invisible')
        shareBtn.classList.remove('visible')
        shareBtn.classList.add('hidden')
        closeBtn.classList.remove('invisible')
        closeBtn.classList.add('visible')
        closeBtn.classList.remove('hidden')
    }
    else{
        shareIcons.style="opacity: 0; z-index: -1000";
        shareIcons.classList.add('hidden')
        //shareDiv.style = "border-radius:2.5em;";
        shareBtn.classList.remove('hidden')
        shareBtn.classList.add('visible')
        shareBtn.classList.remove('invisible')
        closeBtn.classList.add('hidden')
        closeBtn.classList.remove('visible')
        closeBtn.classList.add('invisible')
    }
}
function menu(Menu){
        m = document.getElementById(Menu);
        if (m.classList.contains('menuHide')){
            m.classList.remove('menuHide')
            document.cookie = "menu=open;path=/";
            
        }
        else{
            m.classList.add('menuHide')
            document.cookie = "menu=closed;path=/";
        }
    }