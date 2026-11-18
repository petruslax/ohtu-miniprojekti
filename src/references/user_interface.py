def add_information():
    """Kysy käyttäjältä mitä lisätään."""
    information = input("Anna lisättävä tieto: ")
    print("\nLisää uusi tieto")
    print("----------------")

    title = input("Otsikko: ")
    description = input("testi: ")

    print("\nAnnetut tiedot:")
    print(f"Otsikko: {title}")
    print(f"testi: {description}")


def start():
    """Käynnistetään komentorivi-näkymä."""
    print("tervetuloa testiohjelmaan")
    add_information()