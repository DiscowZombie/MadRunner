<?php

require_once("config/databases.php");

// Si il y a un Id dans l'url
if(isset($_POST["pseudo"]) AND !empty($_POST["pseudo"]) AND isset($_POST["password"]) AND !empty($_POST["password"])){
  $pseudo = $_POST["pseudo"];
  $password = $_POST["password"];

  $q = $pdo->prepare("SELECT id, password WHERE pseudo = ?");
  $q->execute([$pseudo])

  $r = $q->fetch(PDO::FETCH_OBJ)[0];
  $q->closeCursor();

  if($password == $r->password){
    $id = $r->id;

    // On génère une clé pour l'identification (Clé qui expire après un certains temps)
    $key = password_hash(uniqid());

    // On met la clé dans la db
    $q = $pdo->prepare("INSERT INTO sessions(uuid, id) VALUES (:uuid, :id)");
    $q->execute([
      "uuid" => $key,
      "id" => $id
    ]);

    // On prépare le Json
  	$jsontxt = array();
    $jsontxt["key"] = $key;

    $fp = fopen('response.json', 'w');
  	fwrite($fp, json_encode($jsontxt));
  	fclose($fp);

  }

	header("Location: response.json");

}
