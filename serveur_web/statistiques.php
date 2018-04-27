<?php

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
