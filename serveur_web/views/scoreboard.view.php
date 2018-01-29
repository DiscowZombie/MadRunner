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

    <?php if(isset($scoreboard[1])){ ?>
      <table>
       <tr>
           <td></td>
           <td style="text-align: center;">
             <b><?= $scoreboard[1]["pseudo"] ?></b>
             <br/><?= $scoreboard[1]["coursename"] ?>
             <br/>
             <?= $scoreboard[1]["score"] ?> points
             <br/>
             <?= date_format(date_create($scoreboard[1]["date"]), 'd M Y - H:i') ?>
           </td>
           <td></td>
       </tr>
       <tr>
          <?php if(isset($scoreboard[2])){ ?>
             <td style="text-align: center;">
               <b><?= $scoreboard[2]["pseudo"] ?></b>
               <br/><?= $scoreboard[2]["coursename"] ?>
               <br/>
               <?= $scoreboard[2]["score"] ?> points
               <br/>
               <?= date_format(date_create($scoreboard[2]["date"]), 'd M Y - H:i') ?>
             </td>
           <?php } ?>
           <?php if(isset($scoreboard[3])){ ?>
             <td></td>
             <td style="text-align: center;">
               <b><?= $scoreboard[3]["pseudo"] ?></b>
               <br/><?= $scoreboard[3]["coursename"] ?>
               <br/>
               <?= $scoreboard[3]["score"] ?> points
               <br/>
               <?= date_format(date_create($scoreboard[3]["date"]), 'd M Y - H:i') ?>
             </td>
          <?php } ?>
       </tr>
      </table>
    <?php }else{ ?>
      <p>Aucun résulat trouvé !</p>
    <?php } ?>

  </body>
</html>
