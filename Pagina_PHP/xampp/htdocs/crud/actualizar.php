<?php 
    include "./clases/Conexion.php";
    include "./clases/Crud.php";

    $crud = new Crud();
    $id = $_POST['id'];
    $datos = $crud->obtenerDocumento($id);
    $idMongo = $datos->_id;

?>

<?php include "./header.php"; ?>

<div class="container">
    <div class="row">
        <div class="col">
            <div class="card mt -4">
                <div class="card-body">
                    <a href="index.php" class="btn btn-info">
                        <i class="fa-solid fa-left-long"></i> regresar
                    </a>
                    <h2>Actualizar un registro de las antenas</h2>
                    <form action="./procesos/actualizar.php" method="post">
                        <input type="text" hidden value = "<?php echo $idMongo ?>" name = "id">
                        <label for="hora">Hora</label>
                        <input type="text" class="form-control" name="hora" id="hora" value = "<?php echo $datos->hora ?>">
                        <label for="Iden_tag">Identificador del tag</label>
                        <input type="text" class="form-control" name="Iden_tag" id="Iden_tag" value = "<?php echo $datos->Iden_tag ?>">
                        <label for="RSSI">RSSI</label>
                        <input type="text" class="form-control" name="RSSI" id="RSSI" value = "<?php echo $datos->RSSI ?>">
                        <label for="Ang_azimuth">Angulo de Azimuth</label>
                        <input type="text" class="form-control" name="Ang_azimuth" id="Ang_azimuth" value = "<?php echo $datos->Ang_azimuth ?>">
                        <label for="Ang_elevacion">Angulo de Elevacion</label>
                        <input type="text" class="form-control" name="Ang_elevacion" id="Ang_elevacion" value = "<?php echo $datos->Ang_elevacion ?>">
                        <label for="Canal">Canal</label>
                        <input type="text" class="form-control" name="Canal" id="Canal" value = "<?php echo $datos->Canal ?>">
                        <label for="LOS">Linea de vision</label>
                        <input type="text" class="form-control" name="LOS" id="LOS" value = "<?php echo $datos->LOS ?>">
                        <label for="Altura_ant">Altura de la antena</label>
                        <input type="text" class="form-control" name="Altura_ant" id="Altura_ant" value = "<?php echo $datos->Altura_ant ?>">
                        <label for="Distancia_entre_ant_tag">Distancia entre la antena y el tag</label>
                        <input type="text" class="form-control" name="Distancia_entre_ant_tag" id="Distancia_entre_ant_tag" value = "<?php echo $datos->Distancia_entre_ant_tag ?>">
                        <label for="Altura_tag">Altura del tag</label>
                        <input type="text" class="form-control" name="Altura_tag" id="Altura_tag" value = "<?php echo $datos->Altura_tag ?>">
                        <button class="btn btn-warning mt-3">
                            <i class="fa-regular fa-file-circle-plus"></i> Actualizar
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div> 

<?php include "./scripts.php" ?>