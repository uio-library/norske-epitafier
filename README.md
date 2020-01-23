# Norske epitafier

Dette repoet inneholder data for «Norske epitafier» som XML-filer,
samt script for å konvertere postene til Dublin Core og laste dem opp til Alma Digital.

## Dublin Core applikasjonsprofil

Definisjon av felter som brukes i xml-versjonen av katalogen, og hvilke felter disse skal korrespondere med i DC application profile 1 i UBOs katalog.

Feltene i Alma Digital konfigureres i ExLibris Alma under `Alma Configuration > Resources > Cataloging > Metadata Configuration > DC application profile 1`

Språkvalg for skjemaet:
engelske felt/egenskaper og norske etiketter/labels. [utviklingsønske: etiketter på flere språk]

Felter som er i bruk for denne samlingen (pr 17.01.2020):

Felt | Innsnevring av | Etikett | Beskrivelse
---|---|---|---
`dc:date`               || Dato            | TODO
`dc:description`        || Beskrivelse     | TODO
`dcterms:bibliographicCitation` || Referanser  | TODO
`dcterms:provenance`    || Proveniens        | TODO
`dcterms:rightsHolder`  ||    Opphaver         | TODO
`dc:contributor`    ||    Contributor
`dc:coverage`    ||   Coverage
`dc:creator`    ||    Creator
`dc:format`    ||    Format
`dc:identifier`    ||    Identifier
`dc:language`    ||    Language
`dc:publisher`    ||   Publisher
`dc:relation`    ||    Relation
`dc:rights`    ||    Rights
`dc:source`    ||   Source
`dc:subject`    ||    Subject
`dc:title`    ||   Title
`dc:type`    ||    Type
`:epitaphOn`   ||  `dc:subject` ? |    Epitafium over         | TODO
`:diocese`      || Stift  | Historisk stift|
`:location`    | `dcterms:spatial` ?   Nåværende plassering         | TODO
`:originalLocation`    ||   Opprinnelig plassering         | TODO
`:filelabel`    ||  File label         | TODO
`:kunstner`    ||  Kunstner     | TODO
`:inscriptions`    ||  Innskrift     | Feltet inneholder alle innskrifter, samt overskrifter. Er html-formatert med avsnitt pga manglende formateringsmuligheter i visning |
`:beskrivelse`    ||   Beskrivelse     | TODO
`:merknader`    || Merknader     | TODO

## Script

### Oppsett

Hent inn avhengigheter med pipenv:

	pipenv install

Lag en `.env`-fil for hemmeligheter:

	cp .env.dist .env

og legg nøkler for Alma og S3 her.

### Konvertere

For å konvertere poster fra lokalt XML-format til Dublin Core:

	pipenv -m scripts.convert

### Laste opp

For å laste opp til Alma:

	pipenv -m scripts.upload

### Synkronisere ID-er

Når postene har blitt importert i Alma bør man hente ned ID-ene som har blitt generert for postene:

	pipenv -m scripts.fetch_ids

Disse lagres i fila `alma_ids.json`.
