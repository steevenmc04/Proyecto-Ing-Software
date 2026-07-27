"""Prepara una base SQLite limpia y determinista para las pruebas E2E."""

from __future__ import annotations

import os
import sys
from pathlib import Path


URL_E2E = "sqlite:///./e2e_caja_ahorros.db"


def main() -> None:
    os.environ["DATABASE_URL"] = URL_E2E
    raiz = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(raiz))
    base = raiz / "e2e_caja_ahorros.db"
    base.unlink(missing_ok=True)

    from seed import main as cargar_datos

    cargar_datos()


if __name__ == "__main__":
    main()
