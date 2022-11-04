<?php

    require_once $_SERVER['DOCUMENT_ROOT'] . "/crud/vendor/autoload.php"

    class Conexion{
        public function conectar(){
            try {
                $servidor = "127.0.0.1;
                $usuario = "adminpoxan";
                $password = "123456";
                $baseDatos = "memory_test";
                $puerto = "27017";

                $cadenaConexion = "mongodb:/" . "/" .
                                $usuario . ":" .
                                $password . "@" . 
                                $puerto . "/" . 
                                $baseDatos;
                $cliente = new MongoDB\Client($cadenaConexion);
                return $cliente->selectDatabase($baseDatos);
            } catch (\Throwable $th) {
                return $th->getMessage();
            }

        }
    }

    $objeto = new Conexion();
    var_dump($objeto->conectar);

?>