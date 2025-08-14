# A Dona Aranha: Missão Filó 

Bem-vindo ao *Resgate das saias*, um jogo de aventura e ação no qual você assume o papel da dona Aranha e enfrenta uma chuva forte para recuperar as 6 saias que estão faltando da sua amiga, a Barata!

---

## 1. Título e membros da equipe
*A Dona Aranha: Missão Filó*  
*Membros:*  
- Miguel Melo de Albuquerque <mma4>
- Luan Gustavo Nogueira de Souza <lgns>
- Beatriz Farias Silva <bfs8>
- Ana Beatriz Regis de Souza <abrs>
- Giovana Castro de Melo e Silva <gcms3>
- Iury Mikael Sobral dos Santos <imss2>
 

---

## 2. Arquitetura do Projeto

O jogo foi desenvolvido com Pygame e organizado em diferentes arquivos para melhor modularização:

- *run_game.py*: inicializa o Pygame e executa o jogo.
- *main.py*: contém a classe que representa a janela do jogo e coordena os estados do jogo.
- *classes.py*: reúne as classes dos obstáculos, dos objetos coletáveis e da parede (cada um com sua lógica própria).
- *player.py*: define a classe do jogador e a lógica de interação com os coletáveis, saltos e obstáculos.
- *constants.py*: guarda valores fixos (como tamanho da janela, número associado a cada estado do jogo, etc.), imagens e fontes utilizadas.
- *resources* (pasta): guarda imagens e fontes utilizadas.


### Jogabilidade:

- Ação principal: pular de uma parede à outra usando as teclas Espaço, setas, A (esquerda) e D (direita).
- Com o tempo, a velocidade de queda das gotas de chuva aumenta, dificultando o desafio.
- O dano causado por uma gota é proporcional ao seu tamanho.
- O objetivo do jogo é coletar as 6 saias que estão faltando; ele termina quando esse objetivo é atingido ou quando o jogador perde toda a vida em consequência de ser atingido pelas gotas de chuva.

---

## 3. Capturas de Tela

> <img align="center" src="https://raw.githubusercontent.com/lgns-cin/projeto-ip/dev/resources/screenshots/screenshot1.png" width="960">
> <img align="center" src="https://raw.githubusercontent.com/lgns-cin/projeto-ip/dev/resources/screenshots/screenshot2.png" width="960">
> <img align="center" src="https://raw.githubusercontent.com/lgns-cin/projeto-ip/dev/resources/screenshots/screenshot3.png" width="960">
> <img align="center" src="https://raw.githubusercontent.com/lgns-cin/projeto-ip/dev/resources/screenshots/screenshot4.png" width="960">
> <img align="center" src="https://raw.githubusercontent.com/lgns-cin/projeto-ip/dev/resources/screenshots/screenshot5.png" width="960">
> <img align="center" src="https://raw.githubusercontent.com/lgns-cin/projeto-ip/dev/resources/screenshots/screenshot6.png" width="960">


---

## 4. Ferramentas, bibliotecas e frameworks utilizados

- *Python 3*
- *Pygame*: biblioteca principal usada para renderização, eventos e lógica do jogo.
- Ferramentas de desenho utilizadas: *Piskel*, *Pixel Art (geral)* e *Canva*.

### Justificativa:
O Pygame é leve, fácil de aprender e ideal para protótipos rápidos de jogos 2D.

---

## 5. Divisão de trabalho

- Todos: idealização coletiva da proposta do jogo.
- Luan, Miguel e Iury: responsabilidade pelo desenvolvimento do código.
- Ana Beatriz, Giovana e Beatriz: encarregadas da parte gráfica, do relatório e dos slides.

---

## 6. Conceitos da disciplina utilizados

- *Programação Orientada a Objetos*: o jogo é estruturado com classes, usando herança; por exemplo, a classe do jogador herda da classe Sprite do Pygame.
- *Tratamento de eventos*: uso intensivo de eventos do Pygame.
- *Estrutura condicional e Dicionários*: usados em diversas partes do código.
- *Controle de fluxo*: "while rodando" é o loop principal do jogo.
- *Modularização*: separação do código em múltiplos arquivos.

---

## 7. Desafios, erros e lições aprendidas

### Erro maior:
Animação do salto: a aranha deve saltar em trajetória parabólica e mudar de direção ao se aproximar da parede oposta.

### Maior desafio:
- Dar início ao projeto: transformar a documentação do Pygame em código.
- Design gráfico dos elementos do jogo (como a dona Aranha e os cenários).

### Lições aprendidas:
- Refatorar o código cedo evita retrabalho.
- Organização no GitHub ajuda no progresso coletivo.
- Dividir tarefas e manter comunicação clara no grupo é essencial.

---

## 8. Como jogar

### Requisitos:
- Python 3.x instalado
- Pygame instalado (pip install pygame)

### Instruções:

```
bash
git clone https://github.com/lgns-cin/projeto-ip.git
cd projeto-ip
python run_game.py 
```


Use as teclas Espaço, setas ou A (esquerda) e D (direita) para pular de uma parede à outra.
