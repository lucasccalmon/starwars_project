# Projeto de Análise de Dados de Star Wars: Canon vs. Legends

## Bem-vindo! Que a Força dos Dados esteja com você.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/1200px-Star_Wars_Logo.svg.png)

Esse é o repositório onde estão todos os códigos criados para a análise da biodiversidade e mortalidade na galáxia.

Os dados referentes a mais de **43.000 personagens** (incluindo **espécie**, **afiliação**, **data de nascimento** e **morte**) foram extraídos processando o *dump* XML oficial da [Wookieepedia](https://starwars.fandom.com/) pelo script [`leitura_personagens_xml.py`], utilizando as bibliotecas `mwxml` e `mwparserfromhell` para varrer a estrutura bruta da Wiki. Após a extração, foi gerado o arquivo CSV [`personagens_droides_star_wars.csv`] para guardar os dados estruturados.

Com o auxílio de **Expressões Regulares (Regex)** e **Pandas**, foi realizado o tratamento e limpeza dos dados, convertendo datas complexas (como "c. 19 BBY") em valores numéricos e categorizando automaticamente a continuidade de cada personagem entre **Canon** e **Legends**.

A análise completa e a geração dos gráficos podem ser vistas no notebook [`analise_starwars.ipynb`]. O foco principal foi entender se o universo Canon da Disney é realmente "vazio" comparado ao antigo Universo Expandido.

### Principais Insights:

- **Biodiversidade Galáctica:**
    - Ao contrário do senso comum, o Canon não está vazio. Foram identificadas **1.084 espécies inteligentes** distintas no Canon, contra **1.460** no Legends. Isso indica que o novo universo já recuperou cerca de **74% da diversidade biológica** do antigo em apenas uma década.
    - Em ambos os universos, a proporção de não-humanos é alta. No Canon, **56,6%** dos personagens não são humanos, uma taxa ligeiramente maior que no Legends (**52,4%**).

- **Quem habita a galáxia?**
    - Foi observado que os **Astromech Droids** são a "espécie" não-humana mais frequente no Canon, superando raças clássicas. Já no Legends, a liderança fica com os **Twi'leks**, mostrando a forte influência de obras antigas (HQs e jogos) na demografia galáctica.
    - Outras espécies dominantes incluem Rodians, Zabraks e Wookiees, que mantêm relevância em ambas as continuidades.

- **Histórico de Conflitos (Timeline de Baixas):**
    - Através da normalização das datas de morte (BBY/ABY), foi possível plotar o "pulso" da guerra na galáxia.
    - O gráfico de densidade revelou com precisão o impacto da **Ordem 66** (no ano -19 BBY), que representa o maior pico de mortalidade de Jedi em um curto espaço de tempo.
    - Também foram identificados picos claros nos eventos da **Batalha de Yavin (0 BBY)** e na **Batalha de Exegol (35 ABY)**, validando a consistência dos dados extraídos com a narrativa dos filmes.

### Tecnologias Utilizadas:
* **Python**
* **Mwxml / Mwparserfromhell** (Parsing de XML massivo)
* **Pandas** (Manipulação e estruturação de dados)
* **Regex** (Limpeza de datas e textos não estruturados)
* **Matplotlib / Seaborn** (Visualização de dados)