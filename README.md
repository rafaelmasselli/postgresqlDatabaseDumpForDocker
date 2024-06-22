## Script Python para Backup e Restauração de Banco de Dados PostgreSQL em Contêiner Docker

### Descrição

Este script Python foi desenvolvido para automatizar o processo de backup e restauração de um banco de dados PostgreSQL hospedado dentro de um contêiner Docker. Ele oferece opções para realizar backups completos ou limitados, conforme as necessidades do usuário.

### Pré-requisitos

Antes de executar este script, certifique-se de que você tenha:

- Docker instalado e configurado na sua máquina.
- PostgreSQL client (`pg_dump` e `pg_restore`) instalado e acessível no seu ambiente.
- Python 3.x instalado para executar o script Python.

### Configuração

1. **Variáveis no Script:**

   No início do script (`app.py`), você encontrará as seguintes variáveis que devem ser configuradas conforme o seu ambiente:

```python
DB_NAME = "meu_banco" # Nome do banco de dados PostgreSQL
DB_USER = "postgres" # Usuário do PostgreSQL
DB_HOST = "localhost" # Host onde o PostgreSQL está rodando (geralmente localhost)
DB_PORT = "5432" # Porta do PostgreSQL
DUMP_FILE = "backup.sql" # Nome do arquivo de dump a ser gerado
CONTAINER_NAME = "postgres_container" # Nome do contêiner Docker onde o PostgreSQL será executado
POSTGRES_PASSWORD = "1234" # Senha do usuário postgres do PostgreSQL
Ajuste essas variáveis de acordo com as configurações do seu ambiente PostgreSQL e Docker.
Instalação de Dependências:

Certifique-se de ter as bibliotecas necessárias do Python instaladas. Você pode instalá-las usando pip:
```

```bash
pip install subprocess
```

**Nota**: Se você estiver usando um ambiente virtual (`virtualenv`), ative-o antes de instalar as dependências.

### Utilização

Para usar o script, siga os passos abaixo:

1.  Escolha do Tipo de Backup:

    Execute o script e escolha uma das opções de backup disponíveis:

    - Backup completo do banco de dados.
    - Backup limitado por esquema ou tabela.
    - Backup limitado por número de linhas.
    - Backup limitado por tamanho do arquivo.

    O script solicitará informações adicionais dependendo da opção escolhida (por exemplo, nome do esquema/tabela, número de linhas, tamanho do arquivo).

2.  Execução do Script:

    Após selecionar a opção desejada, o script realizará as seguintes etapas:

    - Criar um dump do banco de dados PostgreSQL.
    - Criar um contêiner Docker com PostgreSQL (se não existir).
    - Aguardar o contêiner iniciar.
    - Copiar o arquivo de dump para o contêiner Docker.
    - Restaurar o banco de dados no contêiner Docker.
    - Exibir informações para conexão via JDBC, incluindo a URL JDBC, usuário e senha.

3.  Conexão via JDBC:

    Use as informações fornecidas pelo script para conectar seu aplicativo Java ou outro cliente que utilize JDBC ao banco de dados PostgreSQL dentro do contêiner Docker.

### Exemplo de Uso

```bash
python app.py
```

Isso iniciará o script e você poderá escolher o tipo de backup que deseja realizar conforme as opções apresentadas.
