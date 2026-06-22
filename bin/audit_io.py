from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class FunctionIO:
    qualname: str
    args: list[str] = field(default_factory=list)
    returns: str | None = None
    raises: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    doc: str | None = None


class _Visitor(ast.NodeVisitor):
    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        self.stack: list[str] = []
        self.results: list[FunctionIO] = []
        self._current: FunctionIO | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._enter_func(node)
        self.generic_visit(node)
        self._exit_func()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._enter_func(node)
        self.generic_visit(node)
        self._exit_func()

    def _enter_func(self, node: ast.AST) -> None:
        name = getattr(node, "name", "<lambda>")
        qual = ".".join([self.module_name, *self.stack, name])

        args: list[str] = []
        a = getattr(node, "args", None)
        if a:
            args = [arg.arg for arg in getattr(a, "posonlyargs", [])]
            args += [arg.arg for arg in getattr(a, "args", [])]
            if getattr(a, "vararg", None):
                args.append("*" + a.vararg.arg)
            args += [arg.arg for arg in getattr(a, "kwonlyargs", [])]
            if getattr(a, "kwarg", None):
                args.append("**" + a.kwarg.arg)

        returns = None
        ann = getattr(node, "returns", None)
        if ann is not None:
            try:
                returns = ast.unparse(ann)
            except Exception:
                returns = "<annotation>"

        doc = ast.get_docstring(node) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else None

        self._current = FunctionIO(qualname=qual, args=args, returns=returns, doc=doc)
        self.results.append(self._current)

    def _exit_func(self) -> None:
        self._current = None

    def visit_Raise(self, node: ast.Raise) -> None:
        if self._current is not None and node.exc is not None:
            try:
                self._current.raises.append(ast.unparse(node.exc))
            except Exception:
                self._current.raises.append("<raise>")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if self._current is not None:
            try:
                self._current.calls.append(ast.unparse(node.func))
            except Exception:
                self._current.calls.append("<call>")
        self.generic_visit(node)


def find_project_root(start: Path) -> Path:
    """
    Remonte jusqu'à trouver un marqueur de racine de projet.
    """
    markers = {"pyproject.toml", ".git", "mkdocs.yml"}
    cur = start.resolve()
    for parent in [cur, *cur.parents]:
        if any((parent / m).exists() for m in markers):
            return parent
    return cur


def iter_py_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.py"):
        parts = set(p.parts)
        if ".venv" in parts or "__pycache__" in parts or ".git" in parts:
            continue
        yield p


def module_name_from_path(root: Path, path: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    return ".".join(rel.parts)


def read_text_robust(path: Path) -> tuple[str | None, str | None]:
    """
    Retourne (texte, erreur). Essaie plusieurs encodages pour éviter de skipper des fichiers.
    """
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc), None
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return None, f"{type(e).__name__}: {e}"
    return None, "UnicodeDecodeError: unsupported encoding for this file"


def main() -> None:
    project_root = find_project_root(Path.cwd())
    out: list[str] = []
    skipped: list[str] = []

    for py in sorted(iter_py_files(project_root)):
        src, err = read_text_robust(py)
        if src is None:
            skipped.append(f"- {py} ({err})")
            continue

        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            out.append(f"\n## {py}\n- ❌ SyntaxError: {e}\n")
            continue

        mod = module_name_from_path(project_root, py)
        v = _Visitor(mod)
        v.visit(tree)

        if not v.results:
            continue

        out.append(f"\n## {py}\n")
        for f in v.results:
            out.append(f"- **{f.qualname}({', '.join(f.args)})** -> `{f.returns or 'None'}`")
            if f.raises:
                out.append(f"  - raises: {', '.join(sorted(set(f.raises)))}")
            if f.calls:
                calls = ", ".join(sorted(set(f.calls))[:15])
                out.append(f"  - calls: {calls}{' ...' if len(set(f.calls)) > 15 else ''}")
            if f.doc:
                first = f.doc.strip().splitlines()[0] if f.doc.strip() else ""
                if first:
                    out.append(f"  - doc: {first}")

    report = "\n".join(out).strip() or "No python functions found."
    (project_root / "AUDIT_IO.md").write_text(report, encoding="utf-8")

    if skipped:
        (project_root / "AUDIT_IO_SKIPPED.md").write_text("\n".join(skipped), encoding="utf-8")

    print(f"✅ Generated {project_root / 'AUDIT_IO.md'}")
    if skipped:
        print(f"⚠️ Skipped files listed in {project_root / 'AUDIT_IO_SKIPPED.md'}")


if __name__ == "__main__":
    main()