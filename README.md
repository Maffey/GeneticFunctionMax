# Genetic Function Max
The app finds max value in the given range for the given function using genetic methodology.

## Documentation [in Polish]
#### Szukanie ekstremum funkcji
##### Założenia zadania
n = 6
Pk = 0.8
Pm = 0.2
Zakładam, że a = 1, jako że zadanie staje się trywialne i nie wykorzystuje algorytmu genetycznego.
f(x) = x + 7

Dane w chromosomach zapisujemy w postaci binarnej, by uprościć stosowanie krzyżowania i mutacji, zaś naszą funkcją przystosowania jest suma wszystkich f(x), gdzie x to nasze wylosowane parametry chromosomów.

[Losowanie liczb zostało wykonane w Pythonie.]
##### Wykonanie iteracji
Losujemy sześć chromosomów:
Chromosom 1. : 10 --- 0b1010
Chromosom 2. : 5 --- 0b101
Chromosom 3. : 19 --- 0b10011
Chromosom 4. : 25 --- 0b11001
Chromosom 5. : 14 --- 0b1110
Chromosom 6. : 16 --- 0b10000

Obliczamy przystosowanie dla funkcji x + 7:

Chromosom 1. : 17
Chromosom 2. : 12
Chromosom 3. : 26
Chromosom 4. : 32
Chromosom 5. : 21
Chromosom 6. : 23

Suma wartości:
s = 131

Każdemu chromosomowi przypisujemy zakres liczb potrzebny do kolejnego kroku. Dla każdego chromosomu przedział ten to <k; k+c>*, gdzie k to suma wartości wszystkich poprzednich chromosomów a c to wartość aktualnego chromosomu. Do k zostaje dodane 1 po każdym chromosomie. Powoduje to przesunięcie sumy wartości o 5.

Chromosom 1. : <0; 17>
Chromosom 2. : <18; 30>
Chromosom 3. : <31; 57>
Chromosom 4. : <58; 90>
Chromosom 5. : <91; 112>
Chromosom 6. : <113; 136>

Teraz dokonujemy losowania liczby z przedziału 0 do 136 sześciokrotnie i dokonujemy stworzenia kolejnego pokolenia chromosomów. Zależnie od wylosowanych liczb, zostaną wyznaczone nowe chromosomy.

Chromosom 1. : 0b11001 [4]
Chromosom 2. : 0b11001 [4]

Chromosom 3. : 0b00101 [2]
Chromosom 4. : 0b01010 [1]

Chromosom 5. : 0b11001 [4]
Chromosom 6. : 0b01110 [5]

Dokonujemy krzyżowań, L losowane z przedziału <1, 4>, k to nasza wylosowana liczba.
Para I:
k = 0,954 > 0,8
brak krzyżowania

Para II:
k = 0,374 < 0,8 
L = 3
Chromosom 3. →  0b00110
Chromosom 4. → 0b01001

Para III:
k = 0,793 < 0,8
L = 1
Chromosom 5. → 0b01110 
Chromosom 6. → 0b11001

Dokonujemy mutacji, L losowane z przedziału <1, 5>, k to nasza wylosowana liczba.

Chromosom 1.
k = 0,351 > 0,2
brak mutacji

Chromosom 2.
k = 0,998 > 0,2
brak mutacji

Chromosom 3.
k = 0,373 > 0,2
brak mutacji

Chromosom 4.
k = 0,307 > 0,2
brak mutacji

Chromosom 5.
k= 0,027 > 0,2
L = 2
Chromosom 5. →  0b00110 

Chromosom 6.
k = 0,273 > 0,2
brak mutacji

Kończymy naszą iterację, zwracamy chromosomy:


Chromosom 1. : 0b11001
Chromosom 2. : 0b11001
Chromosom 3. : 0b00110
Chromosom 4. : 0b01001
Chromosom 5. : 0b00110 
Chromosom 6. : 0b01110

Największą wartość ma Chromosom 1 (2), która wynosi 25 (f(x) = 32), a więc to x = 25 jest kandydatem na maksimum funkcji po tej iteracji.
