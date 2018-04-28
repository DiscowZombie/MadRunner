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
    $jsontxt["id"] = $id;
    $jsontxt["key"] = $key;

    # On retourne les infos comme un fichier json
  	header('Content-type: application/json');
  	echo json_encode($jsontxt);
  }
}

?>
