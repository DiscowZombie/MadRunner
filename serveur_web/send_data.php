<?php
/**
 *     Mad Runner - Projet ISN
 *     Copyright (c) 2018  Ahmet ADAM, Mathéo CIMBARO
 *
 *     This program is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     This program is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

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