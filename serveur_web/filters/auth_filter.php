<?php

if(empty($_SESSION['user_id']) OR empty($_SESSION['username'])){
    $_SESSION['infobar']['level'] = "warning";
    $_SESSION['infobar']['title'] = "Erreur:";
    $_SESSION['infobar']['message'] = "Vous devez être connecté pour voir cette page ou effectuer cette action !";

    header('Location: login.php');
    exit();
}