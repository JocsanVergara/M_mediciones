<?php 
    include "./clases/Conexion.php";
    include "./clases/Crud.php";
    include "./header.php"; 
?>

<?php
    $crud = new Crud();
    $id = $_POST['id'];
    $datos = $crud -> obtenerDocumento($id);
?>


<div class="container">
    <div class="row">
        <div class="col">
            <div class="card mt-4 fondoDelete">
                <div class="card-body">
                    <a href="index.php" class="btn btn-info">
                        <i class="fa-solid fa-left-long"></i> regresar
                    </a>
                    <h2>Eliminar el registro seleccionad</h2>
                    <table class="table table-bordered">
                        <thead>
                            <th>Hora</th>
                            <th>Tag</th>
                            <th>RSSI</th>
                            <th>Angulo de Azimuth</th>
                            <th>Angulo de Elevación</th>
                            <th>Canal</th>
                            <th>LOS</th>
                            <th>Altura de la antena</th>
                            <th>Distancia entre la antena y el tag</th>
                            <th>Altura del tag</th>
                        </thead>
                        <tbody>
                            <tr>
                                <th> <?php echo $datos->hora; ?> </th>
                                <th> <?php echo $datos->Iden_tag; ?> </th>
                                <th> <?php echo $datos->RSSI; ?> </th>
                                <th> <?php echo $datos->Ang_azimuth; ?> </th>
                                <th> <?php echo $datos->Ang_elevacion; ?> </th>
                                <th> <?php echo $datos->Canal; ?> </th>
                                <th> <?php echo $datos->LOS; ?> </th>
                                <th> <?php echo $datos->Altura_ant; ?> </th>
                                <th> <?php echo $datos->Distancia_entre_ant_tag; ?> </th>
                            </tr>
                        </tbody>
                    </table>
                    <hr>
                    <div class="alert alert-danger" role="alert">
                        <p>¿Esta seguro que quieres eliminar este registro?</p>    
                        <p>Una vez eliminado no se podra recuperar</p>
                    </div>
                    <form action="./procesos/eliminar.php" method="post">
                        <input type="text" name="id" value="<?php echo $datos->_id; ?>" hidden>
                        <button class="btn btn-danger">
                            <i class="fa-solid fa-trash"></i>  Eliminar
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div> 

<?php include "./scripts.php" ?>