<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title><?= $page_title ?> | <?= WEBSITE_NAME ?></title>
    <link rel="stylesheet" href="inc/css/mainstyle.css">
  </head>
  <body>
    <!-- Head de la page -->
    <?php include("partials/_header.php"); ?>

    <!-- Bas de la page -->
    <?php include("partials/_footer.php"); ?>

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
