<?php

// On importe ce que l'on as besoin
session_start();
require("includes/constants.php");
require_once("includes/databases.php");
require_once("includes/functions.php");

// On définit les variables propres à notre page
$page_title = "S'inscrire";

// On affiche la page
include("views/register.view.php");

// On vérifie si l'utilisateur a rempli le formulaire
if(!empty($_POST["pseudo"]) && !empty($_POST["password"]) && !empty($_POST["password2"])) {
  extract($_POST);

  if(strlen($pseudo) < 3 || strlen($pseudo) > 16){
    echo "Le nom d'utilisateur doit contenir entre 3 et 16 caractères.";
    return;
  }

  // On sauvegarde son nom d'utilisateur en session pour qu'il n'ait pas besoin de le réecrire
  $_SESSION["pseudo"] = $pseudo;

  //Les deux mot de passe sont-il identique ? Si 0, ils sont identiques
  if(strcmp($password, $password2) != 0){
    echo "Les deux mots de passe ne sont pas identiques.";
    return;
  }

  if(strlen($password) < 3 || strlen($password) > 32){
    echo "Le mot de passe doit contenir entre 3 et 32 caractères.";
    return;
  }

  if(!is_name_unique($pdo, $pseudo)){
    echo "Ce pseudonyme est déjà utilisé. Veuillez en choisir un autre.";
    // Le pseudo est déjà utilisé, on ne va pas lui reproposer !
    $_SESSION["pseudo"] = [];
    session_destroy();
    return;
  }

  register_user($pdo, $pseudo, $password);
  echo "Inscription realisée avez succès ! Vous pouvez maintenant utilisez ces identifiants dans le jeu !";
}

?>
