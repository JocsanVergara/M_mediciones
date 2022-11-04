<?php include "./header.php"; ?>

<div class="container">
    <div class="row">
        <div class="col">
            <div class="card mt -4">
                <div class="card-body">
                    <a href="index.php" class="btn btn-info">
                        <i class="fa-solid fa-left-long"></i> regresar
                    </a>
                    <h2>Agregar un registro de las antenas</h2>
                    <form action="./procesos/insertar.php" method="post">
                        <label for="hora">Hora</label>
                        <input type="text" class="form-control" name="hora" id="hora" require>
                        <label for="Iden_tag">Identificador del tag</label>
                        <input type="text" class="form-control" name="Iden_tag" id="Iden_tag" require>
                        <label for="RSSI">RSSI</label>
                        <input type="text" class="form-control" name="RSSI" id="RSSI" require>
                        <label for="Ang_azimuth">Angulo de Azimuth</label>
                        <input type="text" class="form-control" name="Ang_azimuth" id="Ang_azimuth" require>
                        <label for="Ang_elevacion">Angulo de Elevacion</label>
                        <input type="text" class="form-control" name="Ang_elevacion" id="Ang_elevacion" require>
                        <label for="Canal">Canal</label>
                        <input type="text" class="form-control" name="Canal" id="Canal" require>
                        <label for="LOS">Linea de vision</label>
                        <input type="text" class="form-control" name="LOS" id="LOS" require>
                        <label for="Altura_ant">Altura de la antena</label>
                        <input type="text" class="form-control" name="Altura_ant" id="Altura_ant" require>
                        <label for="Distancia_entre_ant_tag">Distancia entre la antena y el tag</label>
                        <input type="text" class="form-control" name="Distancia_entre_ant_tag" id="Distancia_entre_ant_tag" require>
                        <label for="Altura_tag">Altura del tag</label>
                        <input type="text" class="form-control" name="Altura_tag" id="Altura_tag" require>
                        <button class="btn btn-primary mt-3">
                            <i class="fa-regular fa-file-circle-plus"></i>  Agregar
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div> 

<?php include "./scripts.php" ?>