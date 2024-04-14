// Fonction qui va généré la prochaine page
function PageSuivante(table, numPage){
  console.log(numPage)
  numPage = parseInt(numPage) + 1
  location.href = "/listeDePrix/" + table + "?page=" + numPage
}

// Fonction qui va généré la page précedente
function PagePrec(table, numPage){
  console.log(numPage)
  numPage = parseInt(numPage) -1
  location.href = "/listeDePrix/" + table + "?page=" + numPage 
}


// création d'une form pour l'envoyé afin d'ajouter un produit à une soumission
async function AddToSoumission(productID) {
    let con = "#addForm".concat("-",productID)
    const form = document.querySelector(con);
    // Construction de la form
    const formData = new FormData(form);
  
    try {
      const response = await fetch("/product/addToSoumission", {
        method: "POST",
        body: formData,
      });
      console.log(response.json());
    } catch (e) {
      console.error(e);
    }
  }

