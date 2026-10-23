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
| `--file-template` | Sti til den færdige PDF, der sendes til alle. Standard er miljøvariablen `FILE_TEMPLATE_PATH`. Kræves ved behandling af køen (processen stopper med en fejl, hvis filen ikke findes), men ikke ved `--queue` |

## Behandling
**Udfyld køen (`--queue`):**

1. Borgere hentes fra `[RPA_Dataudveksling_DWH].[dbo].[tilflyttere]`: tilflyttet inden for de seneste 35 dage og ikke intern flytning.
2. Borgeren springes over, hvis personen er død eller ikke har en aktuel adresse i Odense Kommune (Datafordeleren).
3. Borgeren springes over, hvis der allerede findes et færdigt item oprettet inden for de seneste 35 dage (`DAGE_MELLEM_BREVE`). Vinduet skal være lige så langt som SQL-vinduet i `process/mssql_client.py`.
4. Ellers lægges borgerens CPR i køen.

**Behandl køen:** For hvert item hentes adresse fra Datafordeleren, og PDF'en sendes med `sbsip.send_digital_post`. Kun adressen og PDF'en bruges, der flettes ikke noget ind i brevet.

Hvis et brev ikke kan sendes, markeres itemet som fejlet og rapporteres i arket `Fejl`, og processen fortsætter med næste borger. Fejlede items lægges ikke i køen igen af sig selv, men tæller ikke med i 35-dages kontrollen, så borgeren kommer med igen, næste gang køen udfyldes (så længe borgeren stadig er inden for SQL-vinduet).

## Rapportering
Rapporten `brevafsendelse-bmf-bosaetningsstrategi` (via `odk_tools.reporting`) har to ark:

| Ark | Indhold |
|---|---|
| `Fejl` | Én linje pr. fejlet brev eller borger, der ikke kan slås op i Datafordeler ved køudfyldning: CPR og årsag |
| `Antal sendte breve` | Antal breve sendt i kørslen |

**Tracking:** Hvert sendt brev registreres med `odk_tools.tracking.Tracker.track_task` under procesnavnet (`PROCES_NAVN` i `process/config.py`) via credentialen `Odense SQL Server`. En fejl i tracking logges, men får ikke et sendt brev til at tælle som fejlet.

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

Brevets PDF ligger ikke i repoet. I drift angives stien med `--file-template` som parameter på ATS-triggeren (filen ligger på et shared drive). Lokalt kan den lægges i `input/`, som er gitignored.

## Åbne punkter
- Målgruppen (kun unge) forudsættes afgrænset af DWH-tabellen `tilflyttere`. Koden filtrerer ikke på alder, så det bør bekræftes.
- Datafordeler 1.0.0 returnerer ikke personnumre, så tjekket af ændret CPR er væk. Se TODO i `main.py` om borgere med ændret CPR. En `ValueError` fra Datafordeleren ved køudfyldning (ugyldigt eller ukendt CPR) rapporteres i arket `Fejl`, og borgeren springes over.

## Persondata
Køen indeholder kun CPR. Fejlrapporten indeholder CPR og fejlårsagen. Rapporten over sendte breve indeholder kun et antal.
