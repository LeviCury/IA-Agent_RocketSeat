# Desafio Prompt Engineering

Resoluções das 4 questões do desafio de Prompt Engineering, com identificação da técnica utilizada em cada uma.

---

## Questão 1 — Ray Tracing: cálculo da cor de um pixel

### Técnica utilizada: **Chain-of-Thought (Cadeia de Pensamento)**

A questão pede a explicação de um processo técnico com múltiplas etapas encadeadas. A técnica Chain-of-Thought é ideal porque solicita que a IA raciocine passo a passo, revelando cada fase do algoritmo de forma lógica e sequencial.

### Prompt

```
Explique, passo a passo, como o algoritmo de Ray Tracing calcula a cor final
de um pixel em uma imagem renderizada. Detalhe cada etapa do processo, desde
o lançamento do raio a partir da câmera até a determinação da cor final,
incluindo: geração do raio, teste de interseção com objetos, cálculo de
iluminação direta, reflexões, refrações e composição final da cor.
```

### Resposta

O algoritmo de Ray Tracing calcula a cor de um pixel seguindo estas etapas:

**1. Geração do raio (Ray Casting)**
Para cada pixel da imagem, um raio é lançado a partir da posição da câmera virtual, passando pelo plano de projeção (a "tela"). A direção do raio é calculada com base nas coordenadas do pixel, no campo de visão (FOV) e na resolução da imagem.

**2. Teste de interseção com objetos**
O raio percorre a cena e o algoritmo testa a interseção com cada objeto (esferas, triângulos, planos etc.) usando equações geométricas. Para uma esfera, por exemplo, resolve-se a equação quadrática resultante da substituição da equação paramétrica do raio na equação da esfera. O ponto de interseção mais próximo (menor valor positivo de *t*) é selecionado.

**3. Cálculo do vetor normal**
No ponto de interseção encontrado, calcula-se o vetor normal à superfície. Para uma esfera, é simplesmente a direção do ponto de interseção ao centro da esfera, normalizada. Esse vetor é essencial para todos os cálculos de iluminação.

**4. Iluminação direta (Modelo de Phong ou similar)**
A cor no ponto é calculada combinando três componentes:

- **Ambiente**: luz constante que simula iluminação indireta global → `I_a = k_a × cor_objeto`
- **Difusa (Lambert)**: depende do ângulo entre a normal e a direção da luz → `I_d = k_d × max(0, N · L) × cor_luz`
- **Especular**: simula brilho/reflexo pontual → `I_s = k_s × max(0, R · V)^n × cor_luz`

Antes de calcular a contribuição de cada fonte de luz, um **shadow ray** (raio de sombra) é lançado do ponto de interseção em direção à luz. Se o raio atingir outro objeto antes de chegar à luz, aquele ponto está em sombra para aquela fonte.

**5. Reflexão**
Se a superfície é reflexiva, um novo raio é gerado na direção de reflexão: `R = D - 2(D · N)N`, onde D é a direção do raio incidente. Esse raio recursivo repete todo o processo (etapas 2-6) no objeto que atingir, e a cor retornada é ponderada pelo coeficiente de reflexão do material.

**6. Refração (transparência)**
Se a superfície é transparente, um raio de refração é calculado usando a **Lei de Snell**: `n₁ × sin(θ₁) = n₂ × sin(θ₂)`. O equilíbrio entre reflexão e refração é determinado pelas **equações de Fresnel**. O raio refratado segue para dentro do objeto e também gera chamadas recursivas.

**7. Composição final da cor**
A cor final do pixel é a soma ponderada de todas as contribuições:

```
cor_final = cor_ambiente + cor_difusa + cor_especular
          + k_reflexão × cor_reflexo
          + k_refração × cor_refração
```

A recursão é limitada por um número máximo de "bounces" (rebatimentos) para evitar loops infinitos. Cada componente RGB é calculado independentemente e clamped ao intervalo [0, 1] antes da conversão para o espaço de cor da imagem final.

---

## Questão 2 — Decomposição numérica de 142.981

### Técnica utilizada: **Few-Shot Prompting (Poucos exemplos)**

A decomposição numérica segue um padrão claro e repetitivo. Ao fornecer exemplos do formato esperado, a IA compreende exatamente a estrutura desejada e aplica o mesmo padrão ao número solicitado, evitando ambiguidade.

### Prompt

```
Realize a decomposição numérica do número abaixo, seguindo o padrão dos exemplos.

Exemplo 1:
Número: 3.256
Decomposição: 3.000 + 200 + 50 + 6

Exemplo 2:
Número: 87.413
Decomposição: 80.000 + 7.000 + 400 + 10 + 3

Agora faça:
Número: 142.981
Decomposição:
```

### Resposta

**Número: 142.981**

**Decomposição:** 100.000 + 40.000 + 2.000 + 900 + 80 + 1

Explicação por posição:

| Algarismo | Posição              | Valor   |
|-----------|----------------------|---------|
| 1         | Centena de milhar    | 100.000 |
| 4         | Dezena de milhar     | 40.000  |
| 2         | Unidade de milhar    | 2.000   |
| 9         | Centena              | 900     |
| 8         | Dezena               | 80      |
| 1         | Unidade              | 1       |

Soma: 100.000 + 40.000 + 2.000 + 900 + 80 + 1 = **142.981** ✓

---

## Questão 3 — Personagens de As Crônicas de Gelo e Fogo com características de Maquiavel

### Técnica utilizada: **Role Prompting (Atribuição de Papel) + Contextualização**

Esta questão exige conhecimento cruzado entre literatura de fantasia e filosofia política. Atribuir um papel especializado à IA (acadêmico de filosofia e literatura) garante respostas mais profundas e fundamentadas, enquanto a contextualização dos conceitos de Maquiavel estabelece o framework analítico.

### Prompt

```
Assuma o papel de um acadêmico especialista em filosofia política e literatura
de fantasia. Considere os princípios centrais de Maquiavel em "O Príncipe":
a separação entre moral e política, o uso estratégico da força e da astúcia
("leão e raposa"), a importância das aparências, o pragmatismo acima do idealismo,
e o conceito de "virtù" (capacidade de adaptar-se à fortuna).

Com base nesses princípios, identifique quais personagens de "As Crônicas de
Gelo e Fogo" (George R.R. Martin) possuem características claramente inspiradas
na filosofia maquiavélica. Para cada personagem, explique qual princípio de
Maquiavel se manifesta e dê exemplos concretos da narrativa.
```

### Resposta

#### 1. **Tywin Lannister** — O Príncipe pragmático por excelência

**Princípio:** Pragmatismo acima da moral; a força do leão.

Tywin é a personificação do governante maquiavélico que subordina toda a ética à eficácia política. Ele orquestra o **Casamento Vermelho** (a quebra do sagrado direito de hospitalidade) para destruir a Casa Stark sem perder um único soldado Lannister, demonstrando que "os fins justificam os meios". Maquiavel escreveu que o príncipe deve saber "entrar no mal, quando necessário" — Tywin faz isso sem hesitação. Sua frase icônica "um leão não se preocupa com a opinião das ovelhas" ecoa diretamente o conceito maquiavélico de que é melhor ser temido do que amado.

#### 2. **Cersei Lannister** — A manipulação das aparências (sem virtù)

**Princípio:** Importância das aparências; separação moral-política.

Cersei compreende a lição de Maquiavel de que "todos veem o que pareces, poucos sentem o que és". Ela manipula aparências, conspira e usa intrigas para manter o poder. Porém, é o exemplo do governante que Maquiavel alertaria: possui ambição sem *virtù*. Ela não sabe adaptar-se às circunstâncias, age por impulso vingativo e subestima adversários, o que a leva à ruína progressiva — exatamente o tipo de governante que Maquiavel dizia ser destruído pela fortuna.

#### 3. **Petyr Baelish (Mindinho)** — A raposa astuta

**Princípio:** A astúcia da raposa; manipulação e oportunismo.

Mindinho é a metáfora perfeita da "raposa" de Maquiavel. Nascido em uma casa menor, sem exércitos ou linhagem, ele escala o poder exclusivamente pela inteligência, manipulação e capacidade de criar caos para então oferecer soluções. Sua frase "o caos é uma escada" é essencialmente maquiavélica. Ele trai Ned Stark, orquestra o assassinato de Jon Arryn e manipula o casamento dos Tyrell — tudo sem jamais empunhar uma espada. Maquiavel diria que ele "sabe usar a natureza da raposa" com maestria.

#### 4. **Varys** — O conselheiro do bem público (contraponto a Mindinho)

**Princípio:** O pragmatismo a serviço do "bem do reino"; virtù coletiva.

Varys representa uma leitura mais republicana de Maquiavel (dos *Discorsi*), onde o pragmatismo serve ao bem comum, não ao indivíduo. Ele conspira, mente e assassina, mas sempre justifica suas ações pela estabilidade do reino e pelo bem do povo. Sua rede de espiões ("passarinhos") é o aparato de inteligência que Maquiavel considerava indispensável a qualquer governante. A tensão entre Varys e Mindinho reflete o debate maquiavélico entre o poder como instrumento público versus instrumento pessoal.

#### 5. **Olenna Tyrell** — A virtù na velhice

**Princípio:** Adaptação à fortuna; a aliança como arma.

A Rainha dos Espinhos exemplifica a *virtù* maquiavélica — a capacidade de adaptar-se constantemente às circunstâncias. Ela envenena Joffrey não por vingança, mas por cálculo político puro: proteger sua neta Margaery de um rei sádico. Forma alianças pragmáticas (primeiro com os Lannister, depois com Daenerys) conforme o cenário muda. Maquiavel aconselhava "não se casar com a derrota" — Olenna troca de lado sem pestanejar quando a situação exige.

#### 6. **Daenerys Targaryen** — A tensão entre idealismo e necessidade

**Princípio:** O conflito entre ser amado e ser temido.

Daenerys ilustra o dilema central de Maquiavel. Ela deseja ser amada e libertadora, mas repetidamente descobre que governar exige dureza. Crucifica os Mestres de Meereen, executa Randyll e Dickon Tarly, e eventualmente queima Porto Real — uma escalada que demonstra a tese maquiavélica de que "é mais seguro ser temido do que amado, quando se tem que escolher entre os dois". Seu arco trágico é o de um governante que falha em equilibrar as duas forças.

---

## Questão 4 — Endpoint FastAPI com validação

### Técnica utilizada: **Instruction Prompting com especificações técnicas detalhadas**

Para geração de código, a técnica mais eficaz é fornecer instruções claras e específicas com todas as restrições técnicas explícitas. Isso elimina ambiguidades e garante que a IA gere código funcional que atenda exatamente aos requisitos.

### Prompt

```
Crie um endpoint POST com FastAPI que receba e valide um objeto "Item" com os
seguintes campos e regras:

1. nome: string, máximo 25 caracteres
2. valor: float
3. data: tipo date, não pode ser superior à data atual (hoje)

Validações:
- Use Pydantic v2 com field_validator para a validação da data
- Use Field() com max_length para limitar o nome

Após validar, retorne o corpo da requisição acrescido de um campo "uuid"
contendo um UUID4 gerado dinamicamente.

Retorne status 201. Use tipagem completa. Inclua apenas o código necessário.
```

### Resposta

```python
from datetime import date
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class Item(BaseModel):
    nome: str = Field(..., max_length=25)
    valor: float
    data: date

    @field_validator("data")
    @classmethod
    def data_nao_pode_ser_futura(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("A data não pode ser superior à data atual.")
        return v


class ItemResponse(Item):
    uuid: str


@app.post("/items", response_model=ItemResponse, status_code=201)
def criar_item(item: Item) -> ItemResponse:
    return ItemResponse(**item.model_dump(), uuid=str(uuid4()))
```

**Como testar:**

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Requisição de exemplo:

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"nome": "Teclado Mecânico", "valor": 299.90, "data": "2025-03-15"}'
```

Resposta esperada (status 201):

```json
{
  "nome": "Teclado Mecânico",
  "valor": 299.9,
  "data": "2025-03-15",
  "uuid": "a3f1b2c4-5d6e-7f8a-9b0c-1d2e3f4a5b6c"
}
```

Validações automáticas:
- Se `nome` tiver mais de 25 caracteres → erro 422
- Se `data` for no futuro → erro 422 com a mensagem "A data não pode ser superior à data atual."
- Se `valor` não for numérico → erro 422

---

## Resumo das técnicas aplicadas

| Questão | Tema | Técnica |
|---------|------|---------|
| 1 | Ray Tracing | **Chain-of-Thought** — raciocínio passo a passo para processo técnico |
| 2 | Decomposição numérica | **Few-Shot Prompting** — exemplos definem o formato esperado |
| 3 | Gelo e Fogo × Maquiavel | **Role Prompting + Contextualização** — papel de especialista com framework filosófico |
| 4 | FastAPI endpoint | **Instruction Prompting** — especificações técnicas precisas e detalhadas |
