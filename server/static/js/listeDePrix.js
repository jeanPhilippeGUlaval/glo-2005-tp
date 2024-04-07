function DisplayListeDePrix(tableName, titleName)
{
    var dataToSend = {
        table: tableName,
        title: titleName
    };
    var queryString = Object.keys(dataToSend).map(key => key + '=' + dataToSend[key]).join('&');
    location.href = "listeDePrix?" + queryString;
}



// function OrderBy(TableName, Title, OrderBy)
// {
//     var dataToSend = {
//         table: TableName,
//         title: Title,
//         orderBy: OrderBy
//     };
//     var queryString = Object.keys(dataToSend).map(key => key + '=' + dataToSend[key]).join('&');
//     location.href = "/listeDePrix/orderBy?" + queryString;
// }
async function GetPage(Title, TableName){
    const formData = new FormData();
  
    // Add a text field
    formData.append("table", TableName);
    formData.append("title", Title);

    try {
        const response = await fetch("/listeDePrix", {
          method: "POST",
          body: formData
        });
        console.log(response.json());
      } catch (e) {
        console.error(e);
      }
}

async function AddToSoumission(productID) {
    let con = "#addForm".concat("-",productID)
    const form = document.querySelector(con);
    // Construct a FormData instance
    const formData = new FormData(form);
    // console.log(formData.get('soumissionID'))
    // console.log(formData.get('productID'))
    // if (formData.get('qty') <= 0){
    //     return
    // }
    // Add a text field
    // formData.append("soumissionID", soumissionID);
  
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

