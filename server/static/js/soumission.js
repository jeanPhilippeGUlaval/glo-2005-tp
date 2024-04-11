$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  })

function showAlert(error)
{
  if (error !== "") {
    return true
  }
  return false
}

function deleteSoumission(soumissionID)
{
  location.href= "/soumission/supprimerSoumission?id="+ soumissionID
}

function sendSoumission(soumissionID)
{
  location.href= "/soumission/envoyerSoumission?id="+ soumissionID
}
