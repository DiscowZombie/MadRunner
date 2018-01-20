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

?>
