
function openTab(evt, objname) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(objname).style.display = "block";
    evt.currentTarget.className += " active";
}

var allCells = $("td, th");

allCells
  .on("mouseover", function() {
    var el = $(this),
        pos = el.index();
    el.parent().find("th, td").addClass("hover");
    allCells.filter(":nth-child(" + (pos+1) + ")").addClass("hover");
  })
  .on("mouseout", function() {
    allCells.removeClass("hover");
  });


