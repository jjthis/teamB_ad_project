<?php

$url ='./roomInfo.json';

if(!file_exists($url)) {
    echo '404';
    exit;
}

$json_string = file_get_contents($url);
$R = json_decode($json_string, false);
$gid=$_GET["id"];
foreach ($R as $key => $row) {
    $id= $row->userID;
    if($id == $_GET["id"]){
        unset($R[$key]);
        $json = json_encode($R,JSON_PRETTY_PRINT);
        file_put_contents($url, $json);
        echo "400";
        exit;
    }
}
echo "101";
?>