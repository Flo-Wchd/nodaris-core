"""
generate_tree.py

Génère une arborescence texte du projet (type commande `tree`) sans dépendre
d'outils externes. Idéal pour documenter la structure d'un projet.

Usage de base (depuis la racine du projet) :
    python generate_tree.py

Options :
    --root <path>     Racine à analyser (par défaut: .)
    -o, --output      Fichier de sortie (par défaut: TREE.md)
    --include-hidden  Inclure les fichiers/dossiers cachés (commençant par .)
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

# --- Configuration par défaut -----------------------------------------------

# Dossiers ignorés par défaut (nom du dossier, pas le chemin complet)
DEFAULT_IGNORED_DIRS = {
    ".git",
    ".venv",
    ".idea",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".mypy_cache",
    "site",
    "dist",
    "build",
    "htmlcov",
    "out",
    "ndc_core.egg-info",
    "nodaris_core.egg-info",
    "htmlcov",
    "dist",
    "build",
    "out",
}

# Extensions de fichiers ignorées par défaut
DEFAULT_IGNORED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".log",
    ".tmp",
}

# -----------------------------------------------------------------------------


def list_children(
    directory: Path,
    include_hidden: bool,
    ignored_dirs: set[str],
    ignored_exts: set[str],
) -> list[Path]:
    """Retourne les enfants filtrés et triés (dossiers d'abord, puis fichiers)."""
    children: Iterable[Path] = directory.iterdir()

    def keep(p: Path) -> bool:
        name = p.name

        # Fichiers/dossiers cachés
        if not include_hidden and name.startswith("."):
            # On laisse quand même la racine "." déjà gérée ailleurs
            return False

        # Dossiers ignorés par nom
        if p.is_dir() and name in ignored_dirs:
            return False

        # Fichiers ignorés par extension
        if p.is_file() and p.suffix in ignored_exts:
            return False

        return True

    filtered = [p for p in children if keep(p)]

    # Dossiers en premier, puis fichiers, le tout trié alphabétiquement
    filtered.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    return filtered


def build_tree_lines(
    root: Path,
    prefix: str,
    include_hidden: bool,
    ignored_dirs: set[str],
    ignored_exts: set[str],
) -> list[str]:
    """
    Construit récursivement les lignes de l'arborescence à partir de `root`.
    """
    lines: list[str] = []
    children = list_children(root, include_hidden, ignored_dirs, ignored_exts)

    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "

        # Nom affiché
        display_name = child.name + ("/" if child.is_dir() else "")

        lines.append(f"{prefix}{connector}{display_name}")

        # Si c'est un dossier non-symlink, on descend
        if child.is_dir() and not child.is_symlink():
            extension = "    " if is_last else "│   "
            lines.extend(
                build_tree_lines(
                    child,
                    prefix + extension,
                    include_hidden=include_hidden,
                    ignored_dirs=ignored_dirs,
                    ignored_exts=ignored_exts,
                )
            )

    return lines


def generate_tree(
    root: Path,
    output: Path,
    include_hidden: bool = False,
    ignored_dirs: set[str] | None = None,
    ignored_exts: set[str] | None = None,
) -> None:
    """Génère le fichier d'arborescence à partir des paramètres fournis."""
    ignored_dirs = set(ignored_dirs or DEFAULT_IGNORED_DIRS)
    ignored_exts = set(ignored_exts or DEFAULT_IGNORED_EXTENSIONS)

    root = root.resolve()

    lines: list[str] = []

    # Première ligne : racine relative (.)
    lines.append(root.name)
    lines.extend(
        build_tree_lines(
            root,
            prefix="",
            include_hidden=include_hidden,
            ignored_dirs=ignored_dirs,
            ignored_exts=ignored_exts,
        )
    )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Génère un fichier d'arborescence du projet (type `tree`)."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Dossier racine à analyser (par défaut: .)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="TREE.md",
        help="Fichier de sortie (par défaut: TREE.md)",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Inclure les fichiers/dossiers cachés (commençant par un point).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    root = project_root if args.root is None else Path(args.root)

    output = (
        project_root / "TREE.md"
        if args.output == "TREE.md"
        else Path(args.output)
    )

    # Tu peux personnaliser ici des exclusions spécifiques à NDC si tu veux :
    ignored_dirs = set(DEFAULT_IGNORED_DIRS)
    # Exemple : si tu veux exclure le dossier "debug" systématiquement :
    # ignored_dirs.add("debug")

    generate_tree(
        root=root,
        output=output,
        include_hidden=args.include_hidden,
        ignored_dirs=ignored_dirs,
        ignored_exts=DEFAULT_IGNORED_EXTENSIONS,
    )
    print(f"Arborescence générée dans {output}")


if __name__ == "__main__":
    main()