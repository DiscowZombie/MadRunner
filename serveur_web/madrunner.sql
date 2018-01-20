-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Sam 20 Janvier 2018 à 13:47
-- Version du serveur :  5.7.14
-- Version de PHP :  7.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `madrunner`
--

-- --------------------------------------------------------

--
-- Structure de la table `data`
--

CREATE TABLE `data` (
  `id` int(11) NOT NULL,
  `pseudo` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `data`
--

INSERT INTO `data` (`id`, `pseudo`, `password`) VALUES
(1, 'DiscowZombie', '123456'),
(2, 'homermafia', '');

-- --------------------------------------------------------

--
-- Structure de la table `score`
--

CREATE TABLE `score` (
  `id` int(8) NOT NULL,
  `user_id` int(8) NOT NULL,
  `score` int(8) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `score`
--

INSERT INTO `score` (`id`, `user_id`, `score`, `date`) VALUES
(1, 1, 10, '2018-01-16 20:15:32'),
(2, 1, 150, '2018-01-16 20:23:59'),
(3, 2, 50, '2018-01-16 20:36:15');

-- --------------------------------------------------------

--
-- Structure de la table `sessions`
--

CREATE TABLE `sessions` (
  `uuid` varchar(255) NOT NULL,
  `user_id` int(8) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `sessions`
--

INSERT INTO `sessions` (`uuid`, `user_id`, `ip`, `date`) VALUES
('abcd', 1, '', '2018-01-17 14:11:02'),
('$2y$10$hTnTHVlYLrHXIAjmE5xkD.J70BZmEckKd0qQbfiSEE6bsqucklccW', 1, '::1', '2018-01-20 12:54:00'),
('$2y$10$rUhUOeQjz7Mxp1sEz8MnZen0dysgXb/sLimX/Om4JhDxX8o3LgAzK', 1, '::1', '2018-01-20 12:55:52'),
('$2y$10$UKC60/JC3njlCNma3MoOGOWeL3Ivv4JI5jh4aQjSWl8r16ZZcaA4e', 1, '::1', '2018-01-20 12:56:29'),
('$2y$10$A.g8O4HAEvP9CCNXvNjj/eGIP.qhoaKSCepdxzdTFeNCjaupurIbi', 1, '::1', '2018-01-20 12:56:51'),
('$2y$10$kMSKW3LUbQm3ew4gMJAvHOM9DGVqA9m4iZdWRpum50QPcE4/fP1t6', 1, '::1', '2018-01-20 12:56:52'),
('$2y$10$a1MXN2.xYGyLO30ysRfFnOyZ06Jd2vZQwJ5zVa71S5VnlVlDXIhOO', 1, '::1', '2018-01-20 12:57:23'),
('$2y$10$wteJ62ZrDI8zQ55NK8UPxeLXc8bF74xtHAX4oO9nT0w85nII89dCS', 1, '::1', '2018-01-20 13:00:17'),
('$2y$10$h5R3sBn3./1vwG.9BvSzi.dY/IiezNrWVynzqRC8dy0xux5K8KMLC', 1, '::1', '2018-01-20 13:00:39'),
('$2y$10$V7EQiNtz5UoqIMZRtnxnM.lcwvf8oNIhVLwNe69i1FeFJZmF6Voq2', 1, '::1', '2018-01-20 13:01:48'),
('$2y$10$egSz86tBy5.qjJfn9lgXKONwFmFibe47Vy/CPSbK0mXcqgYw4WkAm', 1, '::1', '2018-01-20 13:06:36'),
('$2y$10$BF7DaAB0ngexka0ZZRJe6.MdQvJOUsLb/g5GyI.w7Qy0Fw3t1BxGW', 1, '::1', '2018-01-20 13:06:37'),
('$2y$10$1akx6mHBxvEru7Jh2SHcJuQk4jkA0qTpd9swXExaLCeyko8EFhbM.', 1, '::1', '2018-01-20 13:09:51'),
('$2y$10$B4TPgCLYLIGix87roT7c7ei.BDGD7QDxOpcKWeAAv9L9slX7V9DoG', 1, '::1', '2018-01-20 13:10:41'),
('$2y$10$8MOo/MJsMD9MEt7uI260L.tiz1dwjfD.jAeVp0TnhLNZGowa7sbEC', 1, '::1', '2018-01-20 13:12:35'),
('$2y$10$im7gJcZTNeD237l/9VpdfupLjwOzURSCn7u/PgvQOeJb9WOu3ARDe', 1, '::1', '2018-01-20 13:13:08'),
('$2y$10$iQAwv.VStGaSkmdYHf5c1.h4NEHvG1pg7mzcJzmi0bxYGV39hcQGG', 1, '::1', '2018-01-20 13:14:53'),
('$2y$10$RdZmVkUtii5ikDQrY2edu.c/XEEmhclKoKSKgIN7d3V4fybZMynKq', 1, '::1', '2018-01-20 13:16:48');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `data`
--
ALTER TABLE `data`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `score`
--
ALTER TABLE `score`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `data`
--
ALTER TABLE `data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `score`
--
ALTER TABLE `score`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
