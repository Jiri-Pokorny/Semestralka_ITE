const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const password = loginForm.password.value;

    if (password === "blackite") {
	    document.cookie = 'login=ok;path=/;secure';
        window.location="../web/index.html";
    } else {
        alert("Wrong password");
        loginErrorMsg.style.opacity = 1;
    }
})