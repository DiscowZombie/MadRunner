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

if (!function_exists('send_curl_request')) {
    function send_curl_request($ip, $method, $post_params)
    {
        if ($method !== "GET" AND $method !== "POST") {
            return;
        }

        $curl = curl_init($ip);

        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        if ($method == "POST") curl_setopt($curl, CURLOPT_POSTFIELDS, $post_params);

        $response = curl_exec($curl);

        curl_close($curl);

        return $response;
    }
}

if (!function_exists('get_ip')) {
    function get_ip()
    {
        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } else {
            $ip = $_SERVER['REMOTE_ADDR'];
        }
        return $ip;
    }
}

if (!function_exists('read_json')) {
    function read_json($path)
    {
        $json = json_decode(file_get_contents($path));
        return $json;
    }
}

if (!function_exists('get_username')) {
    function get_username($pdo, $id)
    {
        $q = $pdo->prepare("SELECT pseudo FROM user WHERE id = ?");
        $q->execute([$id]);
        while ($row = $q->fetch(PDO::FETCH_OBJ)) {
            $pseudo = $row->pseudo;
        }
        $q->closeCursor();

        return $pseudo;
    }
}

if (!function_exists('get_id')) {
    function get_id($pdo, $pseudo)
    {
        $q = $pdo->prepare("SELECT id FROM  `user` WHERE pseudo = ?");
        $q->execute([$pseudo]);
        $row = $q->fetch(PDO::FETCH_OBJ);
        $q->closeCursor();

        return $row->id;
    }
}

if (!function_exists('get_coursename')) {
    function get_coursename($enum)
    {
        $name = "";

        switch ($enum) {
            case 'Q':
                $name = "400 " . readtext("general:meter") . "s";
                break;
            case 'QH':
                $name = "400 " . readtext("general:meter") . "s " . readtext("general:hedge") . "s";
                break;
            case "I":
                $name = readtext("general:infiniterace");
                break;
            default:
                break;
        }

        return $name;
    }
}

if (!function_exists('get_difficulty')) {
    function get_difficulty($enum)
    {
        $name = "";

        switch ($enum) {
            case 'F':
                $name = readtext("general:easy");
                break;
            case 'M':
                $name = readtext("general:normal");
                break;
            case "D":
                $name = readtext("general:hard");
                break;
            default:
                break;
        }

        return $name;
    }
}

if (!function_exists('is_name_unique')) {
    function is_name_unique($pdo, $pseudo)
    {
        $q = $pdo->prepare("SELECT id FROM user WHERE pseudo = ?");
        $q->execute([$pseudo]);
        $amount = $q->rowCount();
        $q->closeCursor();

        return $amount == 0;
    }
}

if (!function_exists('register_user')) {
    function register_user($pdo, $pseudo, $password)
    {
        $q = $pdo->prepare("INSERT INTO user(pseudo, `password`) VALUES(:pseudo, :password)");
        $hashed = sha1($password);
        $q->execute([
            "pseudo" => $pseudo,
            "password" => $hashed
        ]);
        $q->closeCursor();
    }
}

if (!function_exists('login_user')) {
    function login_user($pdo, $pseudo, $clair_password)
    {
        $q = $pdo->prepare("SELECT id, `password` FROM `user` WHERE pseudo = ?");
        $q->execute([$pseudo]);
        $row = $q->fetch(PDO::FETCH_OBJ);

        $password = sha1($clair_password);

        return strcmp($row->password, $password) == 0 ? True : False;
    }
}

if (!function_exists('isPasswordValidFor')) {
    function isPasswordValidFor($pdo, $user_id, $password)
    {
        $q = $pdo->prepare("SELECT `password` FROM `user` WHERE id = ?");
        $q->execute([$user_id]);
        $row = $q->fetch(PDO::FETCH_OBJ);
        $passwordbdd = $row->password;
        $q->closeCursor();

        return strcmp($passwordbdd, sha1($password)) == 0 ? True : False;
    }
}

if (!function_exists('updatePassword')) {
    function updatePassword($pdo, $user_id, $newpassword)
    {
        $q = $pdo->prepare("UPDATE `user` SET `password` = ? WHERE id = ? ");
        $q->execute([sha1($newpassword), $user_id]);
        $q->closeCursor();
    }
}

if (!function_exists('readtext')) {
    function readtext($path, $lang = "en")
    {
        if ($lang == null) {
            if (empty($_SESSION["lang"])) {
                $pays = json_decode(file_get_contents('http://freegeoip.net/json/' . get_ip()), true)['country_name'];
                $_SESSION["lang"] = ($pays == "France" ? "fr" : "en");
            }
            $lang = $_SESSION["lang"];
        }

		$mess = json_decode( preg_replace('/[\x00-\x1F\x80-\xFF]/', '', file_get_contents("config/lang.json")), true)[$path][$lang];

        return $mess;
    }
}
