<?php

// On importe ce que l'on as besoin
session_abort();
include('filters/guest_filter.php');
require("includes/constants.php");
require_once("includes/databases.php");
require_once("includes/functions.php");

// On définit les variables propres à notre page
$page_title = "Connexion";

// On vérifie si l'utilisateur a rempli le formulaire
if(!empty($_POST["pseudo"]) && !empty($_POST["password"])) {
    extract($_POST);
    $login_success = login_user($pdo, $pseudo, $password);

    if($login_success == True) {
        $_SESSION["username"] = $pseudo;
        $_SESSION["user_id"] = get_id($pdo, $pseudo);

        // On le redirige vers l'accueil
        header("Location: index.php");
    } else {
        $_SESSION['infobar']['level'] = "danger";
        $_SESSION['infobar']['title'] = "Erreur:";
        $_SESSION['infobar']['message'] = "Pseudonyme ou mot de passe invalide. Veuillez essayer à nouveau.";
    }
}

// On affiche la page
include("views/login.view.php");