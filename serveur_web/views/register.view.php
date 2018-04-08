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

    <!-- On créé notre formulaire pour s'inscrire -->
    <div>
      <form method="post">
          <div>
              <label>Choisir un pseudo:</label>
              <input type="text" id="pseudo" name="pseudo" value="<?php if(!empty($_SESSION["pseudo"])) echo $_SESSION["pseudo"]; ?>">
          </div>
          <div>
              <label>Mot de passe:</label>
              <input type="password" id="password" name="password">
          </div>
          <div>
              <label>Confirmation du mot de passe:</label>
              <input type="password" id="password2" name="password2">
          </div>
          <div class="valider">
            <button type="submit">S'inscire</button>
        </div>
      </form>
    </div>

    <!-- Bas de la page -->
    <?php include("partials/_footer.php"); ?>
  </body>
</html>
