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
    if($id == $_GET["id"]){
        echo "100";
        ////already exist
        exit;
    }
}
$info = new stdClass;
$info->userID=$gid;
$info->password=$gpw;
array_push($R, $info);
$json = json_encode($R,JSON_PRETTY_PRINT);
file_put_contents($url, $json);
echo 400;
?>