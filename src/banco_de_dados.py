import oracledb
import pandas as pd

# Configurações de conexão 
USER = 'rm570889'
PASSWORD = '040907'
DSN = 'oracle.fiap.com.br:1521/ORCL'

def conectar():
    """Estabelece e retorna a conexão com o banco de dados Oracle."""
    try:
        conn = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
        return conn
    except Exception as e:
        print(f"Erro de conexão circunstancial com o servidor Oracle: {e}")
        return None

def cadastrar_modulo(nome, consumo, status):
    """CREATE: Insere um novo módulo aplicando tratamento completo de erros."""
    conn = conectar()
    if not conn: return

    try:
        inst_cadastro = conn.cursor()
        # Utilizando f-strings para montar a instrução SQL conforme ensinado
        cadastro = f"""INSERT INTO modulos_aurora (nome_modulo, consumo_energia, status_operacional) 
                       VALUES ('{nome}', {consumo}, '{status}')"""
        
        inst_cadastro.execute(cadastro)
        
    except ValueError as erroValor:
        print(f"ERRO! Digite um valor numérico para o consumo.")
    except oracledb.DatabaseError as erroDB:
        print(f"ERRO! Falha na transação com o banco de dados: {erroDB}.")
    else:
        # O else executa apenas se não houver erro no try
        conn.commit()
        print(f"\n[SUCESSO] Módulo '{nome}' gravado na Aurora Siger!")
    finally:
        # O finally executa independentemente de erro
        if 'inst_cadastro' in locals():
            inst_cadastro.close()
        conn.close()

def listar_modulos():
    """READ: Lista todos os registros utilizando a biblioteca Pandas."""
    conn = conectar()
    if not conn: return

    try:
        inst_consulta = conn.cursor()
        inst_consulta.execute("SELECT id_modulo, nome_modulo, consumo_energia, status_operacional FROM modulos_aurora")
        data = inst_consulta.fetchall()
        
        lista_dados = []
        for dt in data:
            lista_dados.append(dt)
            
        # Ordenação e criação do DataFrame para exibição formatada
        lista_dados = sorted(lista_dados)
        dados_df = pd.DataFrame.from_records(
            lista_dados, 
            columns=['ID', 'Módulo', 'Consumo (kW)', 'Status'], 
            index='ID'
        )
        
        if dados_df.empty:
            print("Não há módulos cadastrados na base de dados.")
        else:
            print("\n--- STATUS DOS MÓDULOS AURORA SIGER ---")
            print(dados_df)
            
    except Exception as e:
        print(f"Erro ao listar os dados: {e}")
    finally:
        inst_consulta.close()
        conn.close()

def alterar_modulo(id_modulo, novo_consumo, novo_status):
    """UPDATE: Consulta a existência do registro e altera seus dados."""
    conn = conectar()
    if not conn: return
        
    try:
        inst_alteracao = conn.cursor()
        
        # Consulta singular para verificar se o ID existe antes de alterar
        consulta = f"SELECT * FROM modulos_aurora WHERE id_modulo = {id_modulo}"
        inst_alteracao.execute(consulta)
        if len(inst_alteracao.fetchall()) == 0:
            print(f"Não há um módulo cadastrado com o ID = {id_modulo}.")
            return
            
        alteracao = f"""UPDATE modulos_aurora 
                        SET consumo_energia = {novo_consumo}, status_operacional = '{novo_status}' 
                        WHERE id_modulo = {id_modulo}"""
        inst_alteracao.execute(alteracao)
        conn.commit()
        print("\nDados do módulo ATUALIZADOS com sucesso!")
        
    except oracledb.DatabaseError as erroDB:
        print(f"Erro na transação do BD: {erroDB}")
    finally:
        inst_alteracao.close()
        conn.close()

def excluir_modulo(id_modulo_str):
    """DELETE: Exclui o registro após validar se o ID digitado é numérico."""
    # Validação do tipo de dado sem try/except, utilizando isdigit()
    if not id_modulo_str.isdigit():
        print("O Id não é numérico!")
        return

    id_modulo = int(id_modulo_str)
    conn = conectar()
    if not conn: return

    try:
        inst_exclusao = conn.cursor()
        
        consulta = f"SELECT * FROM modulos_aurora WHERE id_modulo = {id_modulo}"
        inst_exclusao.execute(consulta)
        
        if len(inst_exclusao.fetchall()) == 0:
            print(f"Não há um módulo cadastrado com o ID = {id_modulo}.")
        else:
            exclusao = f"DELETE FROM modulos_aurora WHERE id_modulo = {id_modulo}"
            inst_exclusao.execute(exclusao)
            conn.commit()
            print("\nMódulo APAGADO com sucesso!")
            
    except oracledb.DatabaseError as erroDB:
        print(f"Erro na transação do BD: {erroDB}")
    finally:
        inst_exclusao.close()
        conn.close()