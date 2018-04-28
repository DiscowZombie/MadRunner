<nav class="navbar navbar-inverse">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="https://madrunner.discowzombie.fr">Mad Runner</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li class="<?= $page_title == "Accueil" ? "active" : "" ?>"><a href="index">Accueil</a></li>
                <li class="<?= $page_title == "Informations" ? "active" : "" ?>"><a href="informations">Informations</a>
                </li>
                <li><a href="https://github.com/DiscowZombie/MadRunner" target="_blank">Github</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                <?php if(!empty($_SESSION["user_id"])) { ?>
                    <li class="dropdown">
                        <a class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><i class="fas fa-user"></i> <?= $_SESSION["username"] ?> <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li class="<?= $page_title == "Mon profil" ? "active" : "" ?>"><a href="myprofil">Mon profil</a></li>
                            <li class="<?= $page_title == "Tableau de score" ? "active" : "" ?>"><a href="scoreboard?id=<?= $_SESSION["user_id"] ?>">Mes classements</a></li>
                        </ul>
                    </li>

                    <li><a href="logout"><i class="fas fa-sign-in-alt"></i> Déconnexion</a></li>
                <?php } else { ?>
                    <li><a href="login"><i class="fas fa-user"></i> Connexion</a></li>
                    <li><a href="register"><i class="fas fa-sign-in-alt"></i> Inscription</a></li>
                <?php } ?>
            </ul>
        </div><!--/.nav-collapse -->
    </div>
</nav>

<header>

</header>

<div id="alerts">
    <?php if (!empty($_SESSION['infobar'])) {
    $level = !empty($_SESSION['infobar']['level']) ? $_SESSION['infobar']['level'] : "info";
    $title = !empty($_SESSION['infobar']['title']) ? $_SESSION['infobar']['title'] : "Info: ";
    $message = !empty($_SESSION['infobar']['message']) ? $_SESSION['infobar']['message'] : "/";
    ?>
    <div class="alert alert-<?= $level ?>"
    " alert-dismissible">
    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
    <strong><?= $title ?> </strong>
    <?php
    echo $message;
    $_SESSION['infobar'] = [];
    ?>
</div>
<?php } ?>
</div>