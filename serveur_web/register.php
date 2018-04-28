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
include('filters/guest_filter.php'); # Il faut être non connecté pour accéder à cette page
require("includes/constants.php");
require_once("includes/databases.php");
require_once("includes/functions.php");

// On définit les variables propres à notre page
$page_title = "S'inscrire";

// On vérifie si l'utilisateur a rempli le formulaire
if(!empty($_POST["pseudo"]) && !empty($_POST["password1"]) && !empty($_POST["password2"])) {
  extract($_POST);

  $_SESSION['infobar']['level'] = "danger";
  $_SESSION['infobar']['title'] = "Erreur:";

  if(strlen($pseudo) < 3 || strlen($pseudo) > 16){
    $_SESSION['infobar']['message'] = "Le nom d'utilisateur doit contenir entre 3 et 16 caractères.";
  } else {
      // On sauvegarde son nom d'utilisateur en session pour qu'il n'ait pas besoin de le réecrire
      $_SESSION["cache"]["pseudo"] = $pseudo;

      //Les deux mot de passe sont-il identique ? Si 0, ils sont identiques
      if (strcmp($password1, $password2) != 0) {
          $_SESSION['infobar']['message'] = "Les deux mots de passe ne sont pas identiques.";
      } else {
          if (strlen($password1) < 3 || strlen($password1) > 32) {
              $_SESSION['infobar']['message'] = "Le mot de passe doit contenir entre 3 et 32 caractères.";
          } else {
              $_SESSION["cache"]["pseudo"] = [];
              if (!is_name_unique($pdo, $pseudo)) {
                  $_SESSION['infobar']['message'] = "Ce pseudonyme est déjà utilisé. Veuillez en choisir un autre.";
              } else {
                  $_SESSION['infobar']['level'] = "success";
                  $_SESSION['infobar']['title'] = "Félicitation !";
                  $_SESSION['infobar']['message'] = "Inscription realisée avez succès ! Vous pouvez maintenant utilisez ces identifiants dans le jeu !";

                  register_user($pdo, $pseudo, $password1);
              }
          }
      }
  }
}

// On affiche la page (après verif pour que les messages s'affichent bien)
include("views/register.view.php");
