
function modalActionOpen(id){
    var ua = navigator.userAgent.toLowerCase(); 
    if (ua.indexOf('safari') != -1) { 
        if (ua.indexOf('chrome') > -1) {
            document.querySelector(id).classList.remove('hidden')
            document.querySelector(id).showModal()
        } else {
            document.querySelector(id).classList.remove('hidden')
            document.querySelector('.logo').classList.add('hidden')
            document.querySelector('.content').style="display: none;"
            document.querySelector(id).style="height: 80%; width: 90%; margin-left: 5%; margin-top: 10%;"
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
            document.querySelector('.logo').classList.remove('hidden')
            document.querySelector('.content').style=""
            document.querySelector(id).style=""
        }
    }
}