import sqlite3

from database import (
    init_db,
    add_reference,
    get_references,
    delete_reference
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


def export_information():

    references = get_references()
    
    if not references:
        return    

    bibtex_entries = []

    for reference in references:
        reference_id, title, author, year = reference

        entry = (
              f"@misc{{AVAINTÄHÄN{reference_id},\n"
              f"author = {{{author}}},\n"
              f"title = {{{title}}},\n"
              f"year = {{{year}}}\n"
              f"}}"  
        )

        bibtex_entries.append(entry)

    try:
        with open("references.bib", "w") as f:
            f.write("\n\n".join(bibtex_entries))
    except OSError:
        print("\nBibTeX-tiedoston luominen epäonnistui")
        return
    
    print("\nLähteet tallennettu tiedostoon references.bib")      
    



def start():
    """Käynnistetään komentorivi-näkymä."""

    init_db()

    while True:
        print("\n==========================")
        print(" UPEE JA MAHTI LÄHDEVIITTEIDEN HALLINTA")
        print("==========================")
        print("1. Lisää uusi lähde")
        print("2. Tutki tallennettuja lähteitä")
        print("3. Poista lähde")
        print("4. Vie tiedostoon")
        print("5. Lopeta")

        choice = input("\nValitse toiminto: ")

        if choice == "1":
            add_information()

        elif choice == "2":
            show_information()

        elif choice == "3":
            remove_information()

        elif choice == "4":
                    export_information()    

        elif choice == "5":
            print("Ohjelma suljetaan.")
            break

        else:
            print("Virheellinen valinta.")
