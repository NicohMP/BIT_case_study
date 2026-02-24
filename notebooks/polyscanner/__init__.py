"""
Notebook-friendly import shim.

When running kernels from the `notebooks/` directory, the project root isn't on
`sys.path`, so `import polyscanner` fails. This package extends its module
search path to include the real package in the project root.

This keeps notebook imports working without requiring an editable install.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import extend_path

# Allow `polyscanner.*` imports to be resolved from multiple directories.
__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

real_pkg_dir = Path(__file__).resolve().parents[2] / "polyscanner"
if real_pkg_dir.is_dir():
    __path__.append(str(real_pkg_dir))

