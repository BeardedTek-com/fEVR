
function modalActionOpen(id){
    var ua = navigator.userAgent.toLowerCase(); 
    if (ua.indexOf('safari') != -1) { 
        if (ua.indexOf('chrome') > -1) {
            document.querySelector(id).classList.remove('hidden')
            document.querySelector(id).showModal()
        } else {
            document.querySelector(id).classList.remove('hidden')
            document.querySelector(id).style="height: 80vh; width: 90vw; margin-left: 5vw; margin-top: 10vh;"
        }
    }
}

function modalActionClose(id){
    var ua = navigator.userAgent.toLowerCase(); 
    if (ua.indexOf('safari') != -1) { 
        if (ua.indexOf('chrome') > -1) {
            document.querySelector(id).classList.add('hidden')
            document.querySelector(id).close()
        } else {
            document.querySelector(id).classList.add('hidden')
        }
    }
}