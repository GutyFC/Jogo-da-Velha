import random

# Função para imprimir o tabuleiro no console
def imprimir_tabuleiro(tabuleiro):
    print("\nTabuleiro atual:")
    print("  0 1 2")  # Cabeçalho das colunas
    for idx, linha in enumerate(tabuleiro):
        print(idx, " ".join(linha))  # Cabeçalho das linhas seguido do conteúdo da linha
    print()

# Função para verificar se há um vencedor
def verificar_vencedor(tabuleiro, jogador):
    # Verifica linhas
    for linha in tabuleiro:
        if all([celula == jogador for celula in linha]):
            return True
    # Verifica colunas
    for col in range(3):
        if all([tabuleiro[linha][col] == jogador for linha in range(3)]):
            return True
    # Verifica diagonais
    if all([tabuleiro[i][i] == jogador for i in range(3)]) or all([tabuleiro[i][2-i] == jogador for i in range(3)]):
        return True
    return False

# Função para verificar se o tabuleiro está cheio (empate)
def tabuleiro_cheio(tabuleiro):
    return all([celula != ' ' for linha in tabuleiro for celula in linha])

# Função para realizar a jogada do jogador
def jogada_jogador(tabuleiro, linha, coluna, jogador):
    while True:
        try:
            linha = int(linha)
            coluna = int(coluna)
            # Verifica se a linha e a coluna estão dentro dos limites do tabuleiro
            if 0 <= linha <= 2 and 0 <= coluna <= 2:
                # Verifica se a célula está vazia
                if tabuleiro[linha][coluna] == ' ':
                    tabuleiro[linha][coluna] = jogador  # Marca a célula com o símbolo do jogador
                    break
                else:
                    print("Esta célula já está ocupada. Escolha outra célula.")
            else:
                print("Entrada inválida. Digite números entre 0 e 2.")
        except ValueError:
            print("Entrada inválida. Digite números inteiros entre 0 e 2.")
        
        # Pedir a entrada do usuário novamente
        linha = input("Digite a linha (0, 1 ou 2): ")
        coluna = input("Digite a coluna (0, 1 ou 2): ")

# Função para realizar a jogada do computador usando a heurística ajustada
def jogada_computador(tabuleiro, jogador_computador, jogador_humano):
    # Verifica se há alguma jogada que leve à vitória imediata
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] == ' ':
                tabuleiro[linha][coluna] = jogador_computador
                if verificar_vencedor(tabuleiro, jogador_computador):
                    tabuleiro[linha][coluna] = jogador_computador  # Realiza a jogada para vencer
                    print(f"O computador escolheu a posição ({linha}, {coluna})")
                    return linha, coluna

                tabuleiro[linha][coluna] = ' '  # Desfaz a jogada

    # Verifica se há alguma jogada que bloqueie a vitória do jogador
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] == ' ':
                tabuleiro[linha][coluna] = jogador_humano
                if verificar_vencedor(tabuleiro, jogador_humano):
                    tabuleiro[linha][coluna] = jogador_computador  # Realiza a jogada para bloquear
                    print(f"O computador escolheu a posição ({linha}, {coluna})")
                    return linha, coluna

                tabuleiro[linha][coluna] = ' '  # Desfaz a jogada

    # Se não houver nenhuma jogada estratégica, faz uma jogada aleatória
    while True:
        linha = random.randint(0, 2)
        coluna = random.randint(0, 2)
        if tabuleiro[linha][coluna] == ' ':
            tabuleiro[linha][coluna] = jogador_computador  # Realiza a jogada aleatória
            print(f"O computador escolheu a posição ({linha}, {coluna})")
            return linha, coluna

# Função para perguntar ao jogador se deseja reiniciar o jogo
def reiniciar_jogo():
    while True:
        opcao = input("Deseja reiniciar o jogo? (1 - SIM, 2 - NÃO): ")
        if opcao == '1':
            return True
        elif opcao == '2':
            return False
        else:
            print("Opção inválida. Por favor, escolha 1 para SIM ou 2 para NÃO.")

# Função principal que controla o fluxo do jogo
def main():
#IMPORTANTE!!!
#Caminho usado para armazenar no meu computador foi esse, para armazenar no seu computador trocar (onde está localizado “jogadas.txt”) este caminho para que o código armazene certo. 
#Para encontrar o caminho e so clicar com botão direto do mouse em cima do "jogadas.txt" no seu computador e ir em copiar como caminhho e substituir no lugar "C:\Faculdade\jogo da velha\jogadas.txt"  
    caminho_arquivo = r"C:\Faculdade\jogo da velha\jogadas.txt"

    while True:
        tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]  # Inicializa o tabuleiro vazio
        print("Bem-vindo ao Jogo da Velha!")
        imprimir_tabuleiro(tabuleiro)

        jogador_humano = ''
        jogador_computador = ''
        
        # Escolha do símbolo pelo jogador
        while jogador_humano not in ['X', 'O']:
            jogador_humano = input("Escolha seu símbolo (X ou O): ").upper()
            if jogador_humano not in ['X', 'O']:
                print("Símbolo inválido. Escolha 'X' ou 'O'.")
        
        jogador_computador = 'O' if jogador_humano == 'X' else 'X'
        
        with open(caminho_arquivo, "a") as arquivo_jogadas:
            arquivo_jogadas.write("\nNovo jogo iniciado\n")
            arquivo_jogadas.write(f"Jogador humano: {jogador_humano}, Computador: {jogador_computador}\n")

            while True:
                print("Sua vez:")
                linha = input("Digite a linha (0, 1 ou 2): ")
                coluna = input("Digite a coluna (0, 1 ou 2): ")
                jogada_jogador(tabuleiro, linha, coluna, jogador_humano)  # Jogador faz sua jogada
                arquivo_jogadas.write(f"Jogador humano jogou em ({linha}, {coluna})\n")
                imprimir_tabuleiro(tabuleiro)  # Exibe o tabuleiro atualizado
                if verificar_vencedor(tabuleiro, jogador_humano):
                    print("Parabéns! Você venceu!")
                    arquivo_jogadas.write("Resultado: Jogador humano venceu\n")
                    break
                if tabuleiro_cheio(tabuleiro):
                    print("Empate!")
                    arquivo_jogadas.write("Resultado: Empate\n")
                    break

                print("Vez do computador:")
                linha, coluna = jogada_computador(tabuleiro, jogador_computador, jogador_humano)  # Computador faz sua jogada
                arquivo_jogadas.write(f"Computador jogou em ({linha}, {coluna})\n")
                imprimir_tabuleiro(tabuleiro)  # Exibe o tabuleiro atualizado
                if verificar_vencedor(tabuleiro, jogador_computador):
                    print("O computador venceu!")
                    arquivo_jogadas.write("Resultado: Computador venceu\n")
                    break
                if tabuleiro_cheio(tabuleiro):
                    print("Empate!")
                    arquivo_jogadas.write("Resultado: Empate\n")
                    break

        if not reiniciar_jogo():
            print("Obrigado por jogar!")
            break

if __name__ == "__main__":
    main()  # Executa a função principal
