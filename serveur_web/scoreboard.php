<?php

require_once("config/databases.php");

// On recupère les meilleures scores
$q = $pdo->prepare("SELECT user_id, score, date FROM score ORDER BY score DESC LIMIT 3");
$q->execute([]);

$scoreboard = array();

$i = 1;

// Remplacer par une boucle for avec 3 composantes ?
while($row = $q->fetch(PDO::FETCH_OBJ)){
  $scoreboard[$i]["user_id"] = $row->user_id;
  $scoreboard[$i]["score"] = $row->score;
  $scoreboard[$i]["date"] = $row->date;
  $i++;
}

$q->closeCursor();

?>


<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>Scoreboard | Mad Runner</title>
  </head>
  <body>

    <table>
     <tr>
         <td></td>
         <td style="text-align: center;">
           <b>UserId: <?= $scoreboard[1]["user_id"] ?></b>
           <br/>
           <?= $scoreboard[1]["score"] ?> points
           <br/>
           <?= date_format(date_create($scoreboard[1]["date"]), 'd M Y - H:i') ?>
         </td>
         <td></td>
     </tr>
     <tr>
         <td style="text-align: center;">
           <b>UserId: <?= $scoreboard[2]["user_id"] ?></b>
           <br/>
           <?= $scoreboard[2]["score"] ?> points
           <br/>
           <?= date_format(date_create($scoreboard[2]["date"]), 'd M Y - H:i') ?>
         </td>
         <td></td>
         <td style="text-align: center;">
           <b>UserId: <?= $scoreboard[3]["user_id"] ?></b>
           <br/>
           <?= $scoreboard[3]["score"] ?> points
           <br/>
           <?= date_format(date_create($scoreboard[3]["date"]), 'd M Y - H:i') ?>
         </td>
     </tr>
    </table>

  </body>
</html>
