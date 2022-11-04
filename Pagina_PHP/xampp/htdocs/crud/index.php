<?php session_start();
    require_once "./clases/Conexion.php";
    require_once "./clases/Crud.php";
    $crud = new Crud();
    $datos = $crud->mostrarDatos();

    $mensaje = '';
    if (isset($_SESSION['mensaje_crud'])) {
        $mensaje = $crud->mensajeCrud($_SESSION['mensaje_crud']);
        unset($_SESSION['mensaje_crud']);
    }

?>


<?php include "./header.php"; ?>

<div class="container">
    <div class="row">
        <div class="col">
            <div class="card mt -4">
                <div class="card-body">
                    <h2>Datos obtenidos de las antenas</h2>
                    <a href="./agregar.php" class="btn btn-primary">
                        <i class="fa-solid fa-plus"></i>  Agregar un nuevo registro
                    </a>
                    <hr>
                    <table class="table table-sm table-hover table-bordered">
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
                            <th>Editar</th>
                            <th>Eliminar</th>
                        </thead>
                        <tbody>
                            <?php
                                foreach($datos as $item) {
                            ?>
                            <tr>
                                <td> <?php echo $item->hora; ?> </td>
                                <td> <?php echo $item->Iden_tag; ?> </td>
                                <td> <?php echo $item->RSSI; ?> </td>
                                <td> <?php echo $item->Ang_azimuth; ?> </td>
                                <td> <?php echo $item->Ang_elevacion; ?> </td>
                                <td> <?php echo $item->Canal; ?> </td>
                                <td> <?php echo $item->LOS; ?> </td>
                                <td> <?php echo $item->Altura_ant; ?> </td>
                                <td> <?php echo $item->Distancia_entre_ant_tag; ?> </td>
                                <td> <?php echo $item->Altura_tag; ?> </td>
                                <td class="text-center">
                                    <form action="./actualizar.php" method="post">
                                        <input type="text" hidden value = "<?php echo $item->_id ?>" name = "id">
                                        <button class="btn btn-warning">
                                            <i class="fa-solid fa-pen-clip"></i> Editar
                                        </button>
                                    </form>
                                </td>
                                <td class="text-center">
                                    <form action="./eliminar.php" method="post">
                                        <input type="text" hidden value = "<?php echo $item->_id ?>" name = "id">
                                        <button class="btn btn-danger">
                                            <i class="fa-solid fa-trash"></i> Eliminar
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div> 

<?php include "./scripts.php" ?>

<script>
    let mensaje = <?php echo $mensaje; ?>;
    console.log(mensaje);
</script>
