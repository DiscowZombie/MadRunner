<?php

// On importe ce que l'on as besoin
session_start();
require("includes/constants.php");
require("includes/databases.php");
require("includes/functions.php");

// On définit les variables propres à notre page
$page_title = "Tableau de score";

# Id de l'utilisateur
$uid = 0;
if(!empty($_GET["id"])) {
    $uid = $_GET["id"];
}

# Classé les résulats
$sort_param = " ORDER BY score DESC";
if(!empty($_GET["sort"])) {
    $sort_param = " ORDER BY " . str_replace("/", " ", $_GET["sort"]);
}

/** == DEBUT PARTIE SQL == **/

// On recupère les meilleures scores
$q = $pdo->prepare("SELECT * FROM score" . ($uid > 0 ? " WHERE user_id = ?" : "") . $sort_param);
$q->execute( ($uid > 0 ? [$uid] : []) );

$scoreboard = array();

while($row = $q->fetch(PDO::FETCH_OBJ)){
    $scoreboard[$row->id]["difficulty"] = $row->difficulty;
    $scoreboard[$row->id]["course_type"] = $row->course_type;
    $scoreboard[$row->id]["user_id"] = $row->user_id;
    $scoreboard[$row->id]["score"] = $row->score;
    $scoreboard[$row->id]["time"] = $row->time;
    $scoreboard[$row->id]["date"] = $row->date;
}

$q->closeCursor();

# TODO: Mettre la variable en cache
# var_dump($scoreboard);

/** == FIN PARTIE SQL == **/


// On affiche la page
include("views/scoreboard.view.php");

?>
