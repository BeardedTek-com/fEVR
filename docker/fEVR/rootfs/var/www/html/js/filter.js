function filterEvents(){
    count = document.getElementById('countSelect').value
    camera = document.getElementById('camSelect').value
    object = document.getElementById('objSelect').value
    scores = +document.getElementById('scoreSelect').value.replace("%", "")/100
    times = document.getElementById('timeSelect').value
    url = "?count="+count+"&camera="+camera+"&type="+object+"&score="+scores+"&time="+times+"&page=1";
    location.href=url;
}