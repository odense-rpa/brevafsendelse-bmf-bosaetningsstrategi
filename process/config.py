"""Faste indstillinger for processen."""

PROCES_NAVN = "Brevafsendelse BMF Bosætningsstrategi"

# Navnet rapporteringen grupperes under i odk_tools.reporting
RAPPORT_NAVN = "brevafsendelse-bmf-bosaetningsstrategi"

# Credentials i ATS
CREDENTIAL_SBSIP = "SBSip - produktion"
CREDENTIAL_SQL = "Odense SQL Server"
CREDENTIAL_DATAFORDELER = "Datafordeler"

# En borger må højst have et brev inden for så mange dage (matcher vinduet i
# MSSQLClient.hent_borgere, som skal være lige så langt)
DAGE_MELLEM_BREVE = 35

# TODO: Erstattes af de rigtige tekster, når BMF har oprettet brevet
BREV_OVERSKRIFT = "Annes testbrev"
BREV_BESKRIVELSE = "bmf bosætningsstragtegi testbrev"
