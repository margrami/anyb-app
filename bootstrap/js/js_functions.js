var tds = 
  document.querySelectorAll("td");
var ths = 
  document.querySelectorAll("th");

var cells = 
    Array.prototype.slice.call(tds)
      .concat(
        Array.prototype.slice.call(ths)
      );

var rows =
  document.querySelectorAll("tr");

[].forEach.call(
  cells, 
  function(el) {
    el.addEventListener(
      'mouseover', 
      function() {

        var index = indexInParent(this);
        
        for (var i = 0; i < rows.length; i++) {
          var cellsInThisRow = rows[i].getElementsByTagName("td");
          
          if (cellsInThisRow.length == 0) {
            cellsInThisRow = rows[i].getElementsByTagName("th");
          }
          
          cellsInThisRow[index]
            .classList
            .add("hover");
        };  
                  
      }, 
      false
    );
  }
);

[].forEach.call(
  cells, 
  function(el) {
    el.addEventListener(
      'mouseout', 
      function() {
        for (var i = 0; i < cells.length; i++) {
          cells[i]
            .classList
            .remove("hover");
        }
      }, 
      false
    );
  }
);

function indexInParent(node) {
    var children = node.parentNode.childNodes;
    var num = 0;
    for (var i=0; i<children.length; i++) {
         if (children[i]==node) return num;
         if (children[i].nodeType==1) num++;
    }
    return -1;
}