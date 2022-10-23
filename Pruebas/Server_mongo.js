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