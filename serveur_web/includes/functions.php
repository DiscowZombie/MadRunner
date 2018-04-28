<?php

if(!function_exists('send_curl_request')){
	function send_curl_request($ip, $method, $post_params){
    if($method !== "GET" AND $method !== "POST"){
      return;
    }

    $curl = curl_init($ip);

    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    if($method == "POST") curl_setopt($curl, CURLOPT_POSTFIELDS, $post_params);

    $response = curl_exec($curl);

    curl_close($curl);

    return $response;
	}
}

if(!function_exists('get_ip')){
  function get_ip(){
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

if(!function_exists('read_json')){
	function read_json($path){
		$json = json_decode(file_get_contents($path));
		return $json;
	}
}

if(!function_exists('get_username')){
	function get_username($pdo, $id){
		$q = $pdo->prepare("SELECT pseudo FROM user WHERE id = ?");
		$q->execute([$id]);
		while($row = $q->fetch(PDO::FETCH_OBJ)){
		  $pseudo = $row->pseudo;
		}
		$q->closeCursor();

		return $pseudo;
	}
}

if(!function_exists('get_id')){
    function get_id($pdo, $pseudo){
        $q = $pdo->prepare("SELECT id FROM  `user` WHERE pseudo = ?");
        $q->execute([$pseudo]);
        $row = $q->fetch(PDO::FETCH_OBJ);
        $q->closeCursor();

        return $row->id;
    }
}

if(!function_exists('get_coursename')){
	function get_coursename($enum){
		$name = "";

		switch ($enum) {
			case 'Q':
				$name = "400 mètres";
				break;
			case 'QH':
				$name= "400 mètres haies";
				break;
			case "I":
				$name = "Course Infini";
				break;
			default:
				break;
		}

		return $name;
	}
}

if(!function_exists('get_difficulty')){
    function get_difficulty($enum){
        $name = "";

        switch ($enum) {
            case 'F':
                $name = "Facile";
                break;
            case 'M':
                $name= "Moyen";
                break;
            case "D":
                $name = "Difficile";
                break;
            default:
                break;
        }

        return $name;
    }
}

if(!function_exists('is_name_unique')){
	function is_name_unique($pdo, $pseudo){
		$q = $pdo->prepare("SELECT id FROM user WHERE pseudo = ?");
		$q->execute([$pseudo]);
		$amount = $q->rowCount();
		$q->closeCursor();

		return $amount == 0;
	}
}

# Fonctionne: 28.04 9h54
if(!function_exists('register_user')){
	function register_user($pdo, $pseudo, $password){
		$q = $pdo->prepare("INSERT INTO user(pseudo, `password`) VALUES(:pseudo, :password)");
		$hashed = sha1($password);
		$q->execute([
			"pseudo" => $pseudo,
			"password" => $hashed
		]);
		$q->closeCursor();
	}
}

if(!function_exists('login_user')){
    function login_user($pdo, $pseudo, $clair_password){
        $q = $pdo->prepare("SELECT id, `password` FROM `user` WHERE pseudo = ?");
        $q->execute([$pseudo]);
        $row = $q->fetch(PDO::FETCH_OBJ);

        $password = sha1($clair_password);

        echo "Clair Pass: " . $clair_password;
        echo "BDD Pass: " . $row->password;
        echo "User Pass: " . $password;

        return strcmp($row->password, $password) == 0 ? True : False;
    }
}
