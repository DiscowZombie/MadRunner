<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title><?= $page_title ?> | <?= WEBSITE_NAME ?></title>
    <link rel="shortcut icon" href="../inc/img/icon/favicon.ico" />
    <link rel="icon" type="image/png" href="../inc/img/icon/favicon.png" />
    <link rel="stylesheet" href="inc/css/mainstyle.css">

    <!-- On ajoute bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.10/css/all.css">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>
  <body>
    <!-- Head de la page -->
    <?php include("partials/_header.php"); ?>

    <div id="main">
        <div class="row">

            <!-- Partie gauche de l'écran -->
            <div class="col-sm-6">
                <strong><?= readtext("pagetitle:register"); ?></strong>
                <br />
                <br />
                <form class="form-horizontal" method="post">
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="pseudo"><?= readtext("general:pseudo"); ?>:</label>
                        <div class="col-sm-5">
                            <input class="form-control" type="text" id="pseudo" name="pseudo" value="<?php if(!empty($_SESSION["cache"]["pseudo"])) echo $_SESSION["cache"]["pseudo"]; ?>">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="password1"><?= readtext("general:password"); ?>:</label>
                        <div class="col-sm-5">
                            <input class="form-control" type="password" id="password1" name="password1">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="password2"><?= readtext("general:confirmpass"); ?>:</label>
                        <div class="col-sm-5">
                            <input class="form-control" type="password" id="password2" name="password2">
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-sm-offset-3 col-sm-9">
                            <button type="submit" class="btn btn-default"><?= readtext("general:submit"); ?></button>
                        </div>
                    </div>
                </form>
            </div>

            <!-- Partie droite de l'écran -->
            <div class="col-sm-6">
                <strong><?= readtext("text:registerwhyt"); ?></strong>
                <br /> <br />
                <p><?= readtext("text:registerwhy"); ?></p>
            </div>
        </div>
    </div>

    <!-- Bas de la page -->
    <?php include("partials/_footer.php"); ?>
  </body>
</html>
