<?php
class User{

    // database connection and table name
    private $conn;
    private $table_name = "users";

    // object properties
    public $id;
    public $last;
    public $middle;
    public $first;
    public $email;
    public $username;
    public $password;

    // constructor with $db as database connection
    public function __construct($db){
        $this->conn = $db;
    }
    // signup user
    function signup(){

        if($this->isAlreadyExist()){
            return false;
        }
        // query to insert record
        $query = "INSERT INTO
                    " . $this->table_name . "
                SET
                    id=:id, last=:last, middle=:middle, first=:first, email=:email, username=:username, password=:password";

        // prepare query
        $stmt = $this->conn->prepare($query);

        // sanitize
        $this->id=htmlspecialchars(strip_tags($this->id));
        $this->last=htmlspecialchars(strip_tags($this->last));
        $this->middle=htmlspecialchars(strip_tags($this->middle));
        $this->first=htmlspecialchars(strip_tags($this->first));
        $this->email=htmlspecialchars(strip_tags($this->email));
        $this->username=htmlspecialchars(strip_tags($this->username));
        $this->password=htmlspecialchars(strip_tags($this->password));

        // bind values
        $stmt->bindParam(":id", $this->id);
        $stmt->bindParam(":last", $this->last);
        $stmt->bindParam(":middle", $this->middle);
        $stmt->bindParam(":first", $this->first);
        $stmt->bindParam(":email", $this->email);
        $stmt->bindParam(":username", $this->username);
        $stmt->bindParam(":password", $this->password);

        // execute query

        if($stmt->execute()){
            $this->id = $this->conn->lastInsertId();
            return true;
        }

        return false;


    }
    // login user
    function login(){
        // select all query
        $query = "SELECT
                    `id`, `last`, `middle`, `first`, `email`, `username`, `password`
                FROM
                    " . $this->table_name . "
                WHERE
                    username='".$this->username."' AND password='".$this->password."'";
        // prepare query statement
        $stmt = $this->conn->prepare($query);
        // execute query
        $stmt->execute();
        return $stmt;
    }
    function isAlreadyExist(){
        $query = "SELECT *
            FROM
                " . $this->table_name . "
            WHERE
                username='".$this->username."'";
        // prepare query statement
        $stmt = $this->conn->prepare($query);
        // execute query
        $stmt->execute();
        if($stmt->rowCount() > 0){
            return true;
        }
        else{
            return false;
        }
    }
}
