<?php

define("SGBD", "mysql");
define("DB_HOST", "localhost");
define("DB_USER", "root");
define("DB_PASSWORD", "password");
define("DATABASE", "madrunner");

try {
	$pdo = new PDO(SGBD.":host=".DB_HOST.";dbname=".DATABASE, DB_USER, DB_PASSWORD);
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
} catch (Exception $e) {
	die('Erreur : ' . $e->getMessage());
} 