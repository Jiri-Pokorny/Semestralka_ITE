const buttonB = document.getElementById("logoutB");
const buttonA = document.getElementById("logoutA");

buttonB.addEventListener("click", (e) => {
    e.preventDefault();
    document.cookie = 'login="";expires=Thu, 18 Dec 2013 12:00:00 UTC";path=/';
    window.location="https://sulis150.zcu.cz";  
})
buttonA.addEventListener("click", (e) => {
    e.preventDefault();
    window.location="https://sulis150.zcu.cz";  
})
