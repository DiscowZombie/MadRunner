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

// Si il y a un Id dans l'url
if(isset($_GET["id"]) AND !empty($_GET["id"])){
	$id = $_GET["id"];

	// On prépare le Json
	$jsontxt = array();

	// On prépare la requête
	$q = $pdo->prepare("SELECT * FROM score WHERE user_id = ? ORDER BY difficulty, course_type, score ASC");
	$q->execute([$id]);

	while($row = $q->fetch(PDO::FETCH_OBJ)){
		$jsontxt[$row->difficulty][$row->course_type]["score"] = $row->score;
		$jsontxt[$row->difficulty][$row->course_type]["time"] = $row->time;
	}

	$q->closeCursor();

	# On retourne les infos comme un fichier json
	header('Content-type: application/json');
	echo json_encode($jsontxt);

}
