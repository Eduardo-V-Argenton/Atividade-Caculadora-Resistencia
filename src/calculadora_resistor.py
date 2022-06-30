from si_prefix import si_format

# pip install si-prefix
# Documento usado como base: https://www.sis.se/api/document/preview/8021442/ (IEC 60062:2016)

quant_faixas = 0
v = []


def main():
    op = True
    while op:   # O codigo se repitirá enquanto o usuário não escolher a opção de não repetir
        entrar_numero_faixas()
        criar_resistor()
        imprimir_info()
        op = repetir()


def entrar_numero_faixas():  # Entrada e Verificação da quantidade de faixas
    global quant_faixas
    global v
    ap = False   # ap == aprovado
    while not ap:
        num_faixas = input("Digite quantas faixas tem o resistor: ")

        if num_faixas.isdigit():    # Verificação da entrada
            quant_faixas = int(num_faixas)
            if 3 <= quant_faixas <= 6:
                v = [0] * quant_faixas  # Criação do vetor que guardará as faixa do resistor
                ap = True
                continue

        print("Entrada Inválida")


def criar_resistor():  # Entrada e Verificação das cores da faixa
    i = 0

    while i < quant_faixas:
        cor = input(f"Digite a cor da {i + 1}ª faixa: ").title()

        if validar_resistor(cor, i):    # A verificação da entrada
            i += 1
            continue

        print("Entrada Inválida")


def validar_resistor(cor, i):  # A cor inserida pelo usuario será verificada
    global v
    cod_cor = {"Preto": 0, "Marrom": 1, "Vermelho": 2, "Laranja": 3, "Amarelo": 4, "Verde": 5, "Azul": 6, "Violeta": 7,
               "Cinza": 8, "Branco": 9, "Ouro": 10, "Prata": 11, "Rosa": 12}    # Tabela de conversão

    #   Verificação se a entrada é uma cor dentre as validas
    if not (cor in cod_cor):
        return False
    else:   # Converte a cor para um número
        cor = cod_cor[cor]

    #   Verificação se a cor é valida na posição inserida
    if quant_faixas == 3 or quant_faixas == 4:
        if (i == 0 or i == 1) and not 0 <= cor <= 9:
            return False
        elif i == 2 and not (0 <= cor <= 12):
            return False
        elif i == 3 and not (0 < cor <= 11 and cor != 9):
            return False
    else:
        if (i == 0 or i == 1 or i == 2) and not 0 <= cor <= 9:
            return False
        elif i == 3 and not (0 <= cor <= 12):
            return False
        elif i == 4 and not (0 < cor <= 11 and cor != 9):
            return False
        elif i == 5 and not 0 < cor <= 8:
            return False
            
    v[i] = cor
    return True


def imprimir_info():  # Imprime o Resultado Final
    res = calcular_resistencia()    # Calcular o valor da resistência
    tol = calcular_tolerancia()     # Calcular a tolerância
    print(f"A resitência é de {si_format(res, precision=3)}\u03A9s\nCom {tol}% de tolerancia"
          f"({si_format((res + res * tol / 100), precision=3)}\u03A9s a "
          f"{si_format((res - res * tol / 100), precision=3)}\u03A9s)")
    if quant_faixas == 6:   # No resistor de 6 faixas a 6ª faixa representa o coeficiente de temperatura
        tcr = calcular_coef_temp()
        print(f"E {tcr} 10⁻⁶/K de coef. de temperatura")


def calcular_resistencia():
    # Nos resistores de 3 e 4 faixas as 2 primeiras indicam os primeiros algarismo e a 3ª o número de zeros
    if quant_faixas == 3 or quant_faixas == 4:
        return (v[0] + (0.1 * v[1])) * 10 * gerar_base_10(2)

    # Nos resistores de 5 e 6 faixas as 3 primeiras indicam os primeiros algarismos e a 4ª o número de zeros
    else:
        return (v[0] + (0.1 * v[1]) + (0.01 * v[2])) * 100 * gerar_base_10(3)


def calcular_tolerancia():  # Converterá a cor para tolerancia
    cor_tol = {1: 1, 2: 2, 3: 0.05, 4: 0.02, 5: 0.5, 6: 0.25, 7: 0.1, 8: 0.01, 10: 5, 11: 10}

    if quant_faixas == 3:   # Resistores de 3 faixas tem tolerância de 20%
        return 20
    # Nos resistores de 4 faixas a faixa inidica a tolerãncia é a 4ª já nos de 5 e 6 faixas a 5ª
    elif quant_faixas <= 4:
        return cor_tol[v[3]]
    else:
        return cor_tol[v[4]]


def calcular_coef_temp():   # Converterá a 6ª faixa em coeficente de temperatura
    cor_temp = {0: 250, 1: 100, 2: 50, 3: 15, 4: 25, 5: 20, 6: 10, 7: 5, 8: 1}  # Tabela de conversão
    return cor_temp[v[5]]


def gerar_base_10(i):   # Converterá o numero dado a cor da faixa que indica o numero de zero para potência de base 10
    if v[i] <= 9:
        return 10 ** v[i]

    else:
        return 10 ** (10 - v[i] - 1)


def repetir():  # Será dado ao usuário a opção de repetir
    op = " "
    ap = False
    while not ap:
        op = input("\nDeseja Repetir? [S/N]").upper()
        if op != "N" and op != "S":
            print("Entrada Inválida")
        else:
            ap = True

    if op == "S":
        return True
    else:
        return False


if __name__ == "__main__":
    main()
