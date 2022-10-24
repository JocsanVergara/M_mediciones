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
db.user.find({
    status : {$exists : true}
});

db.user.find({
    status : {$exists : false}
});
//Esto nos permite saber si tienen diferentes atributos --> Es el método principal

// Obtener todos los usuarios con estatus activo
db.users.find({
    status : 'active'
});

db.users.find({
    $and : [
        {status : {$exists : true}},
        {status : 'active'}
    ]
});

// Obtener todos los usuarios con estatus activo y correo electrónico
db.users.find({
    $and : [
        {status : {$exists : true}},
        {status : 'active'},
        {email : {$exists : true}}
    ]
});

// Obtener el usuario con mayor edad
db.users.find().sort({
    age : -1
}).limit(1);

// Obtener a los tres usuarios más jovenes
db.users.find().sort({
    age : 1
}).limit(3);


// Si necesito buscar dentro de un string y no recuerdo o es demasiado largo para anotarlo puedo hacer busquedas con pequeñas secciones del string indicando en que parte del mismo se encuentra
// Esta a comienzo del string con la expresion regular
db.users.find({
    email : /^user/  // user%
});
// Esta al final del string
db.users.find({
    email : /.com$/  // %.com
});
// Si esta en alguna parte del string
db.users.find({
    email : /@/      // %@%
});

// El método find nos entrega un cursor de 20 documentos, si necesito obtener los siguientes elementos entonce anoto en consola el comando it
db.users.find();
it

// ---------------------------------------------------------------------------------------------------------------------------------
// Todos estos métodos son con cursores -> find, sort, limit y skip devuelven cursores y podemos usar los metodos count() y pretty()
// ---------------------------------------------------------------------------------------------------------------------------------
// Puedo contar el número de iteraciones
db.users.find().count();
// Puedo limitar el número de documentos que me entrega el método find() con limit()
db.users.find().limit(5);
// Puedo saltar algunos documentos con el comando skip
db.users.find().skip(5).limit(5);
// Puedo igualmente ordenar los resultados obtenidos de la siguiente manera
db.users.find().sort({age : -1}).skip(5).limit(5); //de esta manera estan ordenados de menor a mayor
// Puedo tener una salidad más amigable con pretty
db.users.find().pretty();

// Puedo asignar a una variable los cursores no obstante una vez se recorra todo el cursor no podemos llamarla nuevamente
var users = db.users.find()
users
it
// despues de terminar las compaginaciones no nos debería mostrar nada

// Se obtienen paulatinamente cada uno de los documentos
db.users.find().forEach( user => print(user.username));

// Proyecciones obtenermos algunos datos que necesitamos solamente
db.users.find(
    {
        age : {$gte : 50}
    },  //definimos las condiciones
    {
        _id : false,
        username : true,
        email : true,
        age : true
    }
);

// Modificar o actualizar un documento
// 1.- Save
var user = db.users.findOne();
user
user.age = 28
user.email = 'user1@codigofacilito.com'
// con esto añadimos un nuevo elemento a la colección
user.status = 'active'

// En este caso tendremos lo siguiente
db.users.save(user);

// 2.-update
db.users.update(
    {
        "_id" : objectId()
    }, // Condicion que debe cumplir el documento
    {
        $set :{
            username : 'Cody',
            email : 'codigo@facilito.com',
            profile_picture : 'www.codigofacilito.com/user1'
        }
    } // Cambios a realizar, de no existir se crea dentro del documento el objeto(valor o atributo)
);

db.users.update(
    {
        "_id" : objectId()
    }, // Condicion que debe cumplir el documento
    {
        $unset :{
            profile_picture : 'www.codigofacilito.com/user1'
        }
    } // con unset podemos eliminar una condición
);

db.users.update(
    {
        status : 'inactive'
    },
    {
        $set : {
            status : 'active'
        }
    },
    {
        multi : true
    }
);

// updateOne
db.users.updateOne(
    {
        "status" : "active"
    },
    {
        $set : {
            status : 'inactive'
        }
    }
);
// updateMany
db.users.updateMany(
    {
        email : {$exists : true}
    },
    {
        $set : {
            bio : "añade tu biografía"
        }
    }
);

// Para incrementar la edad de todo los documentos en 1
db.users.updateMany(
    {},
    {
        $inc : {
            age : 1
        }
    }
);

// remove
db.users.remove({
    status : 'inactive'
}); // paso una condición

// ten cuidado si no añades una condición se borra todo los documentos
db.users.remove();

// Eliminamos la collection
db.users.drop();

// Eliminamos la base de datos
db.dropDatabase();

user13 = {
    'username' : 'user13',
    'email' : 'user13@example.com',
    'age' : 29,
    'status' : 'active',
    'address' : {
        'zip' : 1001,
        'country' : 'MX'
    },
    'courses' : ['Python','MongoDb','Ruby','Java'],
    'comments' : [
        {
            body : 'Best course',
            like : true,
            tags : ['MongoDB']
        },
        {
            body : 'Super excited',
            like : true
        },
        {
            body : 'The course is ok'
        },
        {
            body : 'Bad course, Im disappointed',
            like : false,
            tags : ['bad','course','MongoDb']
        }
    ]
};

user14 = {
    'username' : 'user14',
    'email' : 'user14@example.com',
    'age' : 29,
    'status' : 'active',
    'comments' : [
        {
            body : 'Best course',
            like : false
        }
    ],
    'address' : {
        'zip' : 1001,
        'country' : 'MX',
        'location' : {
            'lat' : 109,
            'long' : -150
        }
    }
};

db.users.insertMany([user13,user14]);

// Obtener todos los usuarios que radiquen en Mexico
db.users.find(
    {
        'address.country' : 'MX'
    }
);

// Si quiero obtener un documento anidado dos veces, además de solo obtener como salida de la consulta el usuario y el zip
db.users.find(
    {
        'address.location.lat' : 109  // dot notation
    },
    {
        username : true,
        'address.zip' : true
    }
);

// Actualizar el código postal
db.users.updateMany(
    {
        'address.zip' : {$exists : true}
    },
    {
        $set : {
            'address.zip' : 110
        }
    }
);

// Añadir dirección a todos los usuarios que no la posean.
db.users.updateMany(
    {
        'address' : {$exits : false}
    },
    {
        $set :{
            'address':{
                country : 'CLP',
                zip : 2017
            }
        }
    }
);

db.users.updateOne(
    {
        username : 'user 3'
    },
    {
        $set : {
            'address.location':{
                lat : -180,
                long : 250
            }
        }
    }
);

// Obtener todos los usuarios que tengan en su listado de cursos Python
// Obtener todos los usuarios con por lo menos un comentario positivo

// $elemMatch Nos permite filtrar sobre attrs. de documentos dentro de listados.
db.users.find(
    {
        comments : {
            $elemMatch : {
                like : true
            }
        }
    }
);

db.users.find(
    {
        comments : {
            $elemMach : {
                $and : [
                    {like : true},
                    {tags : {$exists : true}}
                ]
            }
        }
    },
    {
        comments : true
    }
);

// Añadir un nuevo comentario positivo al listado de comentarios para el usurios 1
db.users.updateOne(
    {
        username : 'user4'
    },
    {
        $push : {
            comments : {
                like : true,
                body : 'El curso de MongoDB me está Gustando'
            }
        }
    }
);

db.users.updateOne(
    {
        username : 'user4'
    },
    {
        $push : {
                courses : 'Rust'
            }
    }
);

// Anade una nueva etiqueta el comentario 4 del usuario 11
db.users.updateOne(
    {
        username : 'user13'
    },
    {
        $push : {
            'comments.3.tags' : 'Tutor'
        }
    }
);
// Actualizar el segundo comentario del usuario 11
db.users.updateOne(
    {
        username : 'user13'
    },
    {
        $set : {
            'comments.1.body' : 'Me esta gustando el curso'
        }
    }
);
// Actualiza el comentario negativo del usuario 11
db.users.updateOne(
    {
        username : 'username13',
        'comments.like' :false
    },
    {
        $set :{
            'comments.$.body' : 'El curso si me esta gustando',
            'comments.$.like' : true
        },
        $unset : {
            'comments.$.tags' : true
        }
    }
);

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Crear una base de datos
//use Nombre
//db
//show dbs

// Crear una coleccion
db.usuario.insert(
{
	"cedula":"0926448614",
	"name":"Leonardo Kuffo",
	"clave":"12345678",
	"pais":"Ecuador",
}
)
//show collections

// Crear una coleccion de forma implicita
db.createCollection("productos")

// Eliminar una colección
db.Nombre_coleccion.drop()

// Eliminar una base de datos
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


// Eliminar un documento
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


//menor que: $lt
//menor o igual que: $lte
//mayor que: $gt
//mayor o igual que: $gte
//No es igual: $ne
//AND: {{key:value1, key2:value2}}
//OR: {
//$or: [{key1:value1},{key2:value2}]
//}
//AND + OR: { key1:value1 ,  $or:[{{key2:value2},{key3:value3}}]

db.productos.find().sort({valor:1}) //1 de menor a mayor -1 es de mayor a menor

