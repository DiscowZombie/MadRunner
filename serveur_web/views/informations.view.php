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
    <?php include("partials/_header.php"); ?>

    <div id="main">

        <div class="col-sm-12">
            <p> <?= readtext("text:fulldescribe"); ?> </p>
            <h3><?= readtext("general:history"); ?></h3>
            <p> <?= readtext("text:history"); ?> </p>
        </div>

    </div> <!-- Fin de la division div .main -->

    <?php include("partials/_footer.php"); ?>
  </body>
</html>