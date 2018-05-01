<!DOCTYPE html>
<html lang="fr">
  <head>
    <!-- Utf8, classique -->
    <meta charset="utf-8">
    <!-- Les deux lignes suivantes permettent que le site s'adapte à tous les écrans (cela vient de Bootstrap) -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- On définit le nom de la page grace à la variable Php qui se trouve dans informations.php et on ajoute le nom du site (constante) pour que ce oit ésthétique ! -->
    <title><?= $page_title ?> | <?= WEBSITE_NAME ?></title>
    <!-- On charge notre CSS perso, Boostrap ne fait quand même pas tout ! -->
    <link rel="stylesheet" href="inc/css/mainstyle.css">

    <!-- On ajoute les CSS de Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">

    <!-- On ajoute le CSS FontAwesome, cela permet d'avoir des petites icones sympatiques ! -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.10/css/all.css">

    <!-- Pour ajouter le support des versions Internet Explorer -->
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      <![endif]-->
  </head>
  <body>
    <!-- Haut de page, contient la barre de navigation -->
    <?php include("partials/_header.php"); ?>

    <!--
    TODO: Il y a pleins de tuto pour utiliser les class de Bootstrap super facilement sur ce site :
    https://www.w3schools.com/bootstrap, par exemple pour la mise en forme des images : https://www.w3schools.com/bootstrap/bootstrap_images.asp
    Il faut savoir qu'on utilise Bootstrap 3.7
    -->

    <!--
    Cette divisoon permet juste d'avoir une belle mise en forme (partie CSS)
     Cela represente le corps de la page
     -->
    <div id="main">

        <!--
        Dans Bootstrap, l'écran est découpé en 12 zones verticales. Ici on dit que l'on prends juste 6 zones, ce qui correspond à la moitié de
        l'écran, partie gauche. Le "sm" permet que cette partie s'adapte à tous les écrans (téléphones).
        -->
        <div class="col-sm-6">
            <!-- Ici, c'est la partie gaiche de l'écran -->
            <!-- Par exemple, si j'ajoute "class="img-circle"" mon image sera automatiquement arrondie sans modification sur le fichier en lui même, merci Bootstrap -->
            <img src="../fausse image" class="img-circle"/>

            <!-- On peut aussi créé des boutons super facilement -->
            <!-- Ici, sa class va le rendre bleu, les bouton "info" étant bleau dans Bootstrap -->
            <button type="button" class="btn btn-info">Je suis un bouton</button>

            <!-- Bon on peut faire pleins d'autres trucs mais la doc les listes mieux que moi !  https://www.w3schools.com/bootstrap -->
        </div>

        <!--
        De même, on reprends les 6 zones qu'il reste pour la partie droite de l'écran
        -->
        <div class="col-sm-6">
            <p>Partie droite de l'écran</p>
        </div>


    </div> <!-- Fin de la division div .main -->

    <!-- Bas de la page, contient du JS minimale pour Bootsrap -->
    <?php include("partials/_footer.php"); ?>
  </body>
</html>