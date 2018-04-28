<?php

if(!empty($_SESSION['user_id']) AND !empty($_SESSION['username'])){
    $_SESSION['infobar']['level'] = "warning";
    $_SESSION['infobar']['title'] = "Erreur:";
    $_SESSION['infobar']['message'] = "Vous ne pouvez pas accéder à cette page en étant connecté !";

    header('Location: index.php'); # Si il essaye d'acceder à une page en tant connecté (alors que c'est interdit) on le redirige vers la page d'accueil
    exit();
}