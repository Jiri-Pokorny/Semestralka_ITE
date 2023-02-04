const getCookieValue = (name) => (
    document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
  )
  
  let x = getCookieValue("login");
  function checkCookie() {
    if (x == "ok") {
      
    }else {
      window.location="https://sulis150.zcu.cz";  
    }
  }
  
  checkCookie();