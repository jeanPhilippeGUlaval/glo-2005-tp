// Génère la bandrole pour ajouter une nouvelle soumission
$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  })

// Nous permet d'envoyer la demande avec la soumission à supprimer
function deleteSoumission(soumissionID)
{
  location.href= "/soumission/supprimerSoumission?id="+ soumissionID
}

// Nous permet d'envoyer la demande avec la soumission à envoyer
function sendSoumission(soumissionID)
{
  location.href= "/soumission/envoyerSoumission?id="+ soumissionID
}
