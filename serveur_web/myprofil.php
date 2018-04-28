<?php

// On importe ce que l'on as besoin
session_start();
include('filters/auth_filter.php');
require("includes/constants.php");

// On définit les variables propres à notre page
$page_title = "Mon profil";

// On affiche la page
include("views/myprofil.view.php");