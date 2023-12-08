CREATE TABLE IF NOT EXISTS "pedido" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "valor_total" real NOT NULL, 
    "quantidade_total" bigint unsigned NOT NULL CHECK ("quantidade_total" >= 0), 
    "status" varchar(1) NOT NULL, 
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "itempedido" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "produto" varchar(255) NOT NULL, 
    "produto_id" integer unsigned NOT NULL CHECK ("produto_id" >= 0), 
    "variacao" varchar(255) NOT NULL, 
    "variacao_id" integer unsigned NOT NULL CHECK ("variacao_id" >= 0), 
    "preco" real NOT NULL, 
    "promo" real NOT NULL, 
    "quantidade" integer unsigned NOT NULL CHECK ("quantidade" >= 0), 
    "imagem" varchar(2000) NOT NULL, 
    "pedido_id" bigint NOT NULL REFERENCES 
    "pedido_pedido" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "pedido_pedido_user_id_16627dad" ON "pedido_pedido" ("user_id");
CREATE INDEX "pedido_itempedido_pedido_id_15c6b42d" ON "pedido_itempedido" ("pedido_id");

CREATE TABLE IF NOT EXISTS "perfil" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "idade" integer unsigned NOT NULL CHECK ("idade" >= 0), 
    "data_nascimento" date NOT NULL, 
    "cpf" varchar(11) NOT NULL, 
    "endereco" varchar(50) NOT NULL, 
    "numero" varchar(5) NOT NULL, 
    "complemento" varchar(30) NOT NULL, 
    "bairro" varchar(30) NOT NULL, 
    "cep" varchar(8) NOT NULL, 
    "cidade" varchar(30) NOT NULL, 
    "estado" varchar(2) NOT NULL, 
    "usuario_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "categoria" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "categoria" varchar(255) NOT NULL, 
    "slug" varchar(50) NULL UNIQUE);

CREATE TABLE IF NOT EXISTS "produto" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "nome" varchar(255) NOT NULL, 
    "descricao_curta" text NOT NULL, 
    "descricao_longa" text NOT NULL, 
    "imagem" varchar(100) NULL, 
    "slug" varchar(50) NULL UNIQUE, 
    "preco" real NOT NULL, 
    "preco_promocional" real NOT NULL,
    "tipo" varchar(1) NOT NULL, 
    "categoria_id" bigint NULL REFERENCES "categoria" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS "variacao" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "nome" varchar(50) NULL, 
    "preco" real NOT NULL, 
    "preco_promocional" real NOT NULL, 
    "estoque" integer unsigned NOT NULL CHECK ("estoque" >= 0), 
    "produto_id" bigint NOT NULL REFERENCES "produto" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "produto_produto_categoria_id_9747952b" ON "produto" ("categoria_id");
CREATE INDEX "produto_variacao_produto_id_45444889" ON "variacao" ("produto_id");

