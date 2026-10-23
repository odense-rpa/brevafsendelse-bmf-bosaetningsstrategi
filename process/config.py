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
BREV_BESKRIVELSE = "Velkomstbrev til nye unge odenseanere"
