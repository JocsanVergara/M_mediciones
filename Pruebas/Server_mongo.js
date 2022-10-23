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

db.users.find(); // Cursores

// ObjectID ->4
// 1.- (Timestamp)
// 2.- (Identificador para el servidor)
// 3.- (PID)
// 4.- (AutoIncrement)


// Para insertar un documento uso 
db.users.insertOne(user4);

// Si quiero insertar multiples Documentos puedo usar el comando insertMany
db.users.insertMany(
    [
       {'username':'user2',
       'age':27,
       'email':'user2@example.com'},
       {'username':'user3',
       'age':27,
       'email':'user3@example.com'},
       {'username':'user4',
       'age':27,
       'email':'user4@example.com'}, 
    ]
);

// Podemos también usar la función save el cual nos permite ingresar un documento a la coleccion
user5 ={
    'username':'user8',
    'age':56,
    'email':'user8@example.com'
};
db.users.save(user5);
// Si el objeto no existe se crea. (_id)
// Si el objeto existe se actualiza su valor. (_id)

// Como podemos hacer consultas
//Obtener el usuario con username user7

// Retorna un cursor
db.users.find({
    username : 'user7'
});

// Retorna un documento
db.users.findOne({
    username : 'user7'
});

// Obtener todos los usuarios con una edad mayor a 10 (>)
db.users.find({
    age : {$gt :25}
});

// Obtener la cantidad de usuarios con una edad menor a 50 (<)
db.users.find({
    age : {$lt :50}
}).count();

// Obtener todos los usuarios cuya edad mayor a 10 y cuyo estatus sea activo
db.users.find({
    $and: [
        {age : {$gt : 10}},
        {status:'active'}
    ]
});

// Obtener todos los usuarios que no tengan la edad de 11
db.users.find({
    age : {$ne : 11}
});

// Obtener todos los usuarios que tengan por edad: 27 o 40 o 11
db.user.find({
    $or : [
        {age : 27},
        {age : 40},
        {age : 11}
    ]
});

db.user.find({
    age : {$in : [27, 40, 11]}
});

// Obtener todos los usuarios con atributo estatus
// Obtener todos los usuarios con estatus activo
// Obtener todos los usuarios con estatus activo y correo electrónico
// Obtener el usuario con mayor edad
// Obtener a los tres usuarios más jovenes


// Crear una base de datos
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

