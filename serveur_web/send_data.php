<?php

require_once("includes/databases.php");

// Si il y a un Id dans l'url
if(isset($_GET["key"]) AND !empty($_GET["key"]) AND isset($_GET["score"]) AND !empty($_GET["score"])){
  $key = $_GET["key"];
  $score = $_GET["score"];

  $q = $pdo->prepare("SELECT user_id FROM sessions WHERE uuid = ?");
  $q->execute([$key]);

  // FETCH_ASSOC: Retourne la ligne suivante en tant qu'un tableau
  $id = $q->rowCount() == 1 ? $q->fetch(PDO::FETCH_ASSOC)["user_id"] : -1;
  $q->closeCursor();

  if($id !== -1){
    // Insérer dans la bdd qui gère le score son score !
    $q = $pdo->prepare("INSERT INTO score(user_id, score) VALUES (:user_id, :score)");
    $q->execute([
      "user_id" => $id,
      "score" => $score
    ]);

  }

}
