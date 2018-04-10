<?php

require("includes/databases.php");
require("includes/functions.php");

// Si il y a un Id dans l'url
if(!empty($_GET["pseudo"]) && !empty($_GET["password"])){
  $pseudo = $_GET["pseudo"];
  $password = $_GET["password"]; // Le mot de passe doit déjà été chiffrer

  $q = $pdo->prepare("SELECT id, password FROM user WHERE pseudo = ?");
  $q->execute([$pseudo]);

  $r = $q->fetch(PDO::FETCH_OBJ);
  $q->closeCursor();

  if(htmlspecialchars($password) == $r->password){
    $id = $r->id;

    // On génère une clé pour l'identification (Clé qui expire après un certains temps)
    $key = password_hash(uniqid(), PASSWORD_BCRYPT);

    // On met la clé dans la db
    $q = $pdo->prepare("INSERT INTO session(uuid, user_id, ip) VALUES (:uuid, :id, :ip)");
    $q->execute([
      "uuid" => $key,
      "id" => $id,
      "ip" => get_ip()
    ]);

    // On prépare le Json
  	$jsontxt = array();
    $jsontxt["key"] = $key;

    # On retourne les infos comme un fichier json
  	header('Content-type: application/json');
  	echo json_encode($jsontxt);
  }

}

?>
