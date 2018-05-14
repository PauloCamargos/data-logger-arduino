CREATE OR REPLACE FUNCTION aula08.fn_soma(real, real) RETURNS real AS
$$
    BEGIN
        RETURN $1 + $2;
    END
$$
LANGUAGE plpgsql;

SELECT aula08.fn_soma2(4,5)


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

SELECT aula08.fn_soma2(4,5)
