# Paramètres de l'application RADAR

## Acquisition
* **tempo**: stock et transfert l'ensemble de la trame;
* **pos n**: stock le point n par trame.

## Configurations
### Configurations globales
* **input 0/1**: sélectionne si la trame entière est transférée au DAC (valeur
  0) ou seulement un point de la trame, de position donnée par la commande pos
  (ci-dessus), qui est transféré (valeur 0).
* **period nbpoint**: Configure la durée d'une trame (exprimée en nombre de
  point avec 8ns/point);
* **poff n**: durée entre la coupure de la réception et l'activation de
  l'émission, puis entre la coupure de la transmission et la réactivation de la
  réception (voir Remarques plus bas).
* **pon n**: durée de l'émission (en nombre de cycles d'horloges) (voir
  Remarques plus bas);

### bloc check
* **bypass_check 1/0**: Défini si le bloc de détection de trames corrompues est
  utilisé ou pas;
* **start_offset n**: offset (en nombre de point) du début de la zone utilisée pour
  le calcul;
* **limit**: valeur au dela de laquelle la trame est considérée comme corrompu.

### bloc average
* **bypass_mean 1/0**: Défini si le bloc d'average est utilisé ou non
* **iter n**: nombre d'accumulation réalisé par le bloc d'average. Doit être une
puissante de 2

## Remarques

Les options **pon** et **poff** sont utilisées pour piloter le switch. Celui ci contient
deux signaux pour activer indépendemment **RF1** et **RF2** et pour les router sur **RFC**
(cf. datasheet). 

Pour garantir l'isolation la réception est physiquement coupée au niveau du
switch avant d'activer la transmission~:
* le signal allant aux mélangeur est déconnectée de RFC (coupure de la réception);
* au bout de poff cycles d'horloges le signal venant du générateur est connecté
  à RFC (transmission);
* au bout de pon cycles d'horloges la voie du générateur est déconnectée;
* au bout de poff cycles d'horloges la réception est à nouveau activée.

La durée totale est donc de (2 x poff) + pon cycles d'horloges.


## Remarques 2

Le fichier de lancement /opt/radar_red/bin/radar_red_us.sh contient un exemple de
séquence de configuration en fin de fichier :

```
# periode d'interrogation
./radar_red_us period 512
# limite de seuil de rejet de la trame
./radar_red_us limit 55000
# offset de demarrage du calcul
./radar_red_us start_offset 350
# nombre de moyenne
./radar_red_us iter 16
# bloc average active
./radar_red_us bypass_mean 0
# bloc verification trames active
./radar_red_us bypass_check 0
```
