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

// On importe ce que l'on as besoin
session_start();
include('filters/auth_filter.php');
require_once("includes/databases.php");
require("includes/constants.php");
require("includes/functions.php");

// On définit les variables propres à notre page
$page_title = readtext("pagetitle:myprofile");

// On vérifie si l'utilisateur a rempli le formulaire
if(!empty($_POST["password"]) && !empty($_POST["password1"]) && !empty($_POST["password2"])) {
    extract($_POST);

    $_SESSION['infobar']['level'] = "danger";
    $_SESSION['infobar']['title'] = readtext("general:error") . ":";

    if (strlen($password) < 3 || strlen($password) > 32) {
        $_SESSION['infobar']['message'] = readtext("error:passlenght");
    } else if(!isPasswordValidFor($pdo, $_SESSION["user_id"], $password)) {
        $_SESSION['infobar']['message'] = readtext("error:invalidpass");
    } else if(strcmp($password1, $password2) != 0) {
        $_SESSION['infobar']['message'] = readtext("error:notsamepass");
    } else if(strlen($password1) < 3 || strlen($password1) > 32) {
        $_SESSION['infobar']['message'] = readtext("error:passlenght");
    } else {
        $_SESSION['infobar']['level'] = "success";
        $_SESSION['infobar']['title'] = readtext("general:congrat");
        $_SESSION['infobar']['message'] = readtext("general:passupdatesuccess");

        updatePassword($pdo, $_SESSION["user_id"], $password1);
    }
}

// On vérifie si il essaye de changer sa langue
if(!empty($_GET["lang"])) {
    if ($_GET["lang"] == "English") {
        $_SESSION["lang"] = "en";
    } else if ($_GET["lang"] == "Français (French)") {
        $_SESSION["lang"] = "fr";
    }
}

// On affiche la page
include("views/myprofil.view.php");