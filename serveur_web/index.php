<?php

// On importe ce que l'on as besoin
session_abort();
require("includes/constants.php");

// On définit les variables propres à notre page
$page_title = "Accueil";

// On affiche la page
include("views/index.view.php");

?>
