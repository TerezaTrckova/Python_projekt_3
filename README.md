# Python projekt 3 - Engeto akademie
## Popis projektu
Tento projekt obsahuje scraper výsledků parlamentních voleb z roku 2017 v ČR. Program získává výsledky voleb z webu [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven
Nejprve je potřeba instalovat knihovny použité ve skriptu. Potřebné knihovny jsou uloženy v textovém souboru ```requirements.txt```. Pro instalaci knihoven je vhodné použít nové virtuální prostředí a takto spustiti kód:
```
pip --version
pip install -r requirements.txt

```
## Spuštění skriptu
Ke spuštění souboru ```election_scraper.py``` jsou potřeba 2 argumenty. První argument obsahuje odkaz na územní celek, který chcete scrapovat. Druhý argument obsahuje jméno výstupního souboru.
```

python election_scraper.py "<uzemi-URL><vysledny-soubor>

```
## Ukázka programu
Výsledky pro okres Kutná Hora
1. argument: ```https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2105```
2. argument: ```vysledky_okresu_Kutna_Hora.csv```
#### Spuštění programu
```

python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2105" vysledky_okresu_Kutna_Hora.csv

```
#### Průběh stahování
```

Stahuji data z vybraného URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2105
To znamená celkem 88 obcí ke zpracování
Ukládám do souboru: vysledky_okresu_Kutna_Hora.csv
Ukončuji election-scraper

```
#### Ukázka výsledku
```

code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,Unie H.A.V.E.L.,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
531367,Adamov,102,74,72,5,0,0,9,0,8,14,0,2,0,0,0,7,0,0,0,21,0,0,2,0,0,0,0,4,0
531111,Bernardov,157,89,89,5,0,0,1,0,7,14,0,1,1,0,0,11,1,0,0,30,0,2,1,0,1,0,1,11,2

```
