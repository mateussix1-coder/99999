from decimal import Decimal
from pathlib import Path
import unittest

import auditoria_engine as ae


ROOT_DIR = Path(__file__).resolve().parents[1]
SAMPLE_ATUA = ROOT_DIR / "sample_atua.pdf"
SAMPLE_GW = ROOT_DIR / "sample_gw.pdf"


class MoneyParsingTests(unittest.TestCase):
    def test_parse_money_accepts_mixed_decimal_formats(self):
        self.assertEqual(ae.parse_money_br("1.234,56"), Decimal("1234.56"))
        self.assertEqual(ae.parse_money_br("1234.56"), Decimal("1234.56"))
        self.assertEqual(ae.parse_money_br("0.00"), Decimal("0.00"))


class SampleParserTests(unittest.TestCase):
    def test_sample_atua_parser(self):
        registros = ae.extrair_atua_por_blocos(SAMPLE_ATUA)
        self.assertEqual(len(registros), 10)
        self.assertEqual(registros["1751"]["empresa"], Decimal("1000.00"))
        self.assertEqual(registros["1751"]["motorista"], Decimal("1000.35"))
        self.assertEqual(registros["1760"]["empresa"], Decimal("1090.00"))
        self.assertEqual(registros["1760"]["motorista"], Decimal("1090.35"))

    def test_sample_gw_parser(self):
        registros = ae.extrair_gw_por_blocos(SAMPLE_GW)
        self.assertEqual(len(registros), 10)
        self.assertEqual(registros["1751"]["empresa"], Decimal("1000.00"))
        self.assertEqual(registros["1751"]["motorista"], Decimal("1000.40"))
        self.assertEqual(registros["1760"]["empresa"], Decimal("1090.00"))
        self.assertEqual(registros["1760"]["motorista"], Decimal("1090.40"))

    def test_sample_audit(self):
        resultado = ae.auditar(SAMPLE_ATUA, SAMPLE_GW, Decimal("0.50"))
        self.assertEqual(resultado["resumo"]["total_analisado"], 10)
        self.assertTrue(resultado["linhas"])
        self.assertTrue(all(linha["Status"] == "OK por arredondamento" for linha in resultado["linhas"]))


if __name__ == "__main__":
    unittest.main()
