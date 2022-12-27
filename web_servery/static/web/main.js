document.addEventListener("DOMContentLoaded", function() {
    refresh("last_activity.json");  
  });
setInterval(function(){ 
    refresh("last_activity.json");   
}, 5000);

function refresh(file) {
    fetch(file)
        .then(response => response.json())
        .then(data =>{

            state("BLACK",data.black.date,data.black.time);
            state("BLUE",data.blue.date,data.blue.time);
            state("GREEN",data.green.date,data.green.time);
            state("YELLOW",data.yellow.date,data.yellow.time);
            state("RED",data.red.date,data.red.time);
        })
    
}


function state(color,date,time) {
    var today = new Date();
    var color_d = new Date(date+" "+time);
    var color_s = Math.floor((today.getTime() - color_d.getTime())/1000);
    var color_stav = stav(color_s,color);
    document.getElementById(color).innerHTML = "Team: "+color+ "<br>Status: "+ color_stav+"<br>";           
                
}

function stav(time,color) {
    let svg = color+"_SVG";
    if(time>=120){
        document.getElementById(svg).style.fill = "red";
        return "offline";
    }else {
        document.getElementById(svg).style.fill = "green";
        return "online"        
    }
}

