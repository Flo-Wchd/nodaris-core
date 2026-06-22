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

## C:\dev\PythonProject_v4\ndc_core\catalogs\appliance_catalog.py

- **ndc_core.catalogs.appliance_catalog.ApplianceCatalog.normalize_code(value)** -> `str`
  - calls: str, str(value or '').strip
- **ndc_core.catalogs.appliance_catalog.ApplianceCatalog.get(self, code)** -> `Appliance | None`
  - calls: normalized.lower, raw_code.lower, self.appliances_by_code.get, self.appliances_by_code.items, self.normalize_code
- **ndc_core.catalogs.appliance_catalog.ApplianceCatalog.list_codes(self)** -> `list[str]`
  - calls: sorted
- **ndc_core.catalogs.appliance_catalog.ApplianceCatalog.list_appliances(self)** -> `list[Appliance]`
  - calls: self.list_codes
- **ndc_core.catalogs.appliance_catalog.ApplianceCatalog.from_yaml_file(cls, path)** -> `Result[ApplianceCatalog]`
  - calls: Result.failure, appliances_path, cls.from_mapping, load_yaml_file, str
- **ndc_core.catalogs.appliance_catalog.ApplianceCatalog.from_mapping(cls, data, source)** -> `Result[ApplianceCatalog]`
  - calls: Appliance, EngineMessage.warning, Result.success, _first_number, _to_float, _to_optional_float, cls, cls.normalize_code, data.items, isinstance, messages.append, raw_item.get, str, tuple
- **ndc_core.catalogs.appliance_catalog._to_float(value, default)** -> `float`
  - calls: float
- **ndc_core.catalogs.appliance_catalog._to_optional_float(value)** -> `float | None`
  - calls: float
- **ndc_core.catalogs.appliance_catalog._first_number(*values)** -> `float | None`
  - calls: _to_optional_float

## C:\dev\PythonProject_v4\ndc_core\catalogs\fluid_catalog.py

- **ndc_core.catalogs.fluid_catalog.FluidCatalog.get(self, code)** -> `Fluid | None`
  - calls: code.strip, normalized.lower, raw_code.lower, self.fluids_by_code.get, self.fluids_by_code.items
- **ndc_core.catalogs.fluid_catalog.FluidCatalog.get_water_at_temperature(self, temperature_c)** -> `Fluid | None`
  - calls: Fluid, _lerp, sorted, zip
- **ndc_core.catalogs.fluid_catalog.FluidCatalog.from_yaml_file(cls, path)** -> `Result[FluidCatalog]`
  - calls: Result.failure, cls.from_mapping, load_yaml_file, str, water_atm_table_path
- **ndc_core.catalogs.fluid_catalog.FluidCatalog.from_mapping(cls, data, source)** -> `Result[FluidCatalog]`
  - calls: EngineMessage.error, EngineMessage.warning, Fluid, Result.failure, Result.success, _to_float, _to_optional_float, cls, cls._water_or_default, data.get, isinstance, messages.append, raw_point.get, tuple
- **ndc_core.catalogs.fluid_catalog.FluidCatalog._water_or_default(points, temperature_c, kind)** -> `Fluid`
  - calls: Fluid, kind.value.replace, kind.value.replace('_', ' ').title, points.get
- **ndc_core.catalogs.fluid_catalog._to_float(value, default)** -> `float`
  - calls: float
- **ndc_core.catalogs.fluid_catalog._to_optional_float(value)** -> `float | None`
  - calls: float
- **ndc_core.catalogs.fluid_catalog._lerp(lower, upper, ratio)** -> `float`

## C:\dev\PythonProject_v4\ndc_core\catalogs\loaders\catalog_paths.py

- **ndc_core.catalogs.loaders.catalog_paths.find_project_root(start)** -> `Path`
  - calls: (candidate / marker).exists, (start or Path.cwd()).resolve, Path.cwd, any
  - doc: Return the project root by walking upward from ``start``.
- **ndc_core.catalogs.loaders.catalog_paths.data_dir(project_root)** -> `Path`
  - calls: find_project_root
  - doc: Return the project data directory.
- **ndc_core.catalogs.loaders.catalog_paths.standards_dir(project_root)** -> `Path`
  - calls: data_dir
  - doc: Return the standards data directory.
- **ndc_core.catalogs.loaders.catalog_paths.appliances_path(project_root)** -> `Path`
  - calls: data_dir
- **ndc_core.catalogs.loaders.catalog_paths.pipes_path(project_root)** -> `Path`
  - calls: data_dir
- **ndc_core.catalogs.loaders.catalog_paths.singular_losses_cold_water_path(project_root)** -> `Path`
  - calls: data_dir
- **ndc_core.catalogs.loaders.catalog_paths.singular_losses_hot_water_path(project_root)** -> `Path`
  - calls: data_dir
- **ndc_core.catalogs.loaders.catalog_paths.water_atm_table_path(project_root)** -> `Path`
  - calls: data_dir

## C:\dev\PythonProject_v4\ndc_core\catalogs\loaders\yaml_loader.py

- **ndc_core.catalogs.loaders.yaml_loader.load_yaml_file(path)** -> `Result[dict[str, Any]]`
  - calls: EngineMessage.error, Result.failure, Result.success, isinstance, path.exists, path.read_text, str, type, yaml.safe_load
  - doc: Load a YAML file and return a managed Result.
- **ndc_core.catalogs.loaders.yaml_loader.require_mapping(data, key, source)** -> `Result[dict[str, Any]]`
  - calls: EngineMessage.error, Result.failure, Result.success, data.get, isinstance, type
  - doc: Return a child mapping from an already loaded YAML root.
- **ndc_core.catalogs.loaders.yaml_loader.optional_mapping(data, key)** -> `dict[str, Any]`
  - calls: data.get, isinstance
- **ndc_core.catalogs.loaders.yaml_loader.optional_list(data, key)** -> `list[Any]`
  - calls: data.get, isinstance

## C:\dev\PythonProject_v4\ndc_core\catalogs\pipe_catalog.py

- **ndc_core.catalogs.pipe_catalog.PipeCatalog.normalize_code(value)** -> `str`
  - calls: str, str(value or '').strip
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.get_material(self, code)** -> `PipeMaterial | None`
  - calls: self.materials_by_code.get, self.normalize_code
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.get_size(self, code)** -> `PipeSize | None`
  - calls: normalized.lower, raw_code.lower, self.normalize_code, self.sizes_by_code.get, self.sizes_by_code.items
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.list_material_codes(self)** -> `list[str]`
  - calls: sorted
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.list_size_codes(self)** -> `list[str]`
  - calls: sorted
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.list_sizes_for_material(self, material_code)** -> `list[PipeSize]`
  - calls: self.normalize_code, self.size_codes_by_material.get
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.from_yaml_file(cls, path)** -> `Result[PipeCatalog]`
  - calls: Result.failure, cls.from_mapping, load_yaml_file, pipes_path, str
- **ndc_core.catalogs.pipe_catalog.PipeCatalog.from_mapping(cls, data, source)** -> `Result[PipeCatalog]`
  - calls: EngineMessage.error, EngineMessage.warning, PipeMaterial, PipeSize, Result.failure, Result.success, _as_dict, _material_family_from_code, _roughness_mm_to_m, _to_float, _to_optional_float, cls, cls.normalize_code, data.get, design_defaults.get ...
- **ndc_core.catalogs.pipe_catalog._as_dict(value)** -> `dict[str, Any]`
  - calls: isinstance
- **ndc_core.catalogs.pipe_catalog._to_float(value, default)** -> `float`
  - calls: float
- **ndc_core.catalogs.pipe_catalog._to_optional_float(value)** -> `float | None`
  - calls: float
- **ndc_core.catalogs.pipe_catalog._roughness_mm_to_m(value)** -> `float`
  - calls: _to_float, max
- **ndc_core.catalogs.pipe_catalog._material_family_from_code(value)** -> `PipeMaterialFamily`
  - calls: value.strip, value.strip().lower, value.strip().lower().replace

## C:\dev\PythonProject_v4\ndc_core\catalogs\singular_loss_catalog.py

- **ndc_core.catalogs.singular_loss_catalog.SingularLossCatalog.normalize_key(value)** -> `str`
  - calls: str, str(value or '').strip, str(value or '').strip().lower, text.replace, text.replace('-', '_').replace
- **ndc_core.catalogs.singular_loss_catalog.SingularLossCatalog.get(self, code)** -> `SingularLoss | None`
  - calls: self.losses_by_code.get, self.losses_by_code.items, self.mappings_by_keyword.get, self.normalize_key
- **ndc_core.catalogs.singular_loss_catalog.SingularLossCatalog.resolve_loss_code(self, keyword_or_code)** -> `str | None`
  - calls: self.normalize_key
- **ndc_core.catalogs.singular_loss_catalog.SingularLossCatalog.list_codes(self)** -> `list[str]`
  - calls: sorted
- **ndc_core.catalogs.singular_loss_catalog.SingularLossCatalog.from_yaml_file(cls, path)** -> `Result[SingularLossCatalog]`
  - calls: Result.failure, cls.from_mapping, load_yaml_file, singular_losses_cold_water_path, str
- **ndc_core.catalogs.singular_loss_catalog.SingularLossCatalog.from_mapping(cls, data, source)** -> `Result[SingularLossCatalog]`
  - calls: Result.success, _load_k_catalog, _load_kv_catalog, _load_mappings, cls, tuple
- **ndc_core.catalogs.singular_loss_catalog._load_k_catalog(data, source, losses, messages)** -> `None`
  - calls: EngineMessage.warning, SingularLoss, _to_optional_float, data.get, isinstance, messages.append, raw_catalog.items, raw_group.get, raw_item.get, str, str(raw_item.get('id') or '').strip
- **ndc_core.catalogs.singular_loss_catalog._load_kv_catalog(data, source, losses, messages)** -> `None`
  - calls: EngineMessage.warning, SingularLoss, _to_float, data.get, dn_kv.values, isinstance, max, messages.append, raw_catalog.items, raw_group.get, raw_item.get, str, str(raw_item.get('id') or '').strip
- **ndc_core.catalogs.singular_loss_catalog._load_mappings(data)** -> `dict[str, str]`
  - calls: SingularLossCatalog.normalize_key, by_keywords.items, data.get, isinstance, raw_mappings.get, str, str(value).strip
- **ndc_core.catalogs.singular_loss_catalog._to_float(value, default)** -> `float`
  - calls: float
- **ndc_core.catalogs.singular_loss_catalog._to_optional_float(value)** -> `float | None`
  - calls: float

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

## C:\dev\PythonProject_v4\ndc_core\domain\appliances.py

- **ndc_core.domain.appliances.Appliance.__post_init__(self)** -> `None`
  - calls: max, object.__setattr__, self.code.strip, self.name.strip
- **ndc_core.domain.appliances.Appliance.has_cold_water(self)** -> `bool`
- **ndc_core.domain.appliances.Appliance.has_hot_water(self)** -> `bool`
- **ndc_core.domain.appliances.Appliance.total_reference_flow_l_s(self)** -> `float`
  - calls: max
  - doc: Reference flow used when the appliance is treated globally.

## C:\dev\PythonProject_v4\ndc_core\domain\fluids.py

- **ndc_core.domain.fluids.Fluid.__post_init__(self)** -> `None`
  - calls: max, object.__setattr__, self.code.strip, self.name.strip
- **ndc_core.domain.fluids.Fluid.kinematic_viscosity_m2_s(self)** -> `float`

## C:\dev\PythonProject_v4\ndc_core\domain\networks\cell.py

- **ndc_core.domain.networks.cell.Cell.__post_init__(self)** -> `None`
  - calls: int, max, self._normalize_appliance_code, self.appliance_counts.items, self.id.strip, self.name.strip
- **ndc_core.domain.networks.cell.Cell._normalize_appliance_code(value)** -> `str`
  - calls: str, str(value or '').strip
- **ndc_core.domain.networks.cell.Cell.set_appliance_count(self, appliance_code, count)** -> `None`
  - calls: int, max, self._normalize_appliance_code, self.appliance_counts.pop
  - doc: Set an appliance quantity. A non-positive value removes the appliance.
- **ndc_core.domain.networks.cell.Cell.add_appliance_count(self, appliance_code, count)** -> `None`
  - calls: int, max, self._normalize_appliance_code, self.get_appliance_count, self.set_appliance_count
  - doc: Add a quantity to an appliance already declared in the cell.
- **ndc_core.domain.networks.cell.Cell.get_appliance_count(self, appliance_code)** -> `int`
  - calls: int, max, self._normalize_appliance_code, self.appliance_counts.get
- **ndc_core.domain.networks.cell.Cell.remove_appliance(self, appliance_code)** -> `None`
  - calls: self._normalize_appliance_code, self.appliance_counts.pop
- **ndc_core.domain.networks.cell.Cell.has_appliances(self)** -> `bool`
  - calls: bool
- **ndc_core.domain.networks.cell.Cell.total_appliance_count(self)** -> `int`
  - calls: int, max, self.appliance_counts.values, sum
- **ndc_core.domain.networks.cell.Cell.copy_appliance_counts(self)** -> `dict[str, int]`
  - calls: dict

## C:\dev\PythonProject_v4\ndc_core\domain\networks\network.py

- **ndc_core.domain.networks.network.Network.__post_init__(self)** -> `None`
  - calls: self.id.strip, self.name.strip
- **ndc_core.domain.networks.network.Network.add_cell(self, cell)** -> `None`
- **ndc_core.domain.networks.network.Network.add_node(self, node)** -> `None`
- **ndc_core.domain.networks.network.Network.add_section(self, section)** -> `None`
  - calls: downstream_node.add_upstream_section_id, self.nodes.get, upstream_node.add_downstream_section_id
- **ndc_core.domain.networks.network.Network.get_cell(self, cell_id)** -> `Cell | None`
  - calls: cell_id.strip, self.cells.get
- **ndc_core.domain.networks.network.Network.get_node(self, node_id)** -> `Node | None`
  - calls: node_id.strip, self.nodes.get
- **ndc_core.domain.networks.network.Network.get_section(self, section_id)** -> `Section | None`
  - calls: section_id.strip, self.sections.get
- **ndc_core.domain.networks.network.Network.attach_cell_to_node(self, cell_id, node_id)** -> `bool`
  - calls: node.attach_cell, self.get_cell, self.get_node
- **ndc_core.domain.networks.network.Network.remove_section(self, section_id)** -> `None`
  - calls: node.remove_section_id, section_id.strip, self.nodes.values, self.sections.pop
- **ndc_core.domain.networks.network.Network.remove_node(self, node_id)** -> `None`
  - calls: node_id.strip, self.nodes.pop, self.remove_section, self.sections.values
- **ndc_core.domain.networks.network.Network.downstream_sections_of(self, node_id)** -> `list[Section]`
  - calls: self.get_node, self.sections.get
- **ndc_core.domain.networks.network.Network.upstream_sections_of(self, node_id)** -> `list[Section]`
  - calls: self.get_node, self.sections.get
- **ndc_core.domain.networks.network.Network.source_nodes(self)** -> `list[Node]`
  - calls: self.nodes.values
- **ndc_core.domain.networks.network.Network.terminal_nodes(self)** -> `list[Node]`
  - calls: self.nodes.values
- **ndc_core.domain.networks.network.Network.clear_calculation_state(self)** -> `None`
  - calls: node.clear_pressure, section.clear_calculation_state, self.nodes.values, self.sections.values
- **ndc_core.domain.networks.network.Network.validate_topology(self)** -> `tuple[EngineMessage, ...]`
  - calls: EngineMessage.error, EngineMessage.warning, messages.append, self.sections.values, tuple
  - doc: Return managed topology messages.

## C:\dev\PythonProject_v4\ndc_core\domain\networks\node.py

- **ndc_core.domain.networks.node.Node.__post_init__(self)** -> `None`
  - calls: max, self.id.strip, self.name.strip
- **ndc_core.domain.networks.node.Node.attach_cell(self, cell)** -> `None`
  - calls: all, self.cells.append
  - doc: Attach a cell if another cell with the same id is not already attached.
- **ndc_core.domain.networks.node.Node.detach_cell(self, cell_id)** -> `None`
  - calls: cell_id.strip
- **ndc_core.domain.networks.node.Node.get_cell(self, cell_id)** -> `Cell | None`
  - calls: cell_id.strip
- **ndc_core.domain.networks.node.Node.has_cells(self)** -> `bool`
  - calls: bool
- **ndc_core.domain.networks.node.Node.local_appliance_counts(self)** -> `dict[str, int]`
  - calls: cell.appliance_counts.items, counts.get, int, max
- **ndc_core.domain.networks.node.Node.add_upstream_section_id(self, section_id)** -> `None`
  - calls: section_id.strip, self.upstream_section_ids.append
- **ndc_core.domain.networks.node.Node.add_downstream_section_id(self, section_id)** -> `None`
  - calls: section_id.strip, self.downstream_section_ids.append
- **ndc_core.domain.networks.node.Node.remove_section_id(self, section_id)** -> `None`
  - calls: section_id.strip
- **ndc_core.domain.networks.node.Node.set_pressure_bar(self, pressure_bar)** -> `None`
  - calls: max
- **ndc_core.domain.networks.node.Node.get_pressure_bar(self)** -> `float | None`
- **ndc_core.domain.networks.node.Node.clear_pressure(self)** -> `None`

## C:\dev\PythonProject_v4\ndc_core\domain\networks\section.py

- **ndc_core.domain.networks.section.Section.__post_init__(self)** -> `None`
  - calls: max, self.downstream_node_id.strip, self.fluid_code.strip, self.id.strip, self.name.strip, self.upstream_node_id.strip
- **ndc_core.domain.networks.section.Section.diameter_mode(self)** -> `DiameterMode`
- **ndc_core.domain.networks.section.Section.has_forced_diameter(self)** -> `bool`
- **ndc_core.domain.networks.section.Section.used_internal_diameter_mm(self)** -> `float | None`
- **ndc_core.domain.networks.section.Section.total_pressure_loss_pa(self)** -> `float | None`
  - calls: all, sum
- **ndc_core.domain.networks.section.Section.set_downstream_appliance_count(self, appliance_code, count)** -> `None`
  - calls: appliance_code.strip, int, max, self.downstream_appliance_counts.pop
- **ndc_core.domain.networks.section.Section.set_effective_appliance_count(self, appliance_code, count)** -> `None`
  - calls: appliance_code.strip, int, max, self.effective_appliance_counts.pop
- **ndc_core.domain.networks.section.Section.add_singular_loss(self, singular_loss)** -> `None`
  - calls: self.singular_losses.append
- **ndc_core.domain.networks.section.Section.clear_calculation_state(self)** -> `None`
  - calls: self.downstream_appliance_counts.clear, self.effective_appliance_counts.clear
  - doc: Clear calculation outputs while preserving geometry, topology and manual inputs.
- **ndc_core.domain.networks.section.Section.as_debug_dict(self)** -> `dict[str, Any]`
  - calls: dict, len

## C:\dev\PythonProject_v4\ndc_core\domain\pipes.py

- **ndc_core.domain.pipes.PipeMaterial.__post_init__(self)** -> `None`
  - calls: max, object.__setattr__, self.code.strip, self.name.strip
- **ndc_core.domain.pipes.PipeSize.__post_init__(self)** -> `None`
  - calls: max, object.__setattr__, self.code.strip, self.material_code.strip, self.nominal_diameter.strip
- **ndc_core.domain.pipes.PipeSize.internal_diameter_m(self)** -> `float`
- **ndc_core.domain.pipes.PipeSize.internal_area_m2(self)** -> `float`
- **ndc_core.domain.pipes.PipeSize.is_usable(self)** -> `bool`

## C:\dev\PythonProject_v4\ndc_core\domain\singular_losses.py

- **ndc_core.domain.singular_losses.SingularLoss.__post_init__(self)** -> `None`
  - calls: max, object.__setattr__, self.code.strip, self.name.strip
- **ndc_core.domain.singular_losses.SingularLoss.is_zeta_based(self)** -> `bool`
- **ndc_core.domain.singular_losses.SingularLoss.is_kv_based(self)** -> `bool`
- **ndc_core.domain.singular_losses.SingularLoss.is_active(self)** -> `bool`

## C:\dev\PythonProject_v4\tests\catalogs\test_appliance_catalog.py

- **tests.catalogs.test_appliance_catalog.test_appliance_catalog_from_mapping()** -> `None`
  - calls: ApplianceCatalog.from_mapping, catalog.get
- **tests.catalogs.test_appliance_catalog.test_appliance_catalog_ignores_invalid_entries_with_warning()** -> `None`
  - calls: ApplianceCatalog.from_mapping
- **tests.catalogs.test_appliance_catalog.test_appliance_catalog_lists_codes()** -> `None`
  - calls: ApplianceCatalog.from_mapping, result.value.list_codes

## C:\dev\PythonProject_v4\tests\catalogs\test_catalog_paths.py

- **tests.catalogs.test_catalog_paths.test_find_project_root_from_nested_directory(tmp_path)** -> `None`
  - calls: (root / 'pyproject.toml').write_text, find_project_root, nested.mkdir
- **tests.catalogs.test_catalog_paths.test_catalog_paths_from_project_root(tmp_path)** -> `None`
  - calls: appliances_path, data_dir, pipes_path, root.mkdir, singular_losses_cold_water_path, singular_losses_hot_water_path, standards_dir, water_atm_table_path

## C:\dev\PythonProject_v4\tests\catalogs\test_fluid_catalog.py

- **tests.catalogs.test_fluid_catalog.test_fluid_catalog_from_mapping()** -> `None`
  - calls: FluidCatalog.from_mapping, catalog.get
- **tests.catalogs.test_fluid_catalog.test_fluid_catalog_interpolates_water_temperature()** -> `None`
  - calls: FluidCatalog.from_mapping, result.value.get_water_at_temperature
- **tests.catalogs.test_fluid_catalog.test_fluid_catalog_invalid_table_returns_failure()** -> `None`
  - calls: FluidCatalog.from_mapping

## C:\dev\PythonProject_v4\tests\catalogs\test_pipe_catalog.py

- **tests.catalogs.test_pipe_catalog.test_pipe_catalog_from_mapping()** -> `None`
  - calls: PipeCatalog.from_mapping, catalog.get_material, catalog.get_size
- **tests.catalogs.test_pipe_catalog.test_pipe_catalog_invalid_families_returns_failure()** -> `None`
  - calls: PipeCatalog.from_mapping
- **tests.catalogs.test_pipe_catalog.test_pipe_catalog_lists_sizes_for_material()** -> `None`
  - calls: PipeCatalog.from_mapping, result.value.list_sizes_for_material

## C:\dev\PythonProject_v4\tests\catalogs\test_real_catalog_file.py

- **tests.catalogs.test_real_catalog_file.test_real_appliance_catalog_file_loads()** -> `None`
  - calls: ApplianceCatalog.from_yaml_file, result.value.list_codes
- **tests.catalogs.test_real_catalog_file.test_real_pipe_catalog_file_loads()** -> `None`
  - calls: PipeCatalog.from_yaml_file, result.value.list_material_codes, result.value.list_size_codes
- **tests.catalogs.test_real_catalog_file.test_real_singular_loss_catalog_file_loads()** -> `None`
  - calls: SingularLossCatalog.from_yaml_file, result.value.list_codes
- **tests.catalogs.test_real_catalog_file.test_real_fluid_catalog_file_loads()** -> `None`
  - calls: FluidCatalog.from_yaml_file, result.value.get, result.value.get_water_at_temperature

## C:\dev\PythonProject_v4\tests\catalogs\test_singular_loss_catalog.py

- **tests.catalogs.test_singular_loss_catalog.test_singular_loss_catalog_from_mapping()** -> `None`
  - calls: SingularLossCatalog.from_mapping, catalog.get
- **tests.catalogs.test_singular_loss_catalog.test_singular_loss_catalog_resolve_loss_code()** -> `None`
  - calls: SingularLossCatalog.from_mapping, result.value.resolve_loss_code
- **tests.catalogs.test_singular_loss_catalog.test_singular_loss_catalog_invalid_k_catalog_adds_warning()** -> `None`
  - calls: SingularLossCatalog.from_mapping

## C:\dev\PythonProject_v4\tests\catalogs\test_yaml_loader.py

- **tests.catalogs.test_yaml_loader.test_load_yaml_file_success(tmp_path)** -> `None`
  - calls: load_yaml_file, path.write_text
- **tests.catalogs.test_yaml_loader.test_load_yaml_file_missing_file_returns_failure(tmp_path)** -> `None`
  - calls: load_yaml_file
- **tests.catalogs.test_yaml_loader.test_load_yaml_file_invalid_yaml_returns_failure(tmp_path)** -> `None`
  - calls: load_yaml_file, path.write_text
- **tests.catalogs.test_yaml_loader.test_load_yaml_file_empty_yaml_returns_empty_dict(tmp_path)** -> `None`
  - calls: load_yaml_file, path.write_text
- **tests.catalogs.test_yaml_loader.test_load_yaml_file_non_mapping_root_returns_failure(tmp_path)** -> `None`
  - calls: load_yaml_file, path.write_text
- **tests.catalogs.test_yaml_loader.test_require_mapping_success()** -> `None`
  - calls: require_mapping
- **tests.catalogs.test_yaml_loader.test_require_mapping_missing_returns_failure()** -> `None`
  - calls: require_mapping
- **tests.catalogs.test_yaml_loader.test_require_mapping_invalid_returns_failure()** -> `None`
  - calls: require_mapping
- **tests.catalogs.test_yaml_loader.test_optional_helpers()** -> `None`
  - calls: optional_list, optional_mapping

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

## C:\dev\PythonProject_v4\tests\domain\networks\test_cell.py

- **tests.domain.networks.test_cell.test_cell_normalizes_identity()** -> `None`
  - calls: Cell
- **tests.domain.networks.test_cell.test_cell_set_appliance_count()** -> `None`
  - calls: Cell, cell.get_appliance_count, cell.set_appliance_count
- **tests.domain.networks.test_cell.test_cell_removes_appliance_when_count_is_zero()** -> `None`
  - calls: Cell, cell.get_appliance_count, cell.set_appliance_count
- **tests.domain.networks.test_cell.test_cell_add_appliance_count()** -> `None`
  - calls: Cell, cell.add_appliance_count, cell.get_appliance_count
- **tests.domain.networks.test_cell.test_cell_copy_appliance_counts_is_independent()** -> `None`
  - calls: Cell, cell.copy_appliance_counts, cell.get_appliance_count

## C:\dev\PythonProject_v4\tests\domain\networks\test_network.py

- **tests.domain.networks.test_network.test_network_add_entities()** -> `None`
  - calls: Cell, Network, Node, Section, network.add_cell, network.add_node, network.add_section, network.get_cell, network.get_node, network.get_section
- **tests.domain.networks.test_network.test_network_attach_cell_to_node()** -> `None`
  - calls: Cell, Network, Node, network.add_cell, network.add_node, network.attach_cell_to_node, network.get_node
- **tests.domain.networks.test_network.test_network_attach_cell_to_unknown_node_returns_false()** -> `None`
  - calls: Cell, Network, network.add_cell, network.attach_cell_to_node
- **tests.domain.networks.test_network.test_network_downstream_and_upstream_sections()** -> `None`
  - calls: Network, Node, Section, network.add_node, network.add_section, network.downstream_sections_of, network.upstream_sections_of
- **tests.domain.networks.test_network.test_network_source_and_terminal_nodes()** -> `None`
  - calls: Network, Node, network.add_node
- **tests.domain.networks.test_network.test_network_remove_section_updates_nodes()** -> `None`
  - calls: Network, Node, Section, network.add_node, network.add_section, network.get_node, network.remove_section
- **tests.domain.networks.test_network.test_network_validate_topology_detects_missing_node()** -> `None`
  - calls: Network, Node, Section, any, network.add_node, network.add_section, network.validate_topology
- **tests.domain.networks.test_network.test_network_clear_calculation_state()** -> `None`
  - calls: Network, Node, Section, network.add_node, network.add_section, network.clear_calculation_state, node.set_pressure_bar

## C:\dev\PythonProject_v4\tests\domain\networks\test_node.py

- **tests.domain.networks.test_node.test_node_normalizes_identity()** -> `None`
  - calls: Node
- **tests.domain.networks.test_node.test_node_attach_cell_once()** -> `None`
  - calls: Cell, Node, len, node.attach_cell, node.get_cell
- **tests.domain.networks.test_node.test_node_detach_cell()** -> `None`
  - calls: Cell, Node, node.attach_cell, node.detach_cell
- **tests.domain.networks.test_node.test_node_local_appliance_counts()** -> `None`
  - calls: Cell, Node, node.attach_cell
- **tests.domain.networks.test_node.test_node_section_references()** -> `None`
  - calls: Node, node.add_downstream_section_id, node.add_upstream_section_id, node.remove_section_id
- **tests.domain.networks.test_node.test_node_pressure_helpers()** -> `None`
  - calls: Node, node.clear_pressure, node.get_pressure_bar, node.set_pressure_bar

## C:\dev\PythonProject_v4\tests\domain\networks\test_section.py

- **tests.domain.networks.test_section.test_section_normalizes_identity_and_geometry()** -> `None`
  - calls: Section
- **tests.domain.networks.test_section.test_section_diameter_mode_automatic()** -> `None`
  - calls: Section
- **tests.domain.networks.test_section.test_section_diameter_mode_forced_pipe()** -> `None`
  - calls: Section
- **tests.domain.networks.test_section.test_section_diameter_mode_forced_internal_diameter()** -> `None`
  - calls: Section
- **tests.domain.networks.test_section.test_section_total_pressure_loss()** -> `None`
  - calls: Section
- **tests.domain.networks.test_section.test_section_appliance_counts()** -> `None`
  - calls: Section, section.set_downstream_appliance_count, section.set_effective_appliance_count
- **tests.domain.networks.test_section.test_section_add_singular_loss_only_when_active()** -> `None`
  - calls: Section, SingularLoss, len, section.add_singular_loss
- **tests.domain.networks.test_section.test_section_clear_calculation_state_preserves_inputs()** -> `None`
  - calls: Section, section.clear_calculation_state, section.set_downstream_appliance_count

## C:\dev\PythonProject_v4\tests\domain\test_appliances.py

- **tests.domain.test_appliances.test_appliance_normalizes_code_and_name()** -> `None`
  - calls: Appliance
- **tests.domain.test_appliances.test_appliance_negative_flows_are_clamped_to_zero()** -> `None`
  - calls: Appliance
- **tests.domain.test_appliances.test_appliance_water_flags()** -> `None`
  - calls: Appliance
- **tests.domain.test_appliances.test_appliance_total_reference_flow_uses_most_demanding_side()** -> `None`
  - calls: Appliance

## C:\dev\PythonProject_v4\tests\domain\test_fluids.py

- **tests.domain.test_fluids.test_fluid_normalizes_values()** -> `None`
  - calls: Fluid
- **tests.domain.test_fluids.test_fluid_negative_physical_values_are_clamped()** -> `None`
  - calls: Fluid
- **tests.domain.test_fluids.test_fluid_kinematic_viscosity()** -> `None`
  - calls: Fluid

## C:\dev\PythonProject_v4\tests\domain\test_pipes.py

- **tests.domain.test_pipes.test_pipe_material_normalizes_values()** -> `None`
  - calls: PipeMaterial
- **tests.domain.test_pipes.test_pipe_size_normalizes_values()** -> `None`
  - calls: PipeSize
- **tests.domain.test_pipes.test_pipe_size_internal_area()** -> `None`
  - calls: PipeSize, isclose
- **tests.domain.test_pipes.test_pipe_size_with_zero_internal_diameter_is_not_usable()** -> `None`
  - calls: PipeSize

## C:\dev\PythonProject_v4\tests\domain\test_singular_losses.py

- **tests.domain.test_singular_losses.test_singular_loss_normalizes_values()** -> `None`
  - calls: SingularLoss
- **tests.domain.test_singular_losses.test_singular_loss_negative_values_are_clamped()** -> `None`
  - calls: SingularLoss
- **tests.domain.test_singular_losses.test_singular_loss_method_helpers()** -> `None`
  - calls: SingularLoss