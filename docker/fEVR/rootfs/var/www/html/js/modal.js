var ua = navigator.userAgent.toLowerCase(); 
if (ua.indexOf('safari') != -1) { 
    if (ua.indexOf('chrome') > -1) {
        document.querySelector('#frigateErr').classList.remove('hidden')
        document.querySelector('#frigateErr').showModal()
    } else {
        document.querySelector('#frigateErr').classList.remove('hidden')
    }
}
