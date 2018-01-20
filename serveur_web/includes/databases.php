<?php

$conf_jsonfile = json_decode(file_get_contents("config/config.json"));

define("SGBD", $conf_jsonfile->SGBD);
define("DB_HOST", $conf_jsonfile->DB_HOST);
define("DB_USER", $conf_jsonfile->DB_USER);
define("DB_PASSWORD", $conf_jsonfile->DB_PASSWORD);
define("DATABASE", $conf_jsonfile->DATABASE);

try {
	$pdo = new PDO(SGBD.":host=".DB_HOST.";dbname=".DATABASE, DB_USER, DB_PASSWORD);
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);

} catch (Exception $e) {
	die("Erreur: " . $e->getMessage());
}
