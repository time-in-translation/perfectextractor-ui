 function miniXhr(method, url, callback) {
     var xhr = new XMLHttpRequest();
     xhr.open(method, url);
     xhr.addEventListener('readystatechange', function() {
         if(xhr.readyState == 4) {
             callback(JSON.parse(xhr.response));
         }
     });
     xhr.send();
 }
