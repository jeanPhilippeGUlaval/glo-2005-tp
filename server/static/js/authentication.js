function GotoSignUp()
{
    location.href = "signup";
}

function GotoSignIn()
{
    location.href = "signin";
}
function GoToForgotPassword()
{
    location.href = "forgotPassword"
}

function createAnAccount()
{
    location.href = "createAccount";
}

function noPadding()
{
    document.getElementById("inputPassword").style.marginBottom="-1";
}

function validateChangePassword()
{
    var myInput = document.getElementById("inputPassword");

    myInput.onblur = function() {
        document.getElementById("message").style.display = "none";
    }

    myInput.onfocus = function() {
        document.getElementById("message").style.display = "block";
    }


    if (validateRepeat() && validateMDP())
    {
        document.getElementById("changePassword").disabled=false;
    }
}

function validate()
{
    var myInput = document.getElementById("inputPassword");

    myInput.onblur = function() {
        document.getElementById("message").style.display = "none";
    }

    myInput.onfocus = function() {
        document.getElementById("message").style.display = "block";
    }


    if (validateRepeat() && validateEmail() && validateMDP())
    {
        document.getElementById("createAccount").disabled=false;
    }
}

function validateEmail()
{
    var email = document.getElementById("inputEmail");

    const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (email.value.match(validRegex))
    {
        return true;
    }
}

function validateMDP()
{
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");
    var myInput = document.getElementById("inputPassword");
    var repeatInput = document.getElementById("inputPasswordRepeat")


    var lowerOK = false;
    var upperOK = false;
    var numberOK = false;
    var lengthOK = false;
    var repeatOk = false;
    if (repeatInput.value != myInput.value)
    {
        repeatInput.style.borderColor="#EF5350";
    } else {
        repeatInput.style.borderColor="";
        repeatOk = true;
    }

    var lowerCaseLetters = /[a-z]/g;
    if(myInput.value.match(lowerCaseLetters)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
        myInput.style.borderColor="";
        lowerOK = true;
    } else {
        letter.classList.remove("valid");
        myInput.style.borderColor="#EF5350";
        letter.classList.add("invalid");
    }

    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if(myInput.value.match(upperCaseLetters)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
        myInput.style.borderColor="";
        upperOK = true;
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
        myInput.style.borderColor="#EF5350";
    }

    // Validate numbers
    var numbers = /[0-9]/g;
    if(myInput.value.match(numbers)) {
        number.classList.remove("invalid");
        myInput.style.borderColor="";
        number.classList.add("valid");
        numberOK = true;
    } else {
        number.classList.remove("valid");
        myInput.style.borderColor="#EF5350";
        number.classList.add("invalid");
    }

    // Validate length
    if(myInput.value.length >= 8) {
        length.classList.remove("invalid");
        myInput.style.borderColor="";
        length.classList.add("valid");
        lengthOK = true;
    } else {
        length.classList.remove("valid");
        myInput.style.borderColor="#EF5350";
        length.classList.add("invalid");
    }
    if (lowerOK && numberOK && upperOK && lengthOK)
    {
        return true;
    }
    return false
}

function validateRepeat()
{
    var myInput = document.getElementById("inputPassword");
    var repeatInput = document.getElementById("inputPasswordRepeat")
    if (repeatInput.value != myInput.value)
    {
        repeatInput.style.borderColor="#EF5350";
    } else {
        repeatInput.style.borderColor="";
        return true;
    }
}