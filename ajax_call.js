$(document).ready(function() {
   $("#responsecontainer").load("/result");
   var refreshId = setInterval(function() {
      $("#responsecontainer").load('/result');
      }, 10000);
   $.ajaxSetup({ cache: false });

});


#---------------

 $(document).ready(function() {
   $("#responsecontainer").load("/result");
   var ip_addr = document.getElementById('ip_addr');
   var req_port = document.getElementById('req_port')
   var refreshId = setInterval(function() {
      $("#responsecontainer").load('/result', { ip: ip_addr.value, port:req_port.value });
      }, 10000);
   $.ajaxSetup({ cache: false });

});