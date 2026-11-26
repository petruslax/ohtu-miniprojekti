import os
import sys
import tempfile
import unittest
import sqlite3
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "references"))
import database
import user_interface


class TestLahteidenHallinta(unittest.TestCase):
    def setUp(self):
        self.valiaikainen_kansio = tempfile.TemporaryDirectory()
        self.alkuperainen_kansio = os.getcwd()
        os.chdir(self.valiaikainen_kansio.name)
        database.init_db()

    def tearDown(self):
        os.chdir(self.alkuperainen_kansio)
        self.valiaikainen_kansio.cleanup()

    def test_tallennettu_lahde_loytyy_tietokannasta(self):
        database.add_reference("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)

        lahteet = database.get_references()

        self.assertEqual(len(lahteet), 1)
        self.assertEqual(
            lahteet[0][1:],
            ("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)
        )

    def test_poistettu_lahde_ei_loydu_tietokannasta(self):
        database.add_reference("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)
        lahde_id = database.get_references()[0][0]

        database.delete_reference(lahde_id)

        self.assertEqual(database.get_references(), [])

    def test_nayttaa_lahteen_tiedot(self):
        database.add_reference("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)
        tuloste = StringIO()

        with redirect_stdout(tuloste):
            user_interface.show_information()

        self.assertIn("Otsikko: Ohjelmistotuotanto", tuloste.getvalue())
        self.assertIn("Tekijä: Matti Meikäläinen", tuloste.getvalue())
        self.assertIn("Vuosi: 2024", tuloste.getvalue())

    def test_lahteen_lisaaminen_tallentaa_tiedot(self):
        with patch(
            "builtins.input",
            side_effect=["Ohjelmistotuotanto", "Matti Meikäläinen", "2024"]
        ):
            with redirect_stdout(StringIO()):
                user_interface.add_information()

        lahteet = database.get_references()

        self.assertEqual(len(lahteet), 1)
        self.assertEqual(
            lahteet[0][1:],
            ("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)
        )

    def test_valitun_lahteen_poistaminen_poistaa_lahteen(self):
        database.add_reference("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)
        lahde_id = database.get_references()[0][0]

        with patch("builtins.input", return_value=str(lahde_id)):
            with redirect_stdout(StringIO()):
                user_interface.remove_information()

        self.assertEqual(database.get_references(), [])

    def test_virheellinen_vuosiluku_ei_tallenna_lahdetta(self):
        with patch(
            "builtins.input",
            side_effect=["Ohjelmistotuotanto", "Matti Meikäläinen", "ei vuosiluku"]
        ):
            with redirect_stdout(StringIO()):
                user_interface.add_information()

        self.assertEqual(database.get_references(), [])

    def test_tyhjasta_lahdelistasta_naytetaan_viesti(self):
        tuloste = StringIO()

        with redirect_stdout(tuloste):
            user_interface.show_information()

        self.assertIn(
            "Ei vielä tallennettuja lähteitä.",
            tuloste.getvalue()
        )

    def test_tyhja_otsikko_ei_tallenna_lahdetta(self):
        with patch(
            "builtins.input",
            side_effect=["", "Matti Meikäläinen", "2024"]
        ):
            with redirect_stdout(StringIO()):
                user_interface.add_information()

        self.assertEqual(database.get_references(), [])

    def test_tyhja_tekija_ei_tallenna_lahdetta(self):
        with patch(
            "builtins.input",
            side_effect=["Ohjelmistotuotanto", "", "2024"]
        ):
            with redirect_stdout(StringIO()):
                user_interface.add_information()

        self.assertEqual(database.get_references(), [])

    def test_tietokantavirheesta_naytetaan_virheviesti(self):
        tuloste = StringIO()

        with patch(
            "builtins.input",
            side_effect=["Ohjelmistotuotanto", "Matti Meikäläinen", "2024"]
        ):
            with patch(
                "user_interface.add_reference",
                side_effect=sqlite3.OperationalError("tietokanta ei käytettävissä")
            ):
                with redirect_stdout(tuloste):
                    user_interface.add_information()

        self.assertIn(
            "Lähteen tallennus epäonnistui.",
            tuloste.getvalue()
        )
        self.assertNotIn("Lähde tallennettu!", tuloste.getvalue())

    def test_bibtex_vienti_tallentaa_lahteen_tiedostoon(self):
        database.add_reference("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)

        with redirect_stdout(StringIO()):
            user_interface.export_information()

        bibtex = Path("references.bib").read_text(encoding="utf-8")

        self.assertIn("@misc{lahde1,", bibtex)
        self.assertIn("author = {Matti Meikäläinen}", bibtex)
        self.assertIn("title = {Ohjelmistotuotanto}", bibtex)
        self.assertIn("year = {2024}", bibtex)

    
