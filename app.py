import subprocess
import time

def run_shell_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"Erro ao executar comando: {command}\nSaída: {result.stdout.decode()}\nErro: {result.stderr.decode()}")
    return result.stdout.decode()

DB_NAME = "meu_banco"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DUMP_FILE = "backup.sql"
CONTAINER_NAME = "postgres_container"
POSTGRES_PASSWORD = "1234"

print("Escolha a opção para o backup:")
print("1. Backup completo do banco de dados")
print("2. Backup limitado por esquema ou tabela")
print("3. Backup limitado por número de linhas")
print("4. Backup limitado por tamanho do arquivo")
opcao = input("Digite o número da opção desejada (1, 2, 3 ou 4): ")

if opcao not in ['1', '2', '3', '4']:
    print("Opção inválida. Executando backup completo do banco de dados...")
    opcao = '1'

if opcao == '1':
    print("Criando dump completo do banco de dados...")
    dump_command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -F c -b -v -f {DUMP_FILE}"
elif opcao == '2':
    schema = input("Digite o nome do esquema ou tabela para o backup limitado: ")
    dump_command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -F c -b -v -f {DUMP_FILE} -n {schema}"
elif opcao == '3':
    table = input("Digite o nome da tabela para o backup limitado por número de linhas: ")
    limit = input("Digite o número máximo de linhas a serem copiadas: ")
    dump_command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -F c -b -v -f {DUMP_FILE} -t {table} --data-only --limit={limit}"
elif opcao == '4':
    file_size_limit = input("Digite o tamanho máximo do arquivo de backup (ex: 1GB): ")
    dump_command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -F c -b -v --file-level-rate={file_size_limit} -f {DUMP_FILE}"

run_shell_command(dump_command)
print("Dump do banco de dados criado com sucesso.")

print("Verificando se o contêiner Docker já existe...")
try:
    run_shell_command(f"docker inspect {CONTAINER_NAME}")
    print(f"Removendo contêiner existente {CONTAINER_NAME}...")
    run_shell_command(f"docker rm -f {CONTAINER_NAME}")
except Exception:
    print(f"Contêiner {CONTAINER_NAME} não existe. Continuando...")

print("Criando contêiner Docker com PostgreSQL...")
docker_run_command = f"docker run --name {CONTAINER_NAME} -e POSTGRES_PASSWORD={POSTGRES_PASSWORD} -d postgres"
run_shell_command(docker_run_command)
print("Contêiner Docker criado com sucesso.")

print("Aguardando o contêiner iniciar...")
time.sleep(10)

print(f"Copiando arquivo de dump para o contêiner {CONTAINER_NAME}...")
docker_cp_command = f"docker cp {DUMP_FILE} {CONTAINER_NAME}:/{DUMP_FILE}"
run_shell_command(docker_cp_command)
print("Arquivo de dump copiado com sucesso.")

print("Restaurando o banco de dados no contêiner...")
restore_command = f"docker exec -i {CONTAINER_NAME} pg_restore -U postgres -d postgres /{DUMP_FILE}"
run_shell_command(restore_command)
print("Banco de dados restaurado com sucesso no contêiner.")

container_ip_command = f"docker inspect -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' {CONTAINER_NAME}"
container_ip = run_shell_command(container_ip_command).strip()

jdbc_url = f"jdbc:postgresql://{container_ip}:5432/{DB_NAME}"
print("\nInformações para conectar via JDBC:")
print(f"URL JDBC: {jdbc_url}")
print(f"Usuário: {DB_USER}")
print(f"Senha: {POSTGRES_PASSWORD}")

with open("credentials.log", "w") as env_file:
    env_file.write(f"connection jdbc = {jdbc_url}\n")
    env_file.write(f"DB_USER = {DB_USER}\n")
    env_file.write(f"DB_PASSWORD = {POSTGRES_PASSWORD}\n")

print("\nUm arquivo 'credentilas.log' foi criado com as informacoes do container")
