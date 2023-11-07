class Client():
    def __init__(self, row):
       self._id = row[0]
       self._name = row[1]
       self._id_user = row[2]

    def to_json(self):
        return {
            "id" : self._id,
            "name" : self._name,
            "id_user" : self._id_user,
        } 
    
class Usuario():
    def __init__(self, row):
        self._id = row[0]
        self._name = row[1]
        self._surname = row[2]
        self._age = row[3]
        self._dni = row[4]
        self.password = row[5]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "surname": self._surname,
            "age": self._age,
            "dni": self._dni,
            "password": self.password
        }
