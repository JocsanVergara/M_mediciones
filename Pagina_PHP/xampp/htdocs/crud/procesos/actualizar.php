<?php session_start();
    include "../clases/Conexion.php"
    include "../clases/Crud.php"

    $Crud = new Crud();
    $id =  $_POST['id'];

    $datos = array(
        "hora" => $_POST['hora'],
        "Iden_tag" => $_POST['Iden_tag'],
        "RSSI" => $_POST['RSSI'],
        "Ang_azimuth" => $_POST['Ang_azimuth'],
        "Ang_elevacion" => $_POST['Ang_elevacion'],
        "Canal" => $_POST['Canal'],
        "LOS" => $_POST['LOS'],
        "Altura_ant" => $_POST['Altura_ant'],
        "Distancia_entre_ant_tag" => $_POST['Distancia_entre_ant_tag'],
        "Altura_tag" => $_POST['Altura_tag']
    );

    $respuesta = $Crud->actualizar($id,$datos);

    if ($respuesta->getModifiedCount()>0 || $respuesta->getMatchedCount()>0) {
        $_SESSION['mensaje_crud']='update';
        header("location:../index.php");
    } else{
        print_r($respuesta);
    }

?>