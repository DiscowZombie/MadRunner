<?php

require_once("includes/databases.php");

if(!empty($_POST["key"]) AND !empty($_POST["score"]) AND !empty($_POST["coursetype"]) AND !empty($_POST["time"]) AND !empty($_POST["difficulty"])){
  $key = $_POST["key"];
  $score = $_POST["score"];
  $course_type = $_POST["coursetype"];
  $time = $_POST["time"];
  $difficulty = $_POST["difficulty"];

  $q = $pdo->prepare("SELECT id, user_id FROM session WHERE uuid = ?");
  $q->execute([$key]);

  $r = $q->fetch(PDO::FETCH_OBJ);
  $q->closeCursor();

  if(!empty($r->user_id)){
    // Insérer dans la bdd qui gère le score son score !  
    $q = $pdo->prepare("INSERT INTO score(user_id, score, time, difficulty, course_type) VALUES (:user_id, :score, :time, :difficulty, :coursetype)");
    $q->execute([
      "user_id" => $r->user_id,
      "score" => $score,
	  "time" => $time,
	  "difficulty" => $difficulty,
      "coursetype" => $course_type
    ]);
  }

}