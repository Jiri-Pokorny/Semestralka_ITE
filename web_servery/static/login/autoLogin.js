


const getCookieValue = (name) => (
  document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
)

let x = getCookieValue("login");
function checkCookie() {
  // checking whether user is null or not
  if (x == "ok") {
    //if user is not null then alert
    window.location="../web/index.html";  
  }else {
    //take input from user
    console.log("cookie "+document.cookie)
  }
}

checkCookie();