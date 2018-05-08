#!/usr/bin/python
'''
clientes = (
    (17,'Sr', 'Afonso', 'da Silva', 'Avenida Acelino de Leao', '89', NULL, '68900 300', 'Macapa', 'AP', '3565 1243', '8765 8999' ,1)
    (18,'Sr', 'Afonso', 'da Silva', 'Avenida Acelino de Leao', '89', NULL, '68900 300', 'BH', 'MG', '3565 1243', '8765 8999' ,1)
)
'''

# Importanto a biblioteca para comunicacao com o postgreSQL
import psycopg2  # sudo apt-get install python-psycopg2

def main():
    print('Vamo!!!')
    connect()


def connect():
    con = None
    """ Tentanto estabelecer a conexao com o banco """

    try:
        print('Conectando com o banco de dados ...')
        con = psycopg2.connect(database="aula", 
        user="postgres", password="banco",host='localhost',port=5432)
        
        # criando um cursor
        cur = con.cursor()

        # executando um select no postgreSQL
        #print('Versao do postgreSQL: ')
        #cur.execute('SELECT version()')
        
        clientes = (
            (17,'Sr', 'Afonso', 'da Silva', 'Avenida Acelino de Leao', '89', 'NULL', '68900 300', 'Macapa', 'AP', '3565 1243', '8765 8999' ,1),
            (18,'Sr', 'Afonso', 'da Silva', 'Avenida Acelino de Leao', '89', 'NULL', '68900 300', 'BH', 'MG', '3565 1243', '8765 8999' ,1)
        )
        

        
        #cur.execute('SELECT id_cliente, nome, sobrenome, endereco  FROM aulas.tb_cliente')
        

        #db_version = cur.fetchone() #aqui so um registro de retorno do select
        #print(db_version)
        
        #rows = cur.fetchall()
        #for row in rows:
        #    print row[0], row[1],row[2]
            #print row
        

        # Inserindo um valor na tabela de cliente
        #cur.execute("INSERT INTO aulas.tb_cliente(id_cliente, titulo, nome, sobrenome, endereco, numero, complemento, cep, cidade, estado, fone_fixo, fone_movel, fg_ativo) " + 
        #"VALUES (17, 'Sr', 'Manoel', 'da Silva', 'Avenida Acelino de Leao', '89', NULL, '68900 300', 'Macapa', 'AP', '3565 1243', '8765 8999' ,1)")
        
        
        query = "INSERT INTO aulas.tb_cliente(id_cliente, titulo, nome, sobrenome, endereco, numero, complemento, cep, cidade, estado, fone_fixo, fone_movel, fg_ativo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print(query)
        cur.executemany(query,clientes)
        # Atualizando o dados na tabela de cliente

        
        # fechando a comunicacao com o postgreSQL --- IMPORTANTE!!!
        
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        # Ja existe uma conexao e sera fechada
        if con is not None:
            con.close()
            print('Conexao com Database fechada!!')

if __name__ == "__main__":
    main()