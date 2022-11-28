document.getElementById('refresh').addEventListener('click', refresh("last_activity.txt"));


function refresh(file) {

    getText("last_activity.txt");
    async function getText(file) {
        let myObject = await fetch(file);
        let text = await myObject.text();

        const teams = text.split(", ");
        document.getElementById('blue').innerHTML = teams[0];
        document.getElementById('black').innerHTML = teams[1];
        document.getElementById('yellow').innerHTML = teams[2];
        
    }
}





