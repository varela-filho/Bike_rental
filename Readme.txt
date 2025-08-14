!!! ATENÇÃO: LEIA ESSE ARQUIVO ANTES DE OLHAR O PROJETO !!!

Esse é um projeto de aplicação de projetos de data science utilizando o django

O objetivo é criar algoritimos que realizem tarefas de aprendizado de máquina e exibir esses resultados em um site gerenciado através do django.

Atualmente o projeto se encontra em desenvolvimento, porém algumas etapas já foram concluídas como:

* Foi criado um algoritmo de previsão de aluguéis de bicicleta a partir de um banco de dados de dados climáticos de Washington DC.
* Esse algoritmo foi escolhido por apresentar um melhor desempenho conforme demonstrado no notebook `bike_rentals.ipynb`.
* Foi utilizado o Django a fim de criar uma interface web que pudesse interagir com um usuário
* Dessa forma, ao utilizar o terminal na pasta \previsao_aluguel_bike e realizar o comando "python manage.py runserver" é possível verificar que o django inicia o servidor em um endereço como http://127.0.0.1:8000/
* Com o servidor rodando, ao acessar a url http://127.0.0.1:8000/bike_rentals/ o usuário irá ver uma interface dá uma opção para o usuário escolher uma data entre os próximos 5 dias. Após selecionar a data e clicar em "Prever" será exibido um valor para a quantidade previstas de bicicletas a serem alugadas em Washiton DC, com margem de erro. 
* Os dados de previsão gerados são baseados no algoritmo de aprendizado de máquina desenvolvido e em dados novos reais obtidos a partir de API referente ao clima de Washinton DC.

O próximo passo do projeto é criar uma página de portfólio em que será possível saber mais sobre o dono dos projetos e onde será possível clicar em janelas que redirecionaram o usuário para os projetos criados.