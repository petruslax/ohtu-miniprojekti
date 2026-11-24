# ohtu-miniprojekti 

Ohjelmistotuotannon miniprojekti, syksy 2026.

Ryhmä 7: Petrus, Leo, Vili, Tia-Sofia, Luka

## Tavoite

Projektin tavoitteena on kehittää lähdeviitteiden hallintasovellus jolla käyttäjä voi tallentaa, hallita ja hakea lähdeviitteitä sekä viedä niitä BibTeX-muotoon.

Ominaisuudet tarkentuvat asiakkaan kanssa.

## Projektinhallinta

- Product backlog: [linkki](https://docs.google.com/spreadsheets/d/1pdlh-rOde1VTG8ahHbtjvErIwi0Nk5cS1Zb83f1axf8/edit?gid=0#gid=0)
- Sprint backlog: [linkki](https://docs.google.com/spreadsheets/d/1pdlh-rOde1VTG8ahHbtjvErIwi0Nk5cS1Zb83f1axf8/edit?gid=1222218005#gid=1222218005)
- CI (GitHub Actions): [linkki](https://github.com/petruslax/ohtu-miniprojekti/actions)

## Definition of Done

-  Vaatimus analysoitu
-  Toteutus suunniteltu
-  Vaatimus ohjelmoitu
-  Testattu
-  Integroitu ohjelmistoon

  
## Asennus ja käyttö

Asenna Python.

Kloonaa repositorio ja käynnistä ohjelma sen juuresta.

Käynnistä ohjelma ajamalla src/references/main.py

Valitse toiminto syöttämällä sen numero ja painamalla Enter.

1. Lisää uusi lähde antamalla tiedot vaiheittain.
2. Näytä tallennetut lähteet.
3. Poista lähde antamalla sen ID.
4. Lopeta ohjelma.

Viitteet tallentuvat projektin juuressa olevaan `references.db`-tiedostoon. Ohjelma luo tiedoston ensimmäisellä käynnistyskerralla.

Export BibTeX-muotoon ei toimi vielä.

## Lisenssi

Täydennetään...
