"""
Desafio Agentes IA — Geração de Roteiro e Thumbnails para Vídeos de Videogames.

Uso:
    python main.py                           # usa o tema padrão
    python main.py "Melhores jogos de 2020"  # tema personalizado
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

REQUIRED_KEYS = ["OPENAI_API_KEY", "SERPER_API_KEY"]


def _check_env() -> None:
    missing = [k for k in REQUIRED_KEYS if not os.getenv(k)]
    if missing:
        print(
            f"[ERRO] Variáveis de ambiente faltando: {', '.join(missing)}\n"
            "Crie um arquivo .env com base no .env.example."
        )
        sys.exit(1)


def main() -> None:
    _check_env()

    query = sys.argv[1] if len(sys.argv) > 1 else "Melhores jogos de 2020"
    print(f"\n{'='*60}")
    print(f"  Tema do vídeo: {query}")
    print(f"{'='*60}\n")

    Path("output").mkdir(exist_ok=True)

    from crew import build_crew

    crew = build_crew(query)
    result = crew.kickoff()

    print(f"\n{'='*60}")
    print("  Processo finalizado!")
    print(f"  Resultado salvo em: output/resultado_final.md")
    print(f"{'='*60}\n")
    print(result)


if __name__ == "__main__":
    main()
