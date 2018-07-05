from pymongo import *
client = MongoClient('localhost', 27017)  # Iniciando a conexão com o banco
db = client.datalogger  # Acessando a Collection "datalogger"

def main():
    # ----------------- INSERINDO USUARIOS
    usuarios = [
        {
            username: "thiago@ufu.br",
            fullname: "Thiago Pereira Oliveira",
            status: "Ativo",
            password: "thiagoufu"
        },
        {
            username: "paulo@ufu.br",
            fullname: "Paulo Camargos Silva",
            status: "Ativo",
            password: "pauloufu"
        },
        {
            username: "marcio@ufu.br",
            fullname: "Marcio Cunha",
            status: "Ativo",
            password: "marcioufu"
        }
    ]
    users = db.users
    users.insert_many(usuarios)

    # ----------------- INSERINDO AMBIENTES

    ambientes = [
        {
            description: "Ar"
        },
        {
            description: "Água"
        },
        {
            description: "Solo"
        }
    ]
    environments = db.environments
    environments.insert_many(ambientes)

    # ----------------- INSERINDO GRANDEZAS

    grandezas = [
        {
            type: "Temperatura",
            unity: "°C"
        },
        {
            type: "Temperatura",
            unity: "F"
        },
        {
            type: "Umidade",
            unity: "%"
        }
    ]
    physical_quantity = db.physical_quantity
    physical_quantity.insert_many(grandezas)


if __name__ == "__main__":
    main()
