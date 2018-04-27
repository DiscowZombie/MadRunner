<?php

if(!isset($_SESSION['user_id']) OR !isset($_SESSION['pseudo'])){
    header('Location: login.php');
    exit();
}