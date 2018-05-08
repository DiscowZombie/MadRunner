<nav class="navbar navbar-inverse navbar-static-top">
    <div class="container">
        <div class="navbar-header">
            <!-- Permet d'ajouter un bouton pour que la bar de navigation soit responsive -->
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="https://madrunner.discowzombie.fr">Mad Runner</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li class="<?= $page_title == readtext("pagetitle:main") ? "active" : "" ?>"><a href="index"><?= readtext("pagetitle:main") ?></a></li>
                <li class="<?= $page_title == readtext("pagetitle:info") ? "active" : "" ?>"><a href="informations"><?= readtext("pagetitle:info") ?></a>
                </li>
                <li><a href="https://github.com/DiscowZombie/MadRunner" target="_blank">Github</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                <?php if(!empty($_SESSION["user_id"])) { ?>
                    <li class="dropdown">
                        <a class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><i class="fas fa-user"></i> <?= $_SESSION["username"] ?> <span class="caret"></span></a>
                        <ul class="dropdown-menu">
                            <li class="<?= $page_title == readtext("pagetitle:myprofile") ? "active" : "" ?>"><a href="myprofil"><?= readtext("pagetitle:myprofile") ?></a></li>
                            <li class="<?= $page_title == readtext("pagetitle:scoreboard") ? "active" : "" ?>"><a href="scoreboard?id=<?= $_SESSION["user_id"] ?>"><?= readtext("pagetitle:myrankings") ?></a></li>
                        </ul>
                    </li>

                    <li><a href="logout"><i class="fas fa-sign-in-alt"></i> <?= readtext("pagetitle:logout") ?></a></li>
                <?php } else { ?>
                    <li><a href="login"><i class="fas fa-user"></i> <?= readtext("pagetitle:login") ?></a></li>
                    <li><a href="register"><i class="fas fa-sign-in-alt"></i> <?= readtext("pagetitle:register") ?></a></li>
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