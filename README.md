# Data Logger Arduino using PostgreSQL Database

In this project we created a data logger using an Arduino board to store
temperature and humidity from soil and ar into a database on localhost.

## Instalando a biblioteca psycopg2 no python
No seu terminal, digite:
1. `sudo apt-get install psycopg2`

## Programando Arduino com o Atom

1. Instale o pacote `platomformio` no atom.
1. Instale o pacote python para comunicação:
 `pip install platformio`
1. Na pasta onde ficará o código rode: `platformio init --board=uno`
1. Na pasta **src** criada coloque seu código **.ino**.
1. Para usar os comandos use o atalho **Ctrl+Shift+P** no atom e digite: **platomformio**. Os comandos mais utilizados são o build (compilar) e o upload (compilar e carregar).
1. Para visualizar a porta serial utilize um terminal e o comando: `platformio device monitor --baud=9600`

## Protocolo de comunicação entre o Arduino e o Computador
 A comunicação foi feita através da porta serial com baudrate de 9600.
 Pacotes:

 Starter | Tipo | Informação | Finalizador
 ------- | ---- | ---------- | -----------
 '$' | 'U' | '29' | '\n'
 '$' | 'T' | '25.0' | '\n'

Sendo 'U' o indicador que será enviado um valor de Umidade (porcentagem).
E 'T' o indicador que será enviado um valor de Temperatura (graus celcius).

## Group components
- Pablo Nunes
- Paulo Camargos
- Thiago Pereira
- Vítor Menezes

Colaborations: Ítalo Fernandes - github.com/italogfernandes
