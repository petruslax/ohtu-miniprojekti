import sqlite3
from datetime import datetime

from database import (
    init_db,
    add_reference,
    get_references,
    delete_reference,
    edit_reference,
)


def add_information():
    """Lisää uuden lähteen."""

    print("\nLisää uusi lähde")
    print("----------------")

    title = input("Otsikko: ").strip()
    author = input("Tekijä: ").strip()

    if not title or not author:
        print("Otsikko ja tekijä eivät saa olla tyhjiä.")
        return

    try:
        year = int(input("Julkaisuvuosi: "))
    except ValueError:
        print("Virheellinen vuosiluku!")
        return

    try:
        add_reference(title, author, year)
    except sqlite3.Error:
        print("Lähteen tallennus epäonnistui.")
        return

    print("\nLähde tallennettu!")


def show_information():
    """Näyttää tallennetut lähteet."""

    references = get_references()

    print("\nTallennetut lähteet")
    print("-------------------")

    if not references:
        print("Ei vielä tallennettuja lähteitä.")
        return

    for reference in references:
        print(
            f"ID: {reference[0]} | "
            f"Otsikko: {reference[1]} | "
            f"Tekijä: {reference[2]} | "
            f"Vuosi: {reference[3]}"
        )


def remove_information():
    """Poistaa valitun lähteen."""

    show_information()
    references = get_references()

    if not references:
        return

    try:
        reference_id = int(input("\nAnna poistettavan lähteen ID: "))
    except ValueError:
        print("Virheellinen ID!")
        return

    delete_reference(reference_id)
    print("Lähteen poistopyyntö suoritettu.")


def edit_information():
    """Muokkaa tallennetun lähteen tietoja."""

    show_information()
    references = get_references()

    if not references:
        return

    try:
        reference_id = int(input("\nAnna muokattavan lähteen ID: "))
    except ValueError:
        print("Virheellinen ID!")
        return

    if not any(reference[0] == reference_id for reference in references):
        print("Virheellinen ID!")
        return

    while True:
        print("\nMitä haluat muokata?")
        print("1. Muokkaa otsikkoa")
        print("2. Muokkaa tekijää")
        print("3. Muokkaa vuotta")
        print("4. Näytä lähteet")
        print("5. Lopeta muokkaus")

        choice = input("\nValitse toiminto: ")

        if choice == "1":
            title = input("\nAnna uusi otsikko: ").strip()
            if is_it_empty(title):
                print("Otsikko ei saa olla tyhjä.")
            else:
                edit_reference(reference_id, title=title)

        elif choice == "2":
            author = input("\nAnna uusi tekijä: ").strip()
            if is_it_empty(author):
                print("Tekijä ei saa olla tyhjä.")
            else:
                edit_reference(reference_id, author=author)

        elif choice == "3":
            year = input("\nAnna uusi vuosi: ").strip()
            if is_year(year):
                edit_reference(reference_id, year=int(year))
            else:
                print("Virheellinen vuosi.")

        elif choice == "4":
            show_information()

        elif choice == "5":
            print("Muokkaus lopetettu.")
            break

        else:
            print(f"Toimintoa {choice} ei ole olemassa.")


def is_year(year):
    """Tarkistaa, että vuosiluku on kelvollinen."""

    try:
        value = int(year.strip())
    except (AttributeError, ValueError):
        return False

    return 1000 <= value <= datetime.now().year


def is_it_empty(word):
    """Palauttaa True, jos merkkijono on tyhjä tai pelkkää välilyöntiä."""

    return not word.strip()


def export_information():
    """Vie tallennetut lähteet BibTeX-muotoiseen tiedostoon."""

    references = get_references()

    if not references:
        print("Ei lähteitä vietäväksi.")
        return

    bibtex_entries = []

    for reference_id, title, author, year in references:
        entry = (
            f"@misc{{lahde{reference_id},\n"
            f"  author = {{{author}}},\n"
            f"  title = {{{title}}},\n"
            f"  year = {{{year}}}\n"
            "}"
        )
        bibtex_entries.append(entry)

    try:
        with open("references.bib", "w", encoding="utf-8") as bibtex_file:
            bibtex_file.write("\n\n".join(bibtex_entries))
    except OSError:
        print("BibTeX-tiedoston luominen epäonnistui.")
        return

    print("Lähteet tallennettu tiedostoon references.bib.")


def start():
    """Käynnistää komentorivinäkymän."""

    init_db()

    while True:
        print("\n==========================")
        print(" UPEE JA MAHTI LÄHDEVIITTEIDEN HALLINTA")
        print("==========================")
        print("1. Lisää uusi lähde")
        print("2. Tutki tallennettuja lähteitä")
        print("3. Poista lähde")
        print("4. Muokkaa lähteitä")
        print("5. Luo BibTeX-tiedosto")
        print("6. Lopeta")

        choice = input("\nValitse toiminto: ")

        if choice == "1":
            add_information()
        elif choice == "2":
            show_information()
        elif choice == "3":
            remove_information()
        elif choice == "4":
            edit_information()
        elif choice == "5":
            export_information()
        elif choice == "6":
            print("Ohjelma suljetaan.")
            break
        else:
            print("Virheellinen valinta.")
