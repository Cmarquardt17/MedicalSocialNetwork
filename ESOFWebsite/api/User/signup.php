<?php

// get database connection
include_once '../config/database.php';

// instantiate user object
include_once '../objects/user.php';

$database = new Database();
$db = $database->getConnection();

$user = new User($db);

// set user property values
$user->last = $_POST['last'];
$user->middle = $_POST['middle'];
$user->first = $_POST['first'];
$user->email = $_POST['email'];
$user->username = $_POST['username'];
$user->password = base64_encode($_POST['password']);
$user->created = date('Y-m-d H:i:s');

// create the user
if($user->signup()){
    $user_arr=array(
        "status" => true,
        "message" => "Successfully Signup!",
        "id" => $user->id,
        "last" => $user->last,
        "middle" => $user->middle,
        "first" => $user->first,
        "email" => $user->email,
        "username" => $user->username
    );
}
else{
    $user_arr=array(
        "status" => false,
        "message" => "Username already exists!"
    );
}

print_r(json_encode($user_arr));

?>
