<?php

require_once('includes/functions.php');

// WORK
//var_dump(send_curl_request("http://localhost/serveur_web/data.php?id=1", "GET", null));

// Test...
$post = [
  'pseudo' => 'DiscowZombie',
  'password' => '123456'
];

var_dump(send_curl_request("http://localhost/serveur_web/create_session.php", "POST", $post));

$conf_jsonfile = read_json("secure/response.json");
echo($conf_jsonfile->key);
