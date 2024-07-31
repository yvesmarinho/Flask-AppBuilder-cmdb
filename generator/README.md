# Projeto de Gerador de código 

Projeto de um gerador de código para automatizar o processo de criação de novos projetos baseados em Flask AppBuilder.

Esse gerador é utilizado quando se tem a estrutura do banco de dados pronta.

Terá as seguintes etapas:

- ler arquivo config.ini para coletar informações da conexão de banco de dados, com a sessão database com os seguintes parãmetros: db_type (mysql, postgres), db_host_id, db_port, db_name (>=1 db), db_user, db_password,  db_charset(Optional)

- ler o banco de dados e transofkmar em json.

- Baseado no Flask AppBuilder, gerar o model.py com o JSON da estrutura do banco de dados.

-  Baseado no Flask AppBuilder, gerar o views.py com o JSON da estrutura do banco de dados, não esquecer de nos campos com relacionamento colocar um combo para selecionar o item da outra tabela.

- Baseado no Flask AppBuilder, gerar o validator.py com o JSON.

- Gerar demais códigos que seja necessários para que o Flask AppBuilder fique funcional.