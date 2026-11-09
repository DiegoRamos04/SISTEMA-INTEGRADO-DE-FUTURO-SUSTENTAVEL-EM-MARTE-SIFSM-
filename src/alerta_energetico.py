"""Regra compartilhada com o circuito SIFSM: S = (A e B) ou C.

Sem dependências externas. Os limites são definidos pelo operador, na mesma
unidade da leitura; não representam limites validados de engenharia.
"""
import csv
import math
from itertools import product
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def verificar_alerta(consumo_alto: bool, modulo_critico: bool, falha: bool) -> bool:
    if any(type(v) is not bool for v in (consumo_alto, modulo_critico, falha)):
        raise ValueError("As entradas A, B e C devem ser booleanas.")
    return (consumo_alto and modulo_critico) or falha


def avaliar_telemetria(consumo, limite, modulo_critico, falha):
    consumo, limite = float(consumo), float(limite)
    if not all(math.isfinite(v) and v >= 0 for v in (consumo, limite)):
        raise ValueError("Consumo e limite devem ser números finitos não negativos.")
    a = consumo >= limite
    alerta = verificar_alerta(a, modulo_critico, falha)
    return dict(A=int(a), B=int(modulo_critico), C=int(falha), alerta=int(alerta))


def comando_serial(estado):
    return "SET " + "".join(str(estado[k]) for k in ("A", "B", "C"))


def tabela_verdade():
    return [dict(A=a, B=b, C=c, alerta=int(verificar_alerta(bool(a), bool(b), bool(c))))
            for a, b, c in product((0, 1), repeat=3)]


def exportar_estados(estados, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["A", "B", "C", "alerta", "comando_serial"])
        writer.writeheader()
        for estado in estados:
            writer.writerow({**estado, "comando_serial": comando_serial(estado)})
    return destino


def avaliar_csv(origem, limite, modulo_critico, falha):
    """CSV existente não contém status/falhas: B e C são informados pelo operador.

    O limite usa a unidade de Consumo_Energetico. O projeto original diverge
    entre kW e kWh; não fazemos conversão nem inferimos potência pela energia.
    """
    estados = []
    with Path(origem).open(encoding="utf-8-sig", newline="") as arquivo:
        reader = csv.DictReader(arquivo)
        if "Consumo_Energetico" not in (reader.fieldnames or []):
            raise ValueError("CSV sem a coluna Consumo_Energetico.")
        for linha, registro in enumerate(reader, 2):
            try:
                estados.append(avaliar_telemetria(registro["Consumo_Energetico"], limite, modulo_critico, falha))
            except (TypeError, ValueError) as erro:
                raise ValueError(f"Linha {linha}: {erro}") from erro
    if not estados:
        raise ValueError("CSV sem medições.")
    return estados


def ler_bit(pergunta):
    while True:
        valor = input(pergunta + " (1=Sim, 0=Não): ").strip()
        if valor in ("0", "1"):
            return valor == "1"
        print("Digite somente 0 ou 1.")


def executar_alerta():
    print("\nSIFSM — Alerta energético: (A e B) ou C")
    print("1 - Leitura manual | 2 - CSV energético existente | 3 - Tabela verdade")
    try:
        modo = input("Modo: ").strip()
        if modo == "3":
            estados = tabela_verdade()
            nome = "tabela_verdade.csv"
        elif modo in ("1", "2"):
            print("Use a MESMA unidade para leitura e limite. A = leitura >= limite.")
            limite = float(input("Limite de consumo alto: ").replace(",", "."))
            b = ler_bit("Módulo em condição crítica (B)?")
            c = ler_bit("Falha detectada (C)?")
            if modo == "1":
                consumo = float(input("Consumo medido: ").replace(",", "."))
                estados = [avaliar_telemetria(consumo, limite, b, c)]
                nome = "leitura_manual.csv"
            else:
                estados = avaliar_csv(RAIZ / "dados_aurora_siger.csv", limite, b, c)
                nome = "alertas_consumo.csv"
        else:
            print("Modo inválido.")
            return
        for e in estados[:8]:
            print(f"A={e['A']} B={e['B']} C={e['C']} | Alerta={e['alerta']} | {comando_serial(e)}")
        destino = exportar_estados(estados, RAIZ / "data" / "circuito" / nome)
        print(f"{len(estados)} leituras; {sum(e['alerta'] for e in estados)} alertas.\nArquivo: {destino}")
        print("No Monitor Serial do circuito, envie um comando SET por vez; BTN retorna aos botões.")
    except (ValueError, OSError) as erro:
        print(f"Não foi possível avaliar: {erro}")


if __name__ == "__main__":
    executar_alerta()
