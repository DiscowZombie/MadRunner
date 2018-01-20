<?php

// On importe ce que l'on as besoin
require("includes/constants.php");
require_once("includes/databases.php");


/** == DEBUT PARTIE SQL == **/

// On recupère les meilleures scores
$q = $pdo->prepare("SELECT user_id, score, date FROM score ORDER BY score DESC LIMIT 3");
$q->execute([]);

$scoreboard = array();

$i = 1;

// Remplacer par une boucle for avec 3 composantes ?
while($row = $q->fetch(PDO::FETCH_OBJ)){
  $scoreboard[$i]["user_id"] = $row->user_id;
  $scoreboard[$i]["score"] = $row->score;
  $scoreboard[$i]["date"] = $row->date;
  $i++;
}

$q->closeCursor();

/** == FIN PARTIE SQL == **/


// On définit les variables propres à notre page
$page_title = "Tableau de bord";

// On affiche la page
include("views/scoreboard.view.php");

?>
