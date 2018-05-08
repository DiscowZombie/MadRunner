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

if(!empty($_SESSION['user_id']) AND !empty($_SESSION['username'])){
    $_SESSION['infobar']['level'] = "warning";
    $_SESSION['infobar']['title'] = readtext("general:error") . ":";
    $_SESSION['infobar']['message'] = readtext("error:mustlogout");

    header('Location: index.php'); # Si il essaye d'acceder à une page en tant connecté (alors que c'est interdit) on le redirige vers la page d'accueil
    exit();
}