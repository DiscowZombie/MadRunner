<?php

require_once("includes/databases.php");

// Si il y a un Id dans l'url
if(isset($_GET["id"]) AND !empty($_GET["id"])){
	$id = $_GET["id"];

	// On prépare le Json
	$jsontxt = array();

	// On prépare la requête
	$q = $pdo->prepare("SELECT * FROM user WHERE id = ?");
	$q->execute([$id]);

	while($row = $q->fetch(PDO::FETCH_OBJ)){
		$jsontxt['id'] = $row->id;
		$jsontxt['pseudo'] = $row->pseudo;
	}

	$q->closeCursor();

	# On retourne les infos comme un fichier json
	header('Content-type: application/json');
	echo json_encode($jsontxt);

}
