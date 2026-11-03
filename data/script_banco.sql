CREATE TABLE modulos_aurora (
    id_modulo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_modulo VARCHAR2(50),
    consumo_energia FLOAT,
    status_operacional VARCHAR2(30)
);