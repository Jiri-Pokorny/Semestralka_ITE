function getCookieValue() {
  let spli = document.cookie.split('=');
  return(spli[1])
}

function checkCookie() {
  var user = getCookieValue();
  // checking whether user is null or not
  if (user != "") {
    //if user is not null then alert
    console.log("user "+user);
    window.location="../web/index.html";  
  }else {
    //take input from user
    console.log("cookie "+document.cookie)
  }
}

checkCookie();