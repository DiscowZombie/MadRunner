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

        <!-- Tableau de score -->
        <div class="row">
            <div class="col-12 col-sm-12 col-lg-12">
                <!-- Le tableau de score -->
                <div class="table-responsive">
                    <table class="table table-bordered table-responsive" id="scoreboard">
                        <thead>
                        <tr>
                            <!-- Cette partie peut-encore être amméliorer dans le futur. Utilisez le classement Bootstrap 3 avec le JS ? -->
                            <th onclick="sortTable(0)"><?= readtext("general:pseudo"); ?></th>
                            <th onclick="sortTable(1)"><?= readtext("general:coursetype"); ?></th>
                            <th onclick="sortTable(2)"><?= readtext("general:difficulty"); ?></th>
                            <th onclick="sortTable(3)"><?= readtext("general:score"); ?></th>
                            <th onclick="sortTable(4)"><?= readtext("general:timedist"); ?></th>
                            <th onclick="sortTable(5)"><?= readtext("general:completdate"); ?></th>
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
                            echo "<td>" . ($item["course_type"] == "I" ? round($item["time"]) . " m" : gmdate("i:s", ((int)$item["time"] / 1000)) . "." . ((int)$item["time"])%1000 ) . "</td>";
                            $date = date_format(date_create($item["date"]), 'd M Y - H:i');
                            echo "<td>" . $date . "</td>";
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
                            <a type="button" class="btn btn-info btn-md" href="scoreboard"><?= readtext("general:seeglobalranks"); ?></a>
                        <?php } else { ?>
                            <a type="button" class="btn btn-info btn-md" href="scoreboard?id=<?= $_SESSION["user_id"]; ?>"><?= readtext("general:seepersonalranks"); ?></a>
                        <?php } ?>
                    </div>
                <?php } ?>

            </div>
        </div>
    </div>

    <!-- Bas de la page -->
    <?php include("partials/_footer.php"); ?>

    <!-- Un peu de js, c'est pas si loin du Java que ça et c'est juste une petite fonction :P -->
    <script>
        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("scoreboard");
            switching = true;
            // On met l'odre de sortie sur ascendant par défaut
            dir = "asc";
            // Boucle qui tourne tant que les changements (classements) n'ont pas été faits
            while (switching) {
                // Aucun changement n'a été fait pour le moment
                switching = false;
                // On recupère chaque ligne de notre tableau
                rows = table.getElementsByTagName("TR");
                // Boucle pour chaque ligne, sauf la première, car c'est le titre
                for (i = 1; i < (rows.length - 1); i++) {
                    // Par défaut, les élements ne doivent pas etre échangés, la c'est l'initialisation
                    shouldSwitch = false;
                    // Récupérer les deux élements à comparer
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    // Véirifer si les deux élements sont bien classés ou non
                    if (dir === "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            // S'ils ne sont pas bien placés, marqué qu'il y a un changement à faire et sortir de la boucle
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir === "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                if (shouldSwitch) {
                    // Il y a du changement à faire, nous le faissont de suite
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    // Un changement a été fait avec succès
                    switching = true;
                    // Juste un compteur que l'on incrémente à chaque fois
                    switchcount ++;
                } else {
                    // Si tout est déjà bien classé, c'est que ASC n'est pas la bonne direction, donc classons par DESC et retournons dans la boucle!
                    if (switchcount === 0 && dir === "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }
    </script>

    </body>
</html>
