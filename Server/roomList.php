<?php

$url ='./roomInfo.json';

if(!file_exists($url)) {
    echo '[]';
    exit;
}

$json_string = file_get_contents($url);
echo $json_string;
?>