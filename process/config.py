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
# MSSQLClient.hent_borgere; kun første kørsel overstyres med DAGE_TILBAGE)
DAGE_MELLEM_BREVE = 35

# Selve beskeden i digital post, bygget til at ligne brevets PDF. sbsip sætter
# teksten direkte ind i en HTML-body. Mange klienter (og digital post) ignorerer
# <style>-blokke og klasser, så al formatering ligger som inline style, defineret
# én gang herunder. Billeder, logoer og ikoner fra PDF'en kan ikke bruges (ingen
# eksterne ressourcer), og tosporslayoutet er erstattet af ét spor.
_FARVE = "#AA3250"
_BAGGRUND = "#D2EBFA"
_FONT = "font-family:Arial,Helvetica,sans-serif;"
_H1 = f"{_FONT}color:{_FARVE};font-size:40px;line-height:1.05;font-weight:bold;font-style:italic;margin:0 0 20px 0;"
_H2 = f"{_FONT}color:{_FARVE};font-size:20px;font-weight:bold;font-style:italic;margin:24px 0 4px 0;"
_H3 = f"{_FONT}color:{_FARVE};font-size:17px;font-weight:bold;font-style:italic;margin:20px 0 2px 0;"
_P = f"{_FONT}color:#000000;font-size:16px;line-height:1.4;margin:0 0 14px 0;"
_NOTE = f"{_FONT}color:#000000;font-size:10px;font-style:italic;margin:24px 0 0 0;"
_FODNOTE = (
    "Med fremsendelse af dette velkomstbrev behandler Odense Kommune dine "
    "personoplysninger. Du kan læse mere om Odense Kommunes behandling af dine "
    "personoplysninger samt dine rettigheder i forbindelse hermed på "
    "www.odense.dk/privatlivspolitik"
)

BREV_OVERSKRIFT = "Velkommen til Odense"
_BREV_BESKRIVELSE_TEKST = f"""
<div style="background:{_BAGGRUND};padding:24px;">

<h1 style="{_H1}">KÆRE NYE ODENSEANER</h1>
<h2 style="{_H2}">VELKOMMEN TIL ODENSE &#9829;</h2>
<p style="{_P}"><b><i>Please note that you will find an English version below.</i></b></p>
<p style="{_P}">Vi er virkelig glade for, at du har valgt at være en del af vores by. Hvad enten du er flyttet hertil for at studere, arbejde, være tættere på dem, du holder af, vende tilbage, eller starte et helt nyt kapitel i dit liv, håber vi, at du hurtigt kommer til at føle dig hjemme.</p>
<p style="{_P}">At flytte til en ny by kan være både spændende og overvældende. Der er nye gader, nye mennesker og nye drømme, der skal have plads til at vokse. Derfor vil vi gerne give dig en varm velkomst og dele nogle af de ting, som mange unge odenseanere holder særligt meget af ved livet i Odense.</p>
<h2 style="{_H2}">Vi håber, du finder mennesker, steder og oplevelser, som gør Odense til din by.</h2>
<p style="{_P}">Følg <b><i>@odensekommune</i></b> hvis du vil følge med i, hvad der sker i byen, og have tips til oplevelser, fællesskaber og livet som ung i Odense.</p>
<p style="{_P}">Og hvis du leder efter fællesskaber, sociale aktiviteter, guides fra andre unge, studieliv, oplevelser eller bare inspiration til dit liv i byen, så finder du det hele på <b><i>www.odense.dk/odenseforever</i></b></p>
<p style="{_P}">Vi glæder os til, at du bliver en del af Odense.</p>
<p style="{_P}"><b><i>Kærlig hilsen<br>Odense Kommune</i></b></p>

<h1 style="{_H1}margin-top:36px;">10 TING, VI HÅBER, DU OPDAGER VED ODENSE</h1>
<h3 style="{_H3}">1. Du behøver ikke kende nogen for at høre til</h3>
<p style="{_P}">Mange unge flytter til Odense uden at kende andre på forhånd. Heldigvis er byen fuld af fællesskaber, hvor det er nemt at møde nye mennesker.</p>
<h3 style="{_H3}">2. Du er omgivet af andre unge</h3>
<p style="{_P}">Odense er hjemsted for tusindvis af studerende og unge mennesker. Her er altid andre, der ligesom dig er i gang med et nyt kapitel.</p>
<h3 style="{_H3}">3. Det er nemt at komme rundt</h3>
<p style="{_P}">Byen er skabt til cykler, gåture og korte afstande. Du kan hurtigt komme fra studie eller arbejde til caféer, kultur, natur og venner.</p>
<h3 style="{_H3}">4. Naturen ligger lige om hjørnet</h3>
<p style="{_P}">En tur langs Odense Å, gennem Munke Mose eller ved havnen kan være det perfekte afbræk fra en travl hverdag.</p>
<h3 style="{_H3}">5. Der er masser at opleve</h3>
<p style="{_P}">Koncerter, festivaler, sport, kultur, markeder og events fylder kalenderen året rundt. Der sker ofte mere, end man lige tror.</p>
<h3 style="{_H3}">6. Du kan have et godt ungeliv uden et kæmpe budget</h3>
<p style="{_P}">Mange af byens bedste oplevelser er gratis eller billige, og der findes masser af steder at mødes, hænge ud og opleve byen.</p>
<h3 style="{_H3}">7. Studielivet foregår også uden for studiet og arbejdet</h3>
<p style="{_P}">Noget af det bedste ved studietiden er ofte alt det, der sker ved siden af. Foreninger, frivillighed, netværk og nye interesser er med til at skabe minder for livet.</p>
<h3 style="{_H3}">8. Der er gode muligheder for studiejob og karriere</h3>
<p style="{_P}">I Odense finder du både små spændende virksomheder og store internationale arbejdspladser. Mange starter deres karriere allerede under studiet.</p>
<h3 style="{_H3}">9. Din stemme betyder noget</h3>
<p style="{_P}">Vi ønsker, at Odense er en by, som udvikles sammen med dem, der bor her. Derfor er unges idéer, holdninger og engagement vigtige for byens fremtid.</p>
<h3 style="{_H3}">10. Du er med til at gøre Odense til Odense</h3>
<p style="{_P}">Byen bliver til gennem de mennesker, der bor her. Med dine interesser, idéer, venskaber og drømme er du med til at forme det Odense, vi deler.</p>
<p style="{_NOTE}">{_FODNOTE}</p>

<hr style="border:0;border-top:2px solid {_FARVE};margin:36px 0;">

<h1 style="{_H1}">DEAR NEWCOMER</h1>
<h2 style="{_H2}">IT IS OUR PLEASURE TO WELCOME YOU TO ODENSE</h2>
<p style="{_P}">You are now part of a city that is rich in history, full of life, and open to the world. Whether you are here to work, study, or start a new chapter in your life, we hope you will quickly feel at home.</p>
<p style="{_P}">Moving to a new country can be exciting, and sometimes overwhelming. That is why we have gathered useful information and local tips to help you get settled and make the most of life in Odense.</p>
<p style="{_P}">If you would like to stay up to date with what&#8217;s happening in the city and get tips on events, communities, and life in Odense, follow Odense Kommune and International House Odense on Instagram:<br><b><i>@odensekommune @internationalhouseodense</i></b></p>
<p style="{_P}">And if you&#8217;re looking for communities, social activities, local guides, student life inspiration, and tips to help you make the most of life in Odense, you&#8217;ll find it all on <b><i>internationalhouseodense.dk/studying</i></b></p>
<p style="{_P}">We can&#8217;t wait for you to become part of Odense.</p>
<p style="{_P}"><b><i>Warm regards,<br>City of Odense</i></b></p>

<h1 style="{_H1}margin-top:36px;">10 TIPS TO HELP YOU FEEL AT HOME IN ODENSE</h1>
<h3 style="{_H3}">1. International House Odense</h3>
<p style="{_P}">A welcoming space offering guidance, events, and opportunities to connect with locals and internationals. Sign up for the newsletter and follow on social media for updates, events, and tips. You can also find practical information and guides on the website iho.dk. Feel free to visit at Borgernes Hus whenever help is needed.</p>
<h3 style="{_H3}">2. Borgerservice (Citizen Service)</h3>
<p style="{_P}">Handle practical matters such as your driver&#8217;s licence, address registration, parking permits, MitID, health insurance, and more at Borgernes Hus. Book appointments online.</p>
<h3 style="{_H3}">3. Job Search Guide</h3>
<p style="{_P}">Practical advice for internationals on finding a student job or starting a career in Denmark, including tips on Danish work culture, CVs, interviews, and entrepreneurship. Find the guide on www.iho.dk</p>
<h3 style="{_H3}">4. Language Classes</h3>
<p style="{_P}">Learning Danish can help you settle in and feel more at home. After receiving your CPR number, you&#8217;ll be offered a Danish language course. You can also practise informally through conversation groups and language cafés.</p>
<h3 style="{_H3}">5. VisitOdense.com</h3>
<p style="{_P}">Live like a local. Discover events, local favourites, cultural experiences, and hidden gems around the city. VisitOdense is not just for tourists.</p>
<h3 style="{_H3}">6. Odenserundt.dk</h3>
<p style="{_P}">Your digital guide to the city, with real-time updates on roadwork, parking, public facilities, green spaces, and local events.</p>
<h3 style="{_H3}">7. Get Active in Odense</h3>
<p style="{_P}">Discover clubs, activities, and associations for all interests. Many associations welcome internationals. Check out SportinDenmark.dk for activities tailored to internationals and get an overview of clubs and activities on AktivOdense.dk.</p>
<h3 style="{_H3}">8. SocialKompas.dk</h3>
<p style="{_P}">Find support, volunteering opportunities, and more than 350 local services, from family and wellbeing resources to community activities and social initiatives.</p>
<h3 style="{_H3}">9. Studenterhus &amp; Ungdomshuset</h3>
<p style="{_P}">Welcoming spaces for students and young people in Odense. Drop by to meet new people, join events, study in a cozy setting, or become part of a community and grow your network.</p>
<h3 style="{_H3}">10. Library &amp; Kulturmaskinen</h3>
<p style="{_P}">Explore Odense&#8217;s creative and cultural life. From libraries filled with books, games, and creative spaces to workshops, concerts, and events at Kulturmaskinen, there is always something new to discover.</p>
<p style="{_NOTE}">{_FODNOTE}</p>

</div>
"""
# "xmlcharrefreplace" erstatter hvert tegn uden for ASCII med en HTML-entitet, fx
# "æ" -> "&#230;". Uden det vises "Kære" som "KÃ¦re" i digital post, fordi sbsip
# sender UTF-8-bytes, men HTML'en fortæller modtageren, at de er iso-8859-1.
# Linjeskift fjernes, så beskeden ikke indeholder blanke tegn mellem tags.
BREV_BESKRIVELSE = (
    "".join(line.strip() for line in _BREV_BESKRIVELSE_TEKST.splitlines())
    .encode("ascii", "xmlcharrefreplace")
    .decode("ascii")
)
