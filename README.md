# Igra Nim

Skupinski projekt pri predmetu umetna inteligenca: Primerjava različnih metod spodbujevalnega učenja na tej igri.

### Pravila igre

* poljubno število kupov kovancev s poljubnim številom kovancev v vsakem kupu (random? ali pa lahko določi igralec na začetku?)
* kdor vzame zadnji kovanec izgubi

### Ideje

* Q-learning
* SARSA algoritem
* izboljšan min-max algoritem (z Alpha Beta Pruning)

### Vrstni red dela

1. Class Nim - zelo kul zgled je [tukej](https://cs50.harvard.edu/ai/2020/projects/4/nim/) (glej zip datoteko pod Getting started)
2. Vsaka svoj algoritem
3. Primerjava

### Uporabni linki

* [https://cs50.harvard.edu/ai/2020/projects/4/nim/](https://cs50.harvard.edu/ai/2020/projects/4/nim/) navodila za domačo nalogo kjer so morali nardit Nim z Q-learningom (zraven so tudi ogrodja funkcij)
  * dve rešitvi te naloge: [prva](https://github.com/Fatiepie/Nim.ai), [druga](https://github.com/diesel707/Knights/tree/nim)
* [http://www.diva-portal.org/smash/get/diva2:814832/FULLTEXT01.pdf](http://www.diva-portal.org/smash/get/diva2:814832/FULLTEXT01.pdf) primerjava Q-learning in SARSA ampak samo psevdokoda
 * [https://www.cs.rhodes.edu/~kirlinp/courses/ai/f14/projects/proj4/](https://www.cs.rhodes.edu/~kirlinp/courses/ai/f14/projects/proj4/) še ena navodila za dn
* [https://medium.com/100-days-of-algorithms/day-90-simple-nim-ai-864b2fdf9e8a](https://medium.com/100-days-of-algorithms/day-90-simple-nim-ai-864b2fdf9e8a) analiza različnih opponentov? Idk če uporabno
* [https://www.upgrad.com/blog/min-max-algorithm-in-ai/#Breaking_down_the_min_max_algorithm_in_AI](https://www.upgrad.com/blog/min-max-algorithm-in-ai/#Breaking_down_the_min_max_algorithm_in_AI) minmax algoritem
* [https://medium.com/zero-equals-false/n-step-td-method-157d3875b9cb](https://medium.com/zero-equals-false/n-step-td-method-157d3875b9cb) metoda TD? Združuje SARSA in Monte Carlo? Tega si še nisem tok pogledala
* [https://pages.cs.wisc.edu/~jphanna/teaching/2021fall_cs540/documents/lec25-rl-summary.pdf](https://pages.cs.wisc.edu/~jphanna/teaching/2021fall_cs540/documents/lec25-rl-summary.pdf) mogoče pride prav za minmax
* Geeks for geeks: [Q-learning](https://www.geeksforgeeks.org/q-learning-in-python/) in [SARSA](https://www.geeksforgeeks.org/sarsa-reinforcement-learning/)
