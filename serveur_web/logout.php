<?php

session_start();
include('filters/auth_filter.php');

if(isset($_SESSION['user_id']) AND isset($_SESSION['username'])){
    $_SESSION['user_id'] = [];
    $_SESSION['username'] = [];

    header("Location: index.php");
    exit();
}