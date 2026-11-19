# Citizen Assist AI - Módulo de Energia
# Público: moradores de classe média preocupados com a conta de luz.

import os


# PREMISSAS

TARIFA = 0.7894       # R$ por kWh
FATOR_CO2 = 0.074     # kg de CO2 por kWh
HORAS_SOL = 4.5      # horas de sol pleno por dia
PERDAS = 0.80        # o sistema solar rende 80% do ideal (estimado)
CUSTO_KWP = 4500     # R$ por kWp instalado (orçamentos)
TAXA_MINIMA = 50     # kWh cobrados mesmo com solar (conta de luz)
POTENCIA_LED = 9     # W de uma LED que substitui uma lâmpada de 60 W
PRECO_LED = 4      # R$ por lâmpada LED (Ourolux Bivolt 9W)
ANOS = 10            # período de comparação

# Aparelhos de exemplo: (nome, potência em W, horas de uso por dia) - ESTIMADOS
EXEMPLO = [
    ("Geladeira", 150, 24),
    ("Chuveiro", 5500, 1),
    ("TV", 100, 5),
    ("Notebook", 60, 6),
    ("Maquina de lavar", 500, 1),
    ("Lampadas", 300, 5),
]

LIMITACOES = ("São estimativas, não garantias. A tarifa muda, o telhado precisa ser "
              "adequado, e não foram considerados manutenção.")

REGRAS = """Você é o assistente de energia do Citizen Assist AI, para moradores de classe média de São Paulo.
Regras:
1. Use linguagem simples e frases curtas.
2. Use SOMENTE os números dos DADOS abaixo. Nunca invente valores.
3. Diga que os valores são estimativas e nunca prometa economia garantida.
4. Se a pergunta não for sobre energia ou conta de luz, recuse educadamente.
5. Responda em até 180 palavras."""

# Funções
def ler_numero(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite apenas números (ex.: 2,5).")


def kwh_mes(potencia_w, horas_dia):
    return potencia_w * horas_dia * 30 / 1000


def calcular_consumo():
    if input("Usar a lista de exemplo? (s/n): ").lower() == "s":
        aparelhos = EXEMPLO
    else:
        aparelhos = []
        while True:
            nome = input("Nome do aparelho (ENTER para terminar): ")
            if nome == "":
                break
            w = ler_numero("  Potência em watts (está na etiqueta): ")
            h = ler_numero("  Horas de uso por dia: ")
            aparelhos.append((nome, w, h))

    total = 0
    print("\nAparelho            kWh/mês   Custo/mês")
    for nome, w, h in aparelhos:
        kwh = kwh_mes(w, h)
        total = total + kwh
        print(f"{nome:18} {kwh:8.1f}   R$ {kwh * TARIFA:7.2f}")
    print(f"{'TOTAL':18} {total:8.1f}   R$ {total * TARIFA:7.2f}")
    print(f"(tarifa estimada: R$ {TARIFA}/kWh)")
    return total


def mostrar(nome, investimento, kwh_economizados):
    economia_mes = kwh_economizados * TARIFA
    payback = investimento / (economia_mes * 12)
    saldo = economia_mes * 12 * ANOS - investimento
    co2 = kwh_economizados * 12 * ANOS * FATOR_CO2

    print(f"\n{nome}")
    print(f"  Investimento: R$ {investimento:.2f}")
    print(f"  Economia por mês: R$ {economia_mes:.2f}")
    print(f"  Retorno: {payback:.1f} anos")
    print(f"  Saldo em {ANOS} anos: R$ {saldo:.2f}")
    print(f"  CO2 evitado: {co2:.0f} kg")

    return (f"{nome}: investimento R$ {investimento:.2f}, economia R$ {economia_mes:.2f}/mês, "
            f"payback {payback:.1f} anos, saldo em {ANOS} anos R$ {saldo:.2f}, "
            f"CO2 evitado {co2:.0f} kg.")


def comparar(consumo):
    if consumo == 0:
        consumo = ler_numero("Digite seu consumo mensal em kWh: ")

    print("\n--- Alternativa A: trocar lâmpadas antigas por LED ---")
    n = ler_numero("Quantas lâmpadas vai trocar? ")
    w_antiga = ler_numero("Potência de cada lâmpada antiga em W: ")
    horas = ler_numero("Horas de uso por dia: ")

    print(f"\n=== COMPARAÇÃO PARA {ANOS} ANOS (valores estimados) ===")
    resumo = ""

    if w_antiga > POTENCIA_LED and n > 0 and horas > 0:
        economia_led = n * (w_antiga - POTENCIA_LED) * horas * 30 / 1000
        resumo += mostrar("A) LED (eficiência)", n * PRECO_LED, economia_led) + "\n"
    else:
        print("\nA) LED: sem economia com esses dados.")

    if consumo > TAXA_MINIMA:
        kwh_solar = consumo - TAXA_MINIMA
        kwp = kwh_solar / (HORAS_SOL * 30 * PERDAS)
        print(f"\nSistema solar estimado: {kwp:.2f} kWp")
        resumo += mostrar("B) Solar (renovável)", kwp * CUSTO_KWP, kwh_solar) + "\n"
    else:
        print("\nB) Solar: consumo muito baixo, não compensa.")

    print("\nLIMITAÇÕES:", LIMITACOES)
    return resumo


def perguntar_ia(pergunta, consumo, resultados):

    dados = (f"Premissas (estimadas): tarifa R$ {TARIFA}/kWh; fator CO2 {FATOR_CO2} kg/kWh; "
             f"horas de sol {HORAS_SOL}/dia; custo solar R$ {CUSTO_KWP}/kWp.\n"
             f"Consumo do usuário: {consumo:.1f} kWh/mês.\n"
             f"Resultados da comparação:\n{resultados or 'ainda não calculados'}\n"
             f"Limitações: {LIMITACOES}\n"
             "Fontes: ANEEL, CRESESB, MCTI, Procel/Inmetro.")
    try:
        import anthropic
        cliente = anthropic.Anthropic()
        resposta = cliente.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=600,
            system=REGRAS + "\n\nDADOS:\n" + dados,
            messages=[{"role": "user", "content": pergunta}],
        )
        partes_texto = []
        for bloco in resposta.content:
            if getattr(bloco, "type", None) == "text" and hasattr(bloco, "text"):
                partes_texto.append(bloco.text)

        texto = "".join(partes_texto).strip()
        if not texto:
            texto = "Não foi possível gerar uma resposta em texto desta vez."
        print("\n" + texto)
    except Exception as erro:
        print("Não consegui usar a IA agora:", erro)

# Programa principal
def main():
    consumo = 0
    resultados = ""
    print("Olá! Sou o assistente de energia do Citizen Assist AI.")

    while True:
        print("\n1) Calcular meu consumo")
        print("2) Comparar alternativas (LED x solar)")
        print("3) Perguntar para a IA")
        print("0) Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            consumo = calcular_consumo()
        elif opcao == "2":
            resultados = comparar(consumo)
        elif opcao == "3":
            pergunta = input("Sua pergunta (ou ENTER para a IA explicar seus resultados): ")
            if pergunta == "":
                pergunta = "Explique meus resultados e diga qual alternativa parece compensar."
            perguntar_ia(pergunta, consumo, resultados)
        elif opcao == "0":
            print("Até logo! Lembre-se: são estimativas.")
            break
        else:
            print("Opção inválida.")


main()
