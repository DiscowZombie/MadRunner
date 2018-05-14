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
include('filters/guest_filter.php');
require("includes/constants.php");
require_once("includes/databases.php");
require_once("includes/functions.php");

// On définit les variables propres à notre page
$page_title = readtext("pagetitle:login");

// On vérifie si l'utilisateur a rempli le formulaire
if(!empty($_POST["pseudo"]) && !empty($_POST["password"])) {
    extract($_POST);
    $login_success = login_user($pdo, $pseudo, $password);

    if($login_success == True) {
        $_SESSION["username"] = $pseudo;
        $_SESSION["user_id"] = get_id($pdo, $pseudo);
        $langdb = langfromDB($pdo, $pseudo);
        if($langdb == null) {
            $_SESSION["lang"] = $langdb;
        }

        // On le redirige vers l'accueil
        header("Location: index.php");
    } else {
        $_SESSION['infobar']['level'] = "danger";
        $_SESSION['infobar']['title'] = readtext("general:error");
        $_SESSION['infobar']['message'] = readtext("error:invalidcredentials");
    }
}

// On affiche la page
include("views/login.view.php");