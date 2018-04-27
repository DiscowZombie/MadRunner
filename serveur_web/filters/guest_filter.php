<?php

if(isset($_SESSION['user_id']) AND isset($_SESSION['username'])){
    header('Location: index.php'); # Si il essaye d'acceder à une page en tant connecté (alors que c'est interdit) on le redirige vers la page d'accueil
    exit();
}