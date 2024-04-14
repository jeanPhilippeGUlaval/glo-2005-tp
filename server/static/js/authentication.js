// Fonction qui fait fait un appel pour afficher la page de création de compte
function GotoSignUp()
{
    location.href = "signup";
}
// Fonction qui fait fait un appel pour afficher la page de connexion
function GotoSignIn()
{
    location.href = "signin";
}
// Fonction qui fait fait un appel pour afficher la page d'oubli de mot de passe
function GoToForgotPassword()
{
    location.href = "forgotPassword"
}

function noPadding()
{
    document.getElementById("inputPassword").style.marginBottom="-1";
}

// Permet qu'à chaque fois que nous entrons une touche dans la boite de mot de passe, nous relançons la vérification afin
// de s'assurer que tout les critère soit rempli.
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

// Permet qu'à chaque fois que nous entrons une touche dans la boite de mot de passe, nous relançons la vérification afin
// de s'assurer que tout les critère soit rempli ainsi que l'adresse courriel
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

// Permet de valider que le courriel concorde avec la REGEX d'adresse courriel
function validateEmail()
{
    var email = document.getElementById("inputEmail");

    const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (email.value.match(validRegex))
    {
        return true;
    }
}

// Permet de valider le mot passe afin qu'il concorde au requis voulu.
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

    // Validation des lettres minuscules
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

    // Validation des lettres majuscules
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

    // Validation des nombre
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

    // Validation de la longueur
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
    // Si tout est valide, retourne vrai
    if (lowerOK && numberOK && upperOK && lengthOK)
    {
        return true;
    }
    return false
}

//Validation que le mot de passe est revérifier une deuxième fois.
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