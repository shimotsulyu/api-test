USE Base

CREATE TABLE Produtos (
    id integer not null auto_increment,
    produto varchar(100),
    custo float,
    venda float,
    PRIMARY KEY (id)
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_result = utf8;
SET collation_connection = utf8_general_ci;