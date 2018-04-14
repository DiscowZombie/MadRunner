<?php

require_once("includes/databases.php");

if(!empty($_POST["key"]) AND !empty($_POST["score"]) AND !empty($_POST["coursetype"])){
  $key = $_POST["key"];
  $score = $_POST["score"];
  $course_type = $_POST["coursetype"];

  $q = $pdo->prepare("SELECT user_id FROM session WHERE uuid = ?");
  $q->execute([$key]);

  $r = $q->fetch(PDO::FETCH_OBJ);
  $q->closeCursor();

  # TODO: Problème ici: le retour est null !
  if(!empty($r->user_id)){
    // Insérer dans la bdd qui gère le score son score !
    $q = $pdo->prepare("INSERT INTO score(user_id, score, coursetype) VALUES (:user_id, :score, :coursetype)");
    $q->execute([
      "user_id" => $id,
      "score" => $score,
      "coursetype" => $course_type
    ]);
  }

}
