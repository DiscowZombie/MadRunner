<?php

// On importe ce que l'on as besoin
require("includes/constants.php");
require("includes/databases.php");
require("includes/functions.php");

$uid = 0;

if(isset($_GET["id"]) and !empty($_GET["id"])){
  $uid = htmlspecialchars($_GET["id"]);
  print($uid);
}

/** == DEBUT PARTIE SQL == **/

// On recupère les meilleures scores
$q = $pdo->prepare("SELECT user_id, score, coursetype, date FROM score" . ($uid > 0 ? " WHERE user_id = ?" : "") . " ORDER BY score DESC LIMIT 3");
$q->execute( ($uid > 0 ? [$uid] : []) );

$scoreboard = array();

$i = 1;

// Remplacer par une boucle for avec 3 composantes ?
while($row = $q->fetch(PDO::FETCH_OBJ)){
  $scoreboard[$i]["pseudo"] = get_username($pdo, $row->user_id);
  $scoreboard[$i]["coursename"] = get_coursename($pdo, $row->coursetype);
  $scoreboard[$i]["user_id"] = $row->user_id;
  $scoreboard[$i]["score"] = $row->score;
  $scoreboard[$i]["date"] = $row->date;
  $scoreboard[$i]["coursetype"] = $row->coursetype;
  $i++;
}

$q->closeCursor();

/** == FIN PARTIE SQL == **/


// On définit les variables propres à notre page
$page_title = "Tableau de bord";

// On affiche la page
include("views/scoreboard.view.php");

?>
