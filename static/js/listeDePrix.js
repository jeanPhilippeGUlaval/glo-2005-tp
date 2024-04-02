function DisplayListeDePrix(tableName, titleName)
{
    var dataToSend = {
        table: tableName,
        title: titleName
    };
    var queryString = Object.keys(dataToSend).map(key => key + '=' + dataToSend[key]).join('&');
    location.href = "listeDePrix?" + queryString;
}



function OrderBy(TableName, Title, OrderBy)
{
    var dataToSend = {
        table: TableName,
        title: Title,
        orderBy: OrderBy
    };
    var queryString = Object.keys(dataToSend).map(key => key + '=' + dataToSend[key]).join('&');
    location.href = "/listeDePrix/orderBy?" + queryString;
}

function incrementQuantity() {
    var input = document.getElementById('quantity');
    var value = parseInt(input.value, 10);
    input.value = value + 1;
}

function decrementQuantity() {
    var input = document.getElementById('quantity');
    var value = parseInt(input.value, 10);
    if (value > 1) {
        input.value = value - 1;
    }
}