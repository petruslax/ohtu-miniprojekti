def add_information():
    """Kysy käyttäjältä mitä lisätään."""
    information = input("Anna lisättävä tieto: ")
    print(f"Annettu tieto: {information}")


def start():
    """Käynnistetään komentorivi-näkymä."""
    print("tervetuloa testiohjelmaan")
    add_information()