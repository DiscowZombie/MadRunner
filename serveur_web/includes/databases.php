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
	die("DB - Error: " . $e->getMessage());
}
