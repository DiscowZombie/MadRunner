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

    <div class="col-sm-12">

        <p>
            <?= readtext("text:smalldescribe"); ?>
        </p>

        <h3><?= readtext("general:preview") ?></h3>
        <br/>
        <img src="inc/img/screenshot1.png" width="300" height="239">
        <img src="inc/img/screenshot2.png" width="300" height="239">
        <img src="inc/img/screenshot3.png" width="300" height="239">

        <h3><?= readtext("general:download"); ?></h3>
        <br/>
		<a class="btn btn-primary" href="https://github.com/DiscowZombie/MadRunner/releases/download/1.1/Mad_Runner_v1.1_32bits.exe" role="button">Windows
            (32 bits)</a>
        <a class="btn btn-primary" href="https://github.com/DiscowZombie/MadRunner/releases/download/1.1/Mad_Runner_v1.1_64bits.exe" role="button">Windows
            (64 bits)</a>
    </div>

</div>

<!-- Bas de la page -->
<?php include("partials/_footer.php"); ?>
</body>
</html>
