import sqlite3
from datetime import datetime

from database import (
    init_db,
    add_reference,
    get_references,
    delete_reference,
    edit_reference
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
    """Käyttäjä voi muokata tallennettuja lähteitä"""

    show_information()

    references = get_references()

    if not references:
            return

    try:
        reference_id = int(input("\nAnna muokattavan lähteen ID: "))
    except ValueError:
        print("Virheellinen ID!")
        return

    while True:
        print("\nMitä haluat muokata?")
        print("1. muokkaa otsikko")
        print("2. muokkaa tekijä")
        print("3. muokkaa vuosi")
        print("4. näytä lähteet")
        print("5. lopeta muokkaus")

        edit = input("\nValitse toiminto: ")

        if edit == "1":
            newTitle = input("\nAnna uusi otsikko: ")
            if is_it_empty(newTitle) == False:
                edit_reference(reference_id, title=newTitle)
            else:
                print("\notsikko ei saa olla tyhjä")
            
        elif edit == "2":
            newAuthor = input("\nAnna uusi tekijä: ")
            if is_it_empty(newAuthor) == False:
                edit_reference(reference_id, author=newAuthor)
            else: 
                print("\ntekijä ei saa olla tyhjä")
            
        elif edit == "3":
            newYear = input("\nAnna uusi vuosi: ".strip())
            if is_year(newYear) == True:
                edit_reference(reference_id, year=newYear)
            else: 
                print("Virheellinen vuosi")     
        elif edit == "4":
            show_information()

        elif edit == "5":
            print ("Muokkaus lopetettu")
            break
            
        else:
            print("Toimintoa " + edit + " ei ole olemassa.")
            
def is_year(year):
    """Tarkistaa onko syöte vuosi"""
    clearYear = year.strip()
    if 1000 <= int(clearYear) <= datetime.now().year:
        return True
    else:
        return False

def is_it_empty(word):
    return not word.strip()
    
        

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
        print("4. Muokkaa lähteitä")
        print("5. Lopeta")

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
            print("Ohjelma suljetaan.")
            break

        else:
            print("Virheellinen valinta.")
