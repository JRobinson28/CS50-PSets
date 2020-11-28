var technical = document.querySelector("#technical");
var software = document.querySelector("#software");
var communication = document.querySelector("#communication");

var techDesc = document.querySelector("#techDesc");
var softDesc = document.querySelector("#softDesc");
var comDesc = document.querySelector("#comDesc");

technical.addEventListener("click", function(){
	toggle(techDesc, softDesc, comDesc);
});

software.addEventListener("click", function(){
	toggle(softDesc, techDesc, comDesc);
});

communication.addEventListener("click", function(){
	toggle(comDesc, techDesc, softDesc);
});

function toggle(x, y, z) {
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
  y.style.display = "none"
  z.style.display = "none"
}