<?php

require_once("config/databases.php");

// Si il y a un Id dans l'url
if(isset($_GET["id"]) AND !empty($_GET["id"])){
	$id = $_GET["id"];

	// On prépare le Json
	$jsontxt = array();

	// On prépare la requête
	$q = $pdo->prepare("SELECT * FROM data WHERE id = ?");
	$q->execute([$id]);

	while($row = $q->fetch(PDO::FETCH_OBJ)){
		$jsontxt['id'] = $row->id;
		$jsontxt['pseudo'] = $row->pseudo;
	}

	$q->closeCursor();

	# On écrit dans le fichier json
	$fp = fopen('data.json', 'w');
	fwrite($fp, json_encode($jsontxt));
	fclose($fp);

	header("Location: data.json");

}
