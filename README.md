# Desafio Agentes IA — Roteiro & Thumbnails para Vídeos de Videogames

Sistema multi-agentes com **CrewAI** que gera automaticamente roteiros para vídeos de YouTube sobre videogames e produz thumbnails com DALL-E 3.

## Arquitetura

```
query ──► Roteirista ──► Criador de Thumbnail ──► Revisor ──► resultado_final.md
            (SerperDevTool)    (DallETool)
```

| Agente | Função | Ferramentas |
|--------|--------|-------------|
| **Roteirista** | Pesquisa o tema e escreve o roteiro completo | SerperDevTool |
| **Criador de Thumbnail** | Gera 3 opções de thumbnail baseadas no roteiro | DallETool (DALL-E 3) |
| **Revisor** | Revisa o roteiro, escolhe a melhor thumbnail e compila o resultado final | — |

## Requisitos

- Python 3.10+
- Chave da API OpenAI (com acesso ao DALL-E 3)
- Chave da API Serper.dev

## Instalação

```bash
cd desafio-agentes-ia
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...
```

## Execução

```bash
# Tema padrão ("Melhores jogos de 2020")
python main.py

# Tema personalizado
python main.py "Os RPGs mais subestimados da história"
```

## Saída

O resultado final é salvo em `output/resultado_final.md` contendo:

1. Roteiro revisado e completo
2. Thumbnail escolhida com URL e justificativa
3. Parecer de qualidade

## Estrutura do Projeto

```
desafio-agentes-ia/
├── config/
│   ├── agents.yaml      # Definição dos agentes
│   └── tasks.yaml       # Definição das tarefas
├── output/              # Resultado gerado
├── .env.example         # Template de variáveis de ambiente
├── crew.py              # Montagem da crew (agentes + tarefas)
├── main.py              # Ponto de entrada
├── requirements.txt     # Dependências
└── README.md
```
