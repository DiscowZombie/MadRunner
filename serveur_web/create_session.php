<?php

require("includes/databases.php");
require("includes/functions.php");

// Si il y a un Id dans l'url
if(!empty($_POST["pseudo"]) && !empty($_POST["password"])){
  $pseudo = $_POST["pseudo"];
  $password = $_POST["password"]; // Le mot de passe doit déjà été chiffrer

  $q = $pdo->prepare("SELECT id, password FROM user WHERE pseudo = ?");
  $q->execute([$pseudo]);

  $r = $q->fetch(PDO::FETCH_OBJ);
  $q->closeCursor();

  if(htmlspecialchars($password) == $r->password){
    $id = $r->id;

    // On génère une clé pour l'identification (Clé qui expire après un certains temps)
    $key = password_hash(uniqid(), PASSWORD_BCRYPT);

    // On met la clé dans la db
    $q = $pdo->prepare("INSERT INTO session(user_id, uuid, ip) VALUES (:id, :uuid, :ip)");
    $q->execute([
      "id" => $id,
      "uuid" => $key,
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
