import csv
import tempfile
import unittest
from pathlib import Path
from src.alerta_energetico import avaliar_csv, avaliar_telemetria, exportar_estados, tabela_verdade, verificar_alerta


class TestAlerta(unittest.TestCase):
    def test_oito_combinacoes(self):
        self.assertEqual([e['alerta'] for e in tabela_verdade()], [0, 1, 0, 1, 0, 1, 1, 1])

    def test_limite_e_falha(self):
        self.assertEqual(avaliar_telemetria(150, 150, True, False)['alerta'], 1)
        self.assertEqual(avaliar_telemetria(149, 150, True, False)['alerta'], 0)
        self.assertEqual(avaliar_telemetria(0, 150, False, True)['alerta'], 1)

    def test_invalidos(self):
        for valor in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError): avaliar_telemetria(valor, 150, False, False)
            with self.assertRaises(ValueError): avaliar_telemetria(100, valor, False, False)
        with self.assertRaises(ValueError): verificar_alerta('0', False, False)

    def test_csv_e_comandos(self):
        with tempfile.TemporaryDirectory() as pasta:
            origem = Path(pasta) / 'entrada.csv'
            origem.write_text('Consumo_Energetico\n149\n150\n', encoding='utf-8')
            estados = avaliar_csv(origem, 150, True, False)
            self.assertEqual([e['alerta'] for e in estados], [0, 1])
            destino = exportar_estados(estados, Path(pasta) / 'saida.csv')
            with destino.open() as f: registros = list(csv.DictReader(f))
            self.assertEqual([e['comando_serial'] for e in registros], ['SET 010', 'SET 110'])
            origem.write_text('Consumo_Energetico\ninvalido\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Linha 2'): avaliar_csv(origem, 150, True, False)


if __name__ == '__main__':
    unittest.main()
