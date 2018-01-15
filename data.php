<?php

require_once("databases.php");

$q = $pdo->prepare("SELECT * FROM data");
$q->execute();

while($q->hasNext()){
	print($q->next());
}

$q->close();


if(isset($id)){
	$id = $_GET["id"];

	$jsontxt = array()
	$jsontxt['id']; = $id;
	$jsontxt['pseudo'] = "Guest";

	$fp = fopen('data.json', 'w');
	fwrite($fp, $jsontxt)
	fclose($fp)

	header("Location: data.json");
}