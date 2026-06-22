## C:\dev\PythonProject_v4\bin\audit_io.py

- **bin.audit_io._Visitor.__init__(self, module_name)** -> `None`
- **bin.audit_io._Visitor.visit_ClassDef(self, node)** -> `None`
  - calls: self.generic_visit, self.stack.append, self.stack.pop
- **bin.audit_io._Visitor.visit_FunctionDef(self, node)** -> `None`
  - calls: self._enter_func, self._exit_func, self.generic_visit
- **bin.audit_io._Visitor.visit_AsyncFunctionDef(self, node)** -> `None`
  - calls: self._enter_func, self._exit_func, self.generic_visit
- **bin.audit_io._Visitor._enter_func(self, node)** -> `None`
  - calls: '.'.join, FunctionIO, args.append, ast.get_docstring, ast.unparse, getattr, isinstance, self.results.append
- **bin.audit_io._Visitor._exit_func(self)** -> `None`
- **bin.audit_io._Visitor.visit_Raise(self, node)** -> `None`
  - calls: ast.unparse, self._current.raises.append, self.generic_visit
- **bin.audit_io._Visitor.visit_Call(self, node)** -> `None`
  - calls: ast.unparse, self._current.calls.append, self.generic_visit
- **bin.audit_io.find_project_root(start)** -> `Path`
  - calls: (parent / m).exists, any, start.resolve
  - doc: Remonte jusqu'à trouver un marqueur de racine de projet.
- **bin.audit_io.iter_py_files(root)** -> `Iterable[Path]`
  - calls: root.rglob, set
- **bin.audit_io.module_name_from_path(root, path)** -> `str`
  - calls: '.'.join, path.relative_to, path.relative_to(root).with_suffix
- **bin.audit_io.read_text_robust(path)** -> `tuple[str | None, str | None]`
  - calls: path.read_text, type
  - doc: Retourne (texte, erreur). Essaie plusieurs encodages pour éviter de skipper des fichiers.
- **bin.audit_io.main()** -> `None`
  - calls: ', '.join, '\n'.join, '\n'.join(out).strip, (project_root / 'AUDIT_IO.md').write_text, (project_root / 'AUDIT_IO_SKIPPED.md').write_text, Path.cwd, _Visitor, ast.parse, f.doc.strip, f.doc.strip().splitlines, find_project_root, iter_py_files, len, module_name_from_path, out.append ...

## C:\dev\PythonProject_v4\bin\generate_tree.py

- **bin.generate_tree.list_children(directory, include_hidden, ignored_dirs, ignored_exts)** -> `list[Path]`
  - calls: directory.iterdir
  - doc: Retourne les enfants filtrés et triés (dossiers d'abord, puis fichiers).
- **bin.generate_tree.keep(p)** -> `bool`
  - calls: name.startswith, p.is_dir, p.is_file
- **bin.generate_tree.build_tree_lines(root, prefix, include_hidden, ignored_dirs, ignored_exts)** -> `list[str]`
  - calls: build_tree_lines, child.is_dir, child.is_symlink, enumerate, len, lines.append, lines.extend, list_children
  - doc: Construit récursivement les lignes de l'arborescence à partir de `root`.
- **bin.generate_tree.generate_tree(root, output, include_hidden, ignored_dirs, ignored_exts)** -> `None`
  - calls: '\n'.join, build_tree_lines, lines.append, lines.extend, output.write_text, root.resolve, set
  - doc: Génère le fichier d'arborescence à partir des paramètres fournis.
- **bin.generate_tree.parse_args()** -> `argparse.Namespace`
  - calls: argparse.ArgumentParser, parser.add_argument, parser.parse_args
- **bin.generate_tree.main()** -> `None`
  - calls: Path, Path(__file__).resolve, generate_tree, parse_args, print, set

## C:\dev\PythonProject_v4\ndc_core\common\errors.py

- **ndc_core.common.errors.ManagedError.to_message(self)** -> `EngineMessage`
  - calls: EngineMessage.error

## C:\dev\PythonProject_v4\ndc_core\common\messages.py

- **ndc_core.common.messages.EngineMessage.__post_init__(self)** -> `None`
  - calls: object.__setattr__, self.code.strip, self.text.strip
- **ndc_core.common.messages.EngineMessage.info(cls, code, text, context)** -> `EngineMessage`
  - calls: cls
- **ndc_core.common.messages.EngineMessage.warning(cls, code, text, context)** -> `EngineMessage`
  - calls: cls
- **ndc_core.common.messages.EngineMessage.error(cls, code, text, context)** -> `EngineMessage`
  - calls: cls
- **ndc_core.common.messages.EngineMessage.is_info(self)** -> `bool`
- **ndc_core.common.messages.EngineMessage.is_warning(self)** -> `bool`
- **ndc_core.common.messages.EngineMessage.is_error(self)** -> `bool`
- **ndc_core.common.messages.EngineMessage.to_dict(self)** -> `dict[str, Any]`
  - calls: dict

## C:\dev\PythonProject_v4\ndc_core\common\result.py

- **ndc_core.common.result.Result.success(cls, value, messages)** -> `Result[T]`
  - calls: _status_from_messages, cls, tuple
- **ndc_core.common.result.Result.partial(cls, value, messages)** -> `Result[T]`
  - calls: _status_from_messages, cls, tuple
- **ndc_core.common.result.Result.failure(cls, messages, value)** -> `Result[T]`
  - calls: cls, tuple
- **ndc_core.common.result.Result.ok(self)** -> `bool`
- **ndc_core.common.result.Result.failed(self)** -> `bool`
- **ndc_core.common.result.Result.has_messages(self)** -> `bool`
  - calls: bool
- **ndc_core.common.result.Result.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.common.result.Result.has_errors(self)** -> `bool`
  - calls: any
- **ndc_core.common.result.Result.errors(self)** -> `tuple[EngineMessage, ...]`
  - calls: tuple
- **ndc_core.common.result.Result.warnings(self)** -> `tuple[EngineMessage, ...]`
  - calls: tuple
- **ndc_core.common.result.Result.with_message(self, message)** -> `Result[T]`
  - calls: Result, _status_from_messages
- **ndc_core.common.result.Result.with_messages(self, messages)** -> `Result[T]`
  - calls: Result, _status_from_messages, tuple
- **ndc_core.common.result.Result.with_value(self, value)** -> `Result[T]`
  - calls: Result
- **ndc_core.common.result._status_from_messages(messages, default)** -> `ResultStatus`
  - calls: tuple

## C:\dev\PythonProject_v4\ndc_core\common\status.py

- **ndc_core.common.status.ResultStatus.is_success(self)** -> `bool`
- **ndc_core.common.status.ResultStatus.is_partial(self)** -> `bool`
- **ndc_core.common.status.ResultStatus.is_failure(self)** -> `bool`

## C:\dev\PythonProject_v4\tests\common\test_messages.py

- **tests.common.test_messages.test_engine_message_info_factory()** -> `None`
  - calls: EngineMessage.info
- **tests.common.test_messages.test_engine_message_warning_factory()** -> `None`
  - calls: EngineMessage.warning
- **tests.common.test_messages.test_engine_message_error_factory()** -> `None`
  - calls: EngineMessage.error
- **tests.common.test_messages.test_engine_message_normalizes_empty_code()** -> `None`
  - calls: EngineMessage.info
- **tests.common.test_messages.test_engine_message_to_dict()** -> `None`
  - calls: EngineMessage.warning, message.to_dict

## C:\dev\PythonProject_v4\tests\common\test_result.py

- **tests.common.test_result.test_success_result_without_message()** -> `None`
  - calls: Result.success
- **tests.common.test_result.test_success_result_with_warning_becomes_partial()** -> `None`
  - calls: EngineMessage.warning, Result.success, Result.success(value=42).with_message, len
- **tests.common.test_result.test_result_with_error_becomes_failure()** -> `None`
  - calls: EngineMessage.error, Result.success, Result.success(value=42).with_message, len
- **tests.common.test_result.test_failure_result()** -> `None`
  - calls: EngineMessage.error, Result.failure
- **tests.common.test_result.test_result_with_value_returns_new_result()** -> `None`
  - calls: Result.success, result.with_value
- **tests.common.test_result.test_managed_error_to_message()** -> `None`
  - calls: ManagedError, managed_error.to_message