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

        <!-- Tableau de score -->
        <div class="row">
            <div class="col-12 col-sm-12 col-lg-12">
                <!-- Le tableau de score -->
                <div class="table-responsive">
                    <table class="table table-bordered table-responsive">
                        <thead>
                        <tr>
                            <!-- Cette partie peut-encore être amméliorer dans le futur. Utilisez le classement Bootstrap 3 avec le JS ? -->
                            <th>Pseudonyme <?php echo !empty($_REQUEST['sort']) ? "<a role='button' href='scoreboard" . (!empty($_REQUEST['id']) ? "?id=" . $_REQUEST["id"] : "") . "'>&times;</a>" : "<a href='scoreboard?" . (!empty($_REQUEST['id']) ? "id=" . $_REQUEST["id"] . "&" : "") . "sort=user_id/ASC'>&darr;</a>"; ?></th>
                            <th>Type de course <?php echo !empty($_REQUEST['sort']) ? "<a role='button' href='scoreboard" . (!empty($_REQUEST['id']) ? "?id=" . $_REQUEST["id"] : "") . "'>&times;</a>" : "<a href='scoreboard?" . (!empty($_REQUEST['id']) ? "id=" . $_REQUEST["id"] . "&" : "") . "sort=course_type/ASC'>&darr;</a>"; ?></th>
                            <th>Difficulté <?php echo !empty($_REQUEST['sort']) ? "<a role='button' href='scoreboard" . (!empty($_REQUEST['id']) ? "?id=" . $_REQUEST["id"] : "") . "'>&times;</a>" : "<a href='scoreboard?" . (!empty($_REQUEST['id']) ? "id=" . $_REQUEST["id"] . "&" : "") . "sort=difficulty/ASC'>&darr;</a>"; ?></th>
                            <th>Score <?php echo !empty($_REQUEST['sort']) ? "<a role='button' href='scoreboard" . (!empty($_REQUEST['id']) ? "?id=" . $_REQUEST["id"] : "") . "'>&times;</a>" : "<a href='scoreboard?" . (!empty($_REQUEST['id']) ? "id=" . $_REQUEST["id"] . "&" : "") . "sort=score/ASC'>&darr;</a>"; ?></th>
                            <th>Temps/Distance</th>
                            <th>Date de réalisation</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        foreach ($scoreboard as $item) {
                            echo "<tr>";
                            echo "<td>" . get_username($pdo, $item["user_id"]) . "</td>";
                            echo "<td>" . get_coursename($item["course_type"]) . "</td>";
                            echo "<td>" . get_difficulty($item["difficulty"]) . "</td>";
                            echo "<td>" . $item["score"] . "</td>";
                            echo "<td>" . ($item["course_type"] == "I" ? round($item["time"]) . " m" : gmdate("H:i:s", $item["time"])) . "</td>";
                            $french_dateF = date_format(date_create($item["date"]), 'd M Y - H:i');
                            echo "<td>" . $french_dateF . "</td>";
                            echo "</tr>";
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

                <!-- Seulement s'il est connecté -->
                <?php if(!empty($_SESSION["user_id"])) { ?>
                    <!-- Pour que le bouton soit bien à droite en bas -->
                    <div class="col-sm-10"> </div>
                    <div class="col-sm-2">
                        <?php if(!empty($_REQUEST['id'])) { ?>
                            <a type="button" class="btn btn-info btn-md" href="scoreboard">Voir le classement global</a>
                        <?php } else { ?>
                            <a type="button" class="btn btn-info btn-md" href="scoreboard?id=<?= $_SESSION["user_id"]; ?>">Voir le classement personnel</a>
                        <?php } ?>
                    </div>
                <?php } ?>

            </div>
        </div>
    </div>


    <!-- Bas de la page -->
    <?php include("partials/_footer.php"); ?>

  </body>
</html>
