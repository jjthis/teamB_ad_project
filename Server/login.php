<?php

$url ='./userInfo/userInfo.json';

if(!file_exists($url)) {
    echo '404';
    exit;
}

$json_string = file_get_contents($url);
$R = json_decode($json_string, false);
$gid=$_GET["id"];
$gpw=$_GET['pw'];
foreach ($R as $row) {
    $id= $row->userID;
    if($id == $gid){
        if($gpw==$row->password)
            echo "400";
        else echo "102";
        exit;
    }
}echo "101";
?>