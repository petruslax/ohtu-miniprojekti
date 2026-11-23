import os
import sys
import tempfile
import unittest
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

    def test_virheellinen_poisto_id_ei_poista_lahdetta(self):
        database.add_reference("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)

        with patch("builtins.input", return_value="ei numero"):
            with redirect_stdout(StringIO()):
                user_interface.remove_information()

        lahteet = database.get_references()

        self.assertEqual(len(lahteet), 1)
        self.assertEqual(
            lahteet[0][1:],
            ("Ohjelmistotuotanto", "Matti Meikäläinen", 2024)
        )