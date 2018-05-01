<?php
/**
 *     Mad Runner - Projet ISN
 *     Copyright (c) 2018  Ahmet ADAM, Mathéo CIMBARO
 *
 *     This program is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     This program is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

require_once("includes/databases.php");
require_once("includes/functions.php");

$jsontxt = array();

foreach (array("F", "M", "D") as $diff) {
    foreach (array("Q", "QH", "I") as $ct) {
        $q = $pdo->prepare("SELECT * FROM score WHERE difficulty = ? AND course_type = ? ORDER BY score ASC LIMIT 1");
        $q->execute([$diff, $ct]);
        $row = $q->fetch(PDO::FETCH_ASSOC);

        $jsontxt[$row["difficulty"]][$row["course_type"]]["score"] = $row["score"];
        $jsontxt[$row["difficulty"]][$row["course_type"]]["time"] = $row["time"];
    }
}

header('Content-type: application/json');
echo json_encode($jsontxt);
