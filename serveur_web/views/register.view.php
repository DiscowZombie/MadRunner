<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title><?= $page_title ?> | <?= WEBSITE_NAME ?></title>
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
                <strong>Inscription: </strong>
                <br />
                <br />
                <form class="form-horizontal" method="post">
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="pseudo">Pseudonyme:</label>
                        <div class="col-sm-5">
                            <input class="form-control" type="text" id="pseudo" name="pseudo" value="<?php if(!empty($_SESSION["pseudo"])) echo $_SESSION["pseudo"]; ?>">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="password1">Mot de passe:</label>
                        <div class="col-sm-5">
                            <input class="form-control" type="password" id="password1" name="password1">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-sm-3" for="password2">Confirmation du mot de passe:</label>
                        <div class="col-sm-5">
                            <input class="form-control" type="password" id="password2" name="password2">
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-sm-offset-3 col-sm-9">
                            <button type="submit" class="btn btn-default">Valider</button>
                        </div>
                    </div>
                </form>
            </div>

            <!-- Partie droite de l'écran -->
            <div class="col-sm-6">
                <strong>Pourquoi s'inscire ?</strong>
                <br /> <br />
                <p>L'inscription vous permet de sauvegarder vos meilleurs en ligne et ainsi de les comparer facilement avec les autres. Cela vous permet également d'apparaitre dans le classement général des meilleurs joueurs de Mad Runner.</p>
                <br />
                <p>Votre inscription est totalement anonyme et sécurisé. Nous ne vous demanderons jamais votre nom ni prénom, vous utilisez un pseudonyme de votre choix pour tout le jeu. Ce dèrnier est unique et permet de vous reconnaitre. Pour la sécurité, notre site dispose d'un certificat officiel ce qui signique que vos données ne transittent jamais en clair.</p>
            </div>

        </div>
    </div>

    <!-- Bas de la page -->
    <?php include("partials/_footer.php"); ?>
  </body>
</html>
