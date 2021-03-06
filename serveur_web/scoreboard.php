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

// On importe ce que l'on as besoin
session_start();
require("includes/constants.php");
require("includes/databases.php");
require("includes/functions.php");

// On définit les variables propres à notre page
$page_title = readtext("pagetitle:scoreboard");

# Id de l'utilisateur
$uid = 0;
if (!empty($_GET["id"])) {
    $uid = $_GET["id"];
}

# Mettre à jour depuis la DB
$refresh = False;
if (!empty($_GET["refresh"])) {
	$refresh = $_GET["refresh"] == "true" || $_GET["refresh"] == 1;
}

// Un peu d'initialisation des variables de session
if(empty($_SESSION["cache"])) {
    $_SESSION["cache"] = [];
}
if(empty($_SESSION["cache"]["scoreboard"])) {
    $_SESSION["cache"]["scoreboard"] = array();
}

$scoreboard = $_SESSION["cache"]["scoreboard"];

if(empty($scoreboard) || $refresh) {
    // On recupère les meilleures scores
    $q = $pdo->prepare("SELECT * FROM score" . ($uid > 0 ? " WHERE user_id = ?" : "") . " LIMIT 50");
    $q->execute(($uid > 0 ? [$uid] : []));

    $scoreboard = array();

    while ($row = $q->fetch(PDO::FETCH_OBJ)) {
        $scoreboard[$row->id]["difficulty"] = $row->difficulty;
        $scoreboard[$row->id]["course_type"] = $row->course_type;
        $scoreboard[$row->id]["user_id"] = $row->user_id;
        $scoreboard[$row->id]["score"] = $row->score;
        $scoreboard[$row->id]["time"] = $row->time;
        $scoreboard[$row->id]["date"] = $row->date;
    }

    $q->closeCursor();
    $_SESSION["cache"]["scoreboard"] = $scoreboard;
}

// On affiche la page
include("views/scoreboard.view.php");