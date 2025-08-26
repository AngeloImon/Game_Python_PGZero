# Game_Python_PGZero

# 🎮 Plataformeiro

**Plataformeiro** é um jogo de plataforma dinâmico desenvolvido com [PgZero](https://pygame-zero.readthedocs.io/en/stable/), onde o jogador escala plataformas geradas automaticamente, enfrenta inimigos e coleta moedas para acumular pontos. O jogo não tem fim — a aventura continua até o herói cair ou ser derrotado.

---

## 🧠 Mecânicas do Jogo

- Plataformas são geradas dinamicamente, com ou sem inimigos e moedas.
- O jogador ganha:
  - **10 pontos** por cada plataforma escalada
  - **100 pontos** por cada moeda coletada
- Ao morrer (por queda ou inimigo), a pontuação é salva em um arquivo `.txt`.
- O jogo termina apenas quando o jogador morre — não há fase final.

---

## 🕹️ Menu Principal

O jogo possui um menu interativo com botões clicáveis:

- **Start Game** — inicia a aventura
- **Toggle Music/Sound** — ativa ou desativa os efeitos sonoros
- **Exit** — fecha o jogo

---

## 👾 Inimigos e Herói

- Diversos inimigos habitam o cenário e representam perigo real.
- Cada inimigo possui comportamento próprio e se movimenta dentro de seu território.
- O herói e os inimigos usam **animações de sprite** tanto em movimento quanto em repouso (ex: pernas, cauda, respiração, olhar).

---

## 🧱 Requisitos Técnicos

Este projeto segue restrições específicas:

- **Bibliotecas permitidas**:
  - `pgzero`
  - `math`
  - `random`
  - `pygame.Rect` (exceção permitida)
- **Bibliotecas proibidas**:
  - Qualquer outra além das listadas
  - **Pygame completa NÃO deve ser usada**

---

## 🧑‍💻 Boas Práticas

- Código escrito de forma **única e independente**
- Nomes de variáveis, funções e classes seguem o padrão **PEP8**
- Lógica clara e sem bugs conhecidos

---

## 📁 Estrutura do Projeto
    Plataformeiro/
    ├── game.py
    ├── hero.py
    ├── enemy.py
    ├── platforms.py
    ├── scenario.py
    ├── menu.py
    ├── constants.py
    ├── settings.py
    ├── scores.txt
    ├── images/
    ├── sounds/
    ├── music/
    └── .venv/

---

## 📝 Créditos

Desenvolvido por [Angelo Imon](https://github.com/AngeloImon).
Agradecimentos especiais à [Kenney.nl](https://kenney.nl/assets/new-platformer-pack) pela disponibilização dos recursos visuais.

---

## 🚀 Comece a jogar

Clone o repositório e execute com PgZero.
Necessário instalar o PGZero - Recomendado um ambiente virtual.
