"""Faste indstillinger for processen."""

PROCES_NAVN = "Brevafsendelse BMF Bosætningsstrategi"

# Navnet rapporteringen grupperes under i odk_tools.reporting
RAPPORT_NAVN = "brevafsendelse-bmf-bosaetningsstrategi"
RAPPORT_ARK_FEJL = "Fejl"
RAPPORT_ARK_ANTAL = "Antal sendte breve"

# Credentials i ATS
CREDENTIAL_SBSIP = "SBSip - produktion"
CREDENTIAL_SQL = "Odense SQL Server"
CREDENTIAL_DATAFORDELER = "Datafordeler"

# En borger må højst have et brev inden for så mange dage (matcher vinduet i
# MSSQLClient.hent_borgere, som skal være lige så langt)
DAGE_MELLEM_BREVE = 35

BREV_OVERSKRIFT = "Velkommen til Odense"
# Selve beskeden i digital post. sbsip sætter teksten direkte ind i en HTML-body,
# så afsnit skal være <p>-tags (almindelige linjeskift forsvinder). sbsip sender
# beskeden som UTF-8 men erklærer HTML'en som iso-8859-1, så æøå ville blive vist
# forkert. Derfor skrives alle tegn uden for ASCII som HTML-entiteter (æ -> &#230;).
_BREV_BESKRIVELSE_TEKST = (
    "<p>Kære nye odenseaner. Velkommen til byen. Vi er virkelig glade for, at du har "
    "valgt at være en del af Odense. Hvad enten du er flyttet hertil for at studere, "
    "arbejde, være tættere på dem, du holder af, vende tilbage, eller starte et helt "
    "nyt kapitel i dit liv, håber vi, at du hurtigt kommer til at føle dig hjemme.</p>"
    "<p>At flytte til en ny by kan være både spændende og overvældende. Derfor vil vi "
    "gerne give dig en varm velkomst og dele nogle af de ting, som mange unge "
    "odenseanere holder særligt meget af ved livet i Odense.</p>"
)
# "xmlcharrefreplace" erstatter hvert tegn uden for ASCII med en HTML-entitet, fx
# "æ" -> "&#230;". Uden det vises "Kære" som "KÃ¦re" i digital post, fordi sbsip
# sender UTF-8-bytes, men HTML'en fortæller modtageren, at de er iso-8859-1.
BREV_BESKRIVELSE = _BREV_BESKRIVELSE_TEKST.encode("ascii", "xmlcharrefreplace").decode(
    "ascii"
)
