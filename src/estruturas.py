class EstruturasSIFSM:
    def __init__(self):
        # 1. Tabela Hash (Dicionário em Python) - Busca Rápida
        self.modulos_cadastrados = {}
        
        # 2. Fila (Queue - FIFO) - Ordem de Atendimento
        self.fila_manutencao = []
        
        # 3. Pilha (Stack - LIFO) - Histórico de Ações (Desfazer)
        self.historico_acoes = []

    def cadastrar_modulo_hash(self, codigo, nome):
        """Usa a chave (código) para acesso direto e rápido."""
        self.modulos_cadastrados[codigo] = nome
        acao = f"Módulo cadastrado: {codigo} - {nome}"
        self.registrar_historico(acao)
        print(f"Sucesso: {acao}")

    def buscar_modulo(self, codigo):
        """Busca rápida O(1) usando Tabela Hash."""
        modulo = self.modulos_cadastrados.get(codigo)
        if modulo:
            print(f"Módulo Encontrado: {modulo}")
        else:
            print("Erro: Módulo não localizado.")

    def enfileirar_chamado(self, chamado):
        """Insere um alerta/chamado no final da fila (FIFO)."""
        self.fila_manutencao.append(chamado)
        acao = f"Chamado aberto: {chamado}"
        self.registrar_historico(acao)
        print(f"Fila atualizada: '{chamado}' adicionado.")

    def atender_chamado_fila(self):
        """Remove e atende o chamado do início da fila."""
        if not self.fila_manutencao:
            print("Nenhum chamado de manutenção na fila.")
            return None
        
        chamado_atendido = self.fila_manutencao.pop(0)
        acao = f"Chamado finalizado: {chamado_atendido}"
        self.registrar_historico(acao)
        print(f"Atendimento concluído: {chamado_atendido}")
        return chamado_atendido

    def registrar_historico(self, acao):
        """Empilha uma ação no histórico (LIFO)."""
        self.historico_acoes.append(acao)

    def desfazer_ultima_acao(self):
        """Remove a última ação registrada no topo da pilha."""
        if not self.historico_acoes:
            print("Histórico vazio. Nenhuma ação para desfazer.")
            return None
        
        acao_desfeita = self.historico_acoes.pop()
        print(f"Desfazendo ação mais recente: {acao_desfeita}")
        return acao_desfeita

    def exibir_hash(self):
        """Exibe o estado atual da Tabela Hash."""
        print(self.modulos_cadastrados)

    def exibir_fila(self):
        """Exibe o estado atual da Fila."""
        print(self.fila_manutencao)

if __name__ == "__main__":
    print("--- SIFSM: Inicializando Estruturas de Dados ---")
    sistema = EstruturasSIFSM()
    
    # Testando Tabela Hash
    sistema.cadastrar_modulo_hash(101, "Habitação Alpha")
    sistema.cadastrar_modulo_hash(202, "Laboratório Botânico")
    sistema.buscar_modulo(202)
    
    # Testando Fila de Manutenção
    sistema.enfileirar_chamado("Vazamento de Oxigênio")
    sistema.enfileirar_chamado("Falha no Painel Solar")
    sistema.atender_chamado_fila()
    
    # Testando Pilha de Histórico
    sistema.desfazer_ultima_acao()