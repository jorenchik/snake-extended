# Projekta apraksts 

## Projekta nosaukums

Snake multiplayer (snake-extended)

## Grupas dalībnieku saraksts

Jorens Štekeļs, apl.nr.: js21283

## Īss programmas apraksts (ko programma dara)

Programma ir klasiska čūskas spēle. Ir realizēts gan individuālas spēles, gan
spēle divatā caur datoru tīklu, kas tika realizēts P2P modeli. Komunikācija ir
realizēta ar "websockets" bibliotēku un spēles funkcionalitāte ir realizēta ar
"pygame" bibliotēkas palīdzību.

Čūskas spēles mērķis ir iegūt pēc iespējas lielāku čūsku, vācot ēdienus, kas
tiek izvietoti spēles laukā. Spēle beidzas, ja čūska kādas čūskas ķermenim.

## Instrukcijas, kā palaist Jūsu programmu

Iegūt pirmkoda repozitoriju, piemēram, klonējot to no github repozitorija.

```
$ git clone https://github.com/jorenchik/snake-extended 
$ cd ./snake-extended
```

Izveidot virtuālo Python vidi (nav obligāts).

```
$ python -m venv venv
```

Aktivizēt python virtuālo vidi.

Linux/Unix:
```
$ source ./venv/bin/activate
```

Windows:
```
$ source .\venv\Scripts\activate
```

Instalēt ``poetry'', lai iegūt nepieciešamās pakotnes.
```
$ python -m pip install poetry 
$ python -m poetry install 
```

Alternatīvi nepieciešamas pakotnes var iegūt no "requirements.txt".
```
$ pip install -r requirements.txt
```

Palaist programmu viena spēlētāja režīmā.
```
$ python snakext/app.py 
```

Lai palaistu programmu 2 spēlētāju režīmā ir jā norāda argumenti: sockets,
lokālā servera ports (neobligāts). Piemēram pieslēgsimies pie socketa
localhost:54323 sākot lokālo serveri portā 54322.
```
$ python snakext/app.py localhost:54323 --local-port 54322
```

Noklusējuma ports ir 54321. Tātad:
```
$ python snakext/app.py 192.168.8.3
```
Pievienotos pie 192.178.8.3:54321 un startēs serveri portā 54321.

## Ekrānuzņēmumi, kas parāda programmu darbībā

Viena spēlētāja režīms

![Spēle ir sākta](docs/img/singleplayer1.png)
![Spēle procesā](docs/img/singleplayer2.png)

Divu spēlētāju režīms. Sākumā notiek pievienošanās. Ja tā ir veiksmīga
tiek veikts rokasspiediens un sākta spēle līdzīgi kā viena spēlētāja
režīmā.

![Divu spēlētāju spēles sākšana](docs/img/multiplayer1.png)
![Divu spēlētāju spēles process](docs/img/multiplayer2.png)

## Saite uz projekta GitHub (Gitlab, u.tml.) repozitoriju

Projekta repozitorijs ir atrodams
[šeit](https://github.com/jorenchik/snake-extended).
