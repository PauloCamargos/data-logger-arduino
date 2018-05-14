CREATE OR REPLACE FUNCTION aula08.fn_soma(real, real) RETURNS real AS
$$
    BEGIN
        RETURN $1 + $2;
    END
$$
LANGUAGE plpgsql;

SELECT aula08.fn_soma2(4,5);

-- Declarando variaveis
CREATE OR REPLACE FUNCTION aula08.fn_soma2(real, real) RETURNS real AS
$$
    DECLARE
        var1 ALIAS for $1;
        var2 ALIAS for $2;
    BEGIN
        RETURN var1 + var2;
    END
$$
LANGUAGE plpgsql;

SELECT aula08.fn_soma2(4,5);

-- Na chamada
CREATE OR REPLACE FUNCTION aula08.fn_soma3(pvar1 real,pvar2 real) RETURNS real AS
$$
    BEGIN
        RETURN pvar1 + pvar2;
    END
$$
LANGUAGE plpgsql;

SELECT aula08.fn_soma3(4,5);

-- Retornar string
CREATE OR REPLACE FUNCTION aula08.fn_soma3_ret_str(real, real) RETURNS varchar AS
$$
    DECLARE
        pSoma real;
    BEGIN
        pSoma = $1 + $2;
        RETURN 'O valor da soma -> ' || pSoma;
    END
$$
LANGUAGE plpgsql;

SELECT aula08.fn_soma3_ret_str(4,5);


-- Retornar nome do cliente %Type
CREATE TABLE aula08.tb_cliente(
    id_cliente  SERIAL PRIMARY KEY,
    nome VARCHAR(64)
);
INSERT INTO aula08.tb_cliente(nome) VALUES('Italo');
INSERT INTO aula08.tb_cliente(nome) VALUES('João');

SELECT * FROM aula08.tb_cliente;

CREATE OR REPLACE FUNCTION aula08.fn_ret_nome_cliente(integer) RETURNS varchar AS
$$
    DECLARE
        v_nome aula08.tb_cliente.nome%TYPE;
    BEGIN
        SELECT nome INTO v_nome FROM aula08.tb_cliente WHERE id_cliente = $1;
        RETURN 'Nome do cliente -> ' || v_nome;
    END
$$
LANGUAGE plpgsql;

SELECT * FROM aula08.fn_ret_nome_cliente(1);

-- Retornar varios clientes %RowType
CREATE OR REPLACE FUNCTION aula08.fn_ret_nome_cliente_tupla(integer) RETURNS varchar AS
$$
    DECLARE
        v_tupla aula08.tb_cliente%ROWTYPE;
    BEGIN
        SELECT * INTO v_tupla FROM aula08.tb_cliente WHERE id_cliente = $1;
        RETURN 'Tupla (linha): -> ' || v_tupla;
    END
$$
LANGUAGE plpgsql;

SELECT * FROM aula08.fn_ret_nome_cliente_tupla(1);

-- Outro ROWTYPE
DROP FUNCTION aula08.fn_ret_nome_cliente_tupla;
CREATE OR REPLACE FUNCTION aula08.fn_ret_nome_cliente_tupla(integer) RETURNS text AS
$$
    DECLARE
        v_tupla aula08.tb_cliente%ROWTYPE;
    BEGIN
        SELECT * INTO v_tupla FROM aula08.tb_cliente WHERE id_cliente = $1;
        RETURN 'Tupla (linha): -> ' || v_tupla;
    END
$$
LANGUAGE plpgsql;

SELECT * FROM aula08.fn_ret_nome_cliente_tupla(1);

-- Outro ROWTYPE
DROP FUNCTION aula08.fn_ret_nome_cliente_tupla;
CREATE OR REPLACE FUNCTION aula08.fn_ret_nome_cliente_tupla(integer) RETURNS text AS
$$
    DECLARE
        v_tupla RECORD;
    BEGIN
        SELECT id_cliente, nome INTO v_tupla FROM aula08.tb_cliente WHERE id_cliente = $1;
        RETURN 'Tupla (linha): -> ' || v_tupla;
    END
$$
LANGUAGE plpgsql;

SELECT * FROM aula08.fn_ret_nome_cliente_tupla(1);



-- Retornar varios clientes %RECORD
CREATE OR REPLACE FUNCTION
aula08.fn_ret_nome_cliente_record(aula08.tb_cliente.id_cliente%TYPE)
RETURNS text AS
$$
    DECLARE
        v_linha RECORD;
    BEGIN
        SELECT * INTO v_linha FROM aula08.tb_cliente WHERE id_cliente = $1;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Cliente % não encontrado ', $1;
        ELSE
            RETURN 'Cliente encontrado!!';
        END IF;
    END
$$
LANGUAGE plpgsql;

SELECT * FROM aula08.fn_ret_nome_cliente_record(1);
SELECT * FROM aula08.fn_ret_nome_cliente_record(10);
