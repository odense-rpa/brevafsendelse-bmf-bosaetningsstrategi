# Brevafsendelse BMF Bosætningsstrategi

Sender et brev som Digital Post (SBSip) til tilflyttere til Odense Kommune, som BMF's bosætningsstrategi vil informere om kommunens tilbud. Borgerlisten hentes fra DWH. Processen opretter hverken sager eller journalnotater i SBSYS.

## Kørsel
```sh
uv sync
uv run python main.py --queue                              # udfyld køen
uv run python main.py --file-template <sti til brev.pdf>   # behandl køen
```

| Argument | Beskrivelse |
|---|---|
| `--queue` | Ryd items med status NEW, udfyld køen og afslut |
| `--file-template` | Sti til den færdige PDF, der sendes til alle. Standard er miljøvariablen `FILE_TEMPLATE_PATH`. Kræves ved behandling af køen, men ikke ved `--queue` |

## Behandling
**Udfyld køen (`--queue`):**

1. Borgere hentes fra `[RPA_Dataudveksling_DWH].[dbo].[tilflyttere]`: tilflyttet inden for de seneste 35 dage og ikke intern flytning.
2. Borgeren springes over, hvis personen er død eller ikke har en aktuel adresse i Odense Kommune (Datafordeleren).
3. Borgeren springes over, hvis der allerede findes et item (uanset status) oprettet inden for de seneste 35 dage (`DAGE_MELLEM_BREVE`). Vinduet skal være lige så langt som SQL-vinduet i `process/mssql_client.py`.
4. Ellers lægges borgerens CPR i køen.

**Behandl køen:** For hvert item hentes adresse fra Datafordeleren, og PDF'en sendes med `sbsip.send_digital_post`. Kun adressen og PDF'en bruges, der flettes ikke noget ind i brevet.

Hvis et brev ikke kan sendes, markeres itemet som fejlet og rapporteres i arket `Fejl`, og processen fortsætter med næste borger. Fejlede items lægges ikke i køen igen af sig selv, og de tæller med i 35-dages kontrollen.

## Rapportering
Rapporten `brevafsendelse-bmf-bosaetningsstrategi` (via `odk_tools.reporting`) har to ark:

| Ark | Indhold |
|---|---|
| `Fejl` | Én linje pr. fejlet brev: CPR og årsag |
| `Antal sendte breve` | Antal breve sendt i kørslen |

## Credentials
- `SBSip - produktion`
- `Odense SQL Server` (felterne `server` og `database`)
- `Datafordeler`

## Konfiguration
Faste indstillinger ligger i `process/config.py`. Miljøvariabler (se `.env.example`):

| Variabel | Beskrivelse |
|---|---|
| `ATS_URL`, `ATS_TOKEN`, `ATS_WORKQUEUE_OVERRIDE` | Forbindelse til Automation Server ved lokal kørsel |
| `FILE_TEMPLATE_PATH` | Standardsti til brevets PDF |

## Åbne punkter
- `BREV_OVERSKRIFT` og `BREV_BESKRIVELSE` i `process/config.py` er testtekster og skal erstattes, når BMF har oprettet brevet.
- Datafordeler 1.0.0 returnerer ikke personnumre, så tjekket af ændret CPR er væk. Se TODO i `main.py` om borgere med ændret CPR, og om en `ValueError` fra Datafordeleren skal fanges i stedet for at stoppe hele køen.

## Persondata
Køen indeholder kun CPR. Fejlrapporten indeholder CPR og fejlårsagen. Rapporten over sendte breve indeholder kun et antal.
