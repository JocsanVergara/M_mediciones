 //Crear un documento
 // Documento -> Objetos de tipo JSON

 user1 ={
    'username':'user1',
    'age':27,
    'email':'user1@example.com'
 }
// Se valida que la base de datos exista.
// Se valida que la colección exitosa.
 db.users.insert(user1)



 -- Crear una base de datos
use Nombre
db
show dbs

-- Crear una coleccion
db.usuario.insert(
{
	"cedula":"0926448614",
	"name":"Leonardo Kuffo",
	"clave":"12345678",
	"pais":"Ecuador",
}
)
show collections

-- Crear una coleccion de forma implicita
db.createCollection("productos")

-- Eliminar una colección
db.Nombre_coleccion.drop()

-- Eliminar una base de datos
db.dropDatabase()



db.productos.insert(
{
	"id":"1",
	"name":"Camiseta S",
	"valor":18.0,
	"stock":2,
}
)

db.productos.find().pretty()


db.productos.update(
{
	"id":"1"
},
{
	$set:{'valor':20.45}
}
)


-- Eliminar un documento
db.productos.deleteOne({
	"id":"1"
})

db.productos.find(
{
 "valor":15.0
})

db.productos.find(
{
"valor":{$lt:16.0}
})


menor que: $lt
menor o igual que: $lte
mayor que: $gt
mayor o igual que: $gte
No es igual: $ne
AND: {{key:value1, key2:value2}}
OR: {
$or: [{key1:value1},{key2:value2}]
}
AND + OR: { key1:value1 ,  $or:[{{key2:value2},{key3:value3}}]

db.productos.find().sort({valor:1}) //1 de menor a mayor -1 es de mayor a menor

