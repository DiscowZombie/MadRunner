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

if(!function_exists('get_coursename')){
	function get_coursename($pdo, $enum){
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

if(!function_exists('is_name_unique')){
	function is_name_unique($pdo, $pseudo){
		$q = $pdo->prepare("SELECT pseudo FROM user WHERE pseudo = ?");
		$q->execute([$pseudo]);
		$amount = $q->rowCount();
		$q->closeCursor();

		return $amount == 0;
	}
}

if(!function_exists('register_user')){
	function register_user($pdo, $pseudo, $password){
		$q = $pdo->prepare("INSERT INTO user(pseudo, password) VALUES(:pseudo, :password)");
		$q->execute([
			"pseudo" => $pseudo,
			"password" => password_hash(htmlspecialchars($password), PASSWORD_BCRYPT)
		]);
		$q->closeCursor();
	}
}

?>
