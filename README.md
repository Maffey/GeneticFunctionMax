# GeneticFunctionMax
The app finds max value in the given range for the given function using genetic methodology.

## Lecture notes [in Polish]
f(x) = x + 1 -> do naszego zadania 
f(x) = x + 1
x należy do <0, 31>
Pk = 0.8 - wspolczynnik krzyzowania
Pm = 0.2 - wspolczynnik mutacji

(Do dokumentacji 6 chromosomow, program najlepiej jakby dzialal dla N chromosomow)

chromosomy  fenotyp     przystosowanie (x+1)
Ch1 = 01001 9           10          10/151      6.6 %
Ch2 = 11010 26          27          27/151      17.8 %
Ch3 = 11001 25          26          26/151      17.7 %
Ch4 = 11010 26          27          ...         ...
Ch5 = 11110 30          31
Ch6 = 11101 29          30
                        = 151
Z danych procent tworzymy koło ruletki (pie chart) z wartosciami wpisanym przyrostowo na okolo okregu

losujemy liczbe od zera do stu, wybieramy w ktory chromosom trafimy (ruletka)
losujemy 6 razy, na nowo przypisujemy do chromosomów wartości trafione.

Etap krzyzowania
laczymy w pary chromosomy z Prawdopodobienstwem < Pk
 losujemy dla pary Pk, L z przedzialu <1, 4>
 L - miejsce do zamiany, np. dla L 3 zamieniamy po 3 bicie bity miedzy soboa
 

 Przyklad dla L = 3:
 010 | 01 --> 01010
 110 | 10 --> 11010
 
 Etap mutacji
 Mutujemy kazdy chromosom, z prawdopodobienstwem < Pm
 Pm, L - losujemy; L z przedzialu <1, 5>
 na miejscu bitu L, zmieniamy bit (z 1 na 0 lub odwrotnie)
 
 na dokumentacji robimy jedna iteracje, az do uzyskania nowych chormosomow
 
 dobry pakiet chromosomow to taki, gdzie funkcja przystosowania daje duza wartosc
 to, czy przerwac algorytm, okresla jak wzrasta wartosc przystosowania
