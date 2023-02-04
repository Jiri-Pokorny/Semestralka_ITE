//inicializa�n� stav p�i na�ten� webu
document.addEventListener("DOMContentLoaded", function () {
    refresh("last_activity.json");  
});
//obnoven� stavu po 5 sekund�ch
setInterval(function(){ 
    refresh("last_activity.json");   
}, 5000);

function refresh(file) {
    //p�e�ten� informac� o stavu ESP z json souboru: "last_activity.json"
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

//zji�t�n� stavu ESP
function state(color, date, time) {
    var today = new Date();
    //p�eveden� �asu
    var color_d = new Date(date + " " + time);
    //zji�t�n� jak star� je posledn� aktivita ESP
    var color_s = Math.floor((today.getTime() - color_d.getTime()) / 1000);

    var color_stav = stav(color_s, color);
    //zaps�n� stavu na web
    document.getElementById(color).innerHTML = "Team: "+color+ "<br>Status: "+ color_stav+"<br>";           
                
}
//rozhodnut� o aktivit� ESP
function stav(time,color) {
    let svg = color + "_SVG";
    //pokud ESP nevys�l� d�le jak 2 minuty je pova�ov�n za neaktivn�
    if (time >= 120) {
        //zbarven� stavu na webu �erven�
        document.getElementById(svg).style.fill = "red";
        return "offline";
    } else {
        //zbarven� stavu na webu zelen�
        document.getElementById(svg).style.fill = "green";
        return "online"        
    }
}
