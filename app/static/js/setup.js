function fevrURLdetect(id){
    URL = window.location.href.split("://");
    https = false;
    if (URL[0] == "https"){
      https = true;
    }
    fqdn = URL[1].split("/")[0]
    port = URL[1].split(":")
    if (Boolean(port[1])){
      port = port[1]
    }
    else{
      if (https == true){
        port = 443
      }
      else{
        port = 80
      }
    }
    httpsID = id + "https"
    httpID = id + "http"
    fqdnID = id + "fqdn"
    portID = id + "port"
    if (https){
      document.getElementById(httpsID).selected = true;
      document.getElementById(httpID).selected = false;
    }
    else{
      document.getElementById(httpID).selected = true;
      document.getElementById(httpsID).selected = false;
    }
    document.getElementById(fqdnID).value = fqdn
    document.getElementById(portID).value = port
  }