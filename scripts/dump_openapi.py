"""Write the API's OpenAPI schema to packages/ts-client/openapi.json.

Deterministic (sorted keys) so the generated TypeScript client is stable and a CI drift
check can diff it. Run via ``just gen-client`` (which then regenerates the TS types).
"""

from __future__ import annotations

import json
from pathlib import Path

from hermes_api.main import create_app

OUTPUT = Path(__file__).resolve().parent.parent / "packages" / "ts-client" / "openapi.json"


def main() -> None:
    schema = create_app().openapi()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
