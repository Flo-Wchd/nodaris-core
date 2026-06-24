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
  - doc: Total pressure loss stored or computed from available components.
- **ndc_core.domain.networks.section.Section.total_pressure_loss_pa(self, value)** -> `None`
  - calls: float
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

## C:\dev\PythonProject_v4\ndc_core\hydraulics\conversions.py

- **ndc_core.hydraulics.conversions.flow_l_s_to_m3_s(flow_l_s)** -> `float`
  - calls: float
  - doc: Convert a flow from L/s to m³/s.
- **ndc_core.hydraulics.conversions.flow_m3_s_to_l_s(flow_m3_s)** -> `float`
  - calls: float
  - doc: Convert a flow from m³/s to L/s.
- **ndc_core.hydraulics.conversions.diameter_mm_to_m(diameter_mm)** -> `float`
  - calls: float
  - doc: Convert a diameter from mm to m.
- **ndc_core.hydraulics.conversions.diameter_m_to_mm(diameter_m)** -> `float`
  - calls: float
  - doc: Convert a diameter from m to mm.
- **ndc_core.hydraulics.conversions.pressure_bar_to_pa(pressure_bar)** -> `float`
  - calls: float
  - doc: Convert pressure from bar to Pa.
- **ndc_core.hydraulics.conversions.pressure_pa_to_bar(pressure_pa)** -> `float`
  - calls: float
  - doc: Convert pressure from Pa to bar.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\elevation_pressure_loss.py

- **ndc_core.hydraulics.elevation_pressure_loss.elevation_pressure_change_pa(elevation_change_m, density_kg_m3, gravity_m_s2)** -> `float`
  - calls: float
  - doc: Return pressure change due to elevation.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\friction.py

- **ndc_core.hydraulics.friction.relative_roughness(roughness_m, internal_diameter_m)** -> `float`
  - calls: float
  - doc: Return relative roughness epsilon / D.
- **ndc_core.hydraulics.friction.laminar_friction_factor(reynolds)** -> `float`
  - calls: float
  - doc: Return Darcy friction factor in laminar regime.
- **ndc_core.hydraulics.friction.swamee_jain_friction_factor(reynolds, relative_roughness_value)** -> `float`
  - calls: float, log10, max
  - doc: Return explicit Swamee-Jain Darcy friction factor approximation.
- **ndc_core.hydraulics.friction.colebrook_white_friction_factor(reynolds, relative_roughness_value, max_iterations, tolerance)** -> `float`
  - calls: abs, float, int, log10, max, range, sqrt, swamee_jain_friction_factor
  - doc: Return Darcy friction factor using fixed-point Colebrook-White solving.
- **ndc_core.hydraulics.friction.darcy_friction_factor(reynolds, relative_roughness_value)** -> `float`
  - calls: colebrook_white_friction_factor, float, flow_regime, laminar_friction_factor
  - doc: Return Darcy friction factor for laminar, transition or turbulent flow.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\linear_pressure_loss.py

- **ndc_core.hydraulics.linear_pressure_loss.linear_pressure_loss_pa(friction_factor, length_m, internal_diameter_m, velocity_m_s, density_kg_m3)** -> `float`
  - calls: float
  - doc: Return Darcy-Weisbach linear pressure loss in Pa.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\pipe_sizing.py

- **ndc_core.hydraulics.pipe_sizing.select_smallest_usable_pipe_size(pipe_sizes, minimum_internal_diameter_mm)** -> `PipeSize | None`
  - calls: float, max, sorted
  - doc: Return the smallest pipe size matching a minimum internal diameter.
- **ndc_core.hydraulics.pipe_sizing.select_pipe_size_by_velocity(design_flow_l_s, pipe_sizes, max_velocity_m_s, min_internal_diameter_mm)** -> `PipeSizingResult`
  - calls: PipeSizingResult, float, max, select_smallest_usable_pipe_size, theoretical_diameter_mm_for_velocity, velocity_from_l_s_and_mm
  - doc: Select the smallest pipe size respecting theoretical diameter by velocity.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\reynolds.py

- **ndc_core.hydraulics.reynolds.reynolds_number(velocity_m_s, internal_diameter_m, kinematic_viscosity_m2_s, density_kg_m3, dynamic_viscosity_pa_s)** -> `float`
  - calls: float
  - doc: Return Reynolds number for internal pipe flow.
- **ndc_core.hydraulics.reynolds.flow_regime(reynolds, laminar_limit, turbulent_limit)** -> `FlowRegime`
  - calls: float
  - doc: Return qualitative flow regime.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\singular_pressure_loss.py

- **ndc_core.hydraulics.singular_pressure_loss.sum_zeta(values)** -> `float`
  - calls: float
  - doc: Return positive zeta coefficients sum.
- **ndc_core.hydraulics.singular_pressure_loss.singular_pressure_loss_pa(zeta_total, velocity_m_s, density_kg_m3)** -> `float`
  - calls: float
  - doc: Return singular pressure loss in Pa.
- **ndc_core.hydraulics.singular_pressure_loss.equivalent_zeta_from_kv(flow_l_s, kv_m3_h, velocity_m_s, density_kg_m3)** -> `float`
  - calls: float
  - doc: Convert a Kv value to an equivalent zeta coefficient.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\total_pressure_loss.py

- **ndc_core.hydraulics.total_pressure_loss.total_pressure_loss(velocity_m_s, internal_diameter_m, length_m, density_kg_m3, kinematic_viscosity_m2_s, relative_roughness_value, elevation_change_m, singular_zeta_values)** -> `PressureLossBreakdown`
  - calls: PressureLossBreakdown, darcy_friction_factor, elevation_pressure_change_pa, flow_regime, linear_pressure_loss_pa, reynolds_number, singular_pressure_loss_pa, sum_zeta
  - doc: Return complete pressure loss breakdown for one section.

## C:\dev\PythonProject_v4\ndc_core\hydraulics\types.py

- **ndc_core.hydraulics.types.PressureLossBreakdown.total_pressure_change_pa(self)** -> `float`
- **ndc_core.hydraulics.types.PipeSizingResult.found(self)** -> `bool`
- **ndc_core.hydraulics.types.PipeSizingResult.velocity_ok(self)** -> `bool | None`

## C:\dev\PythonProject_v4\ndc_core\hydraulics\velocity.py

- **ndc_core.hydraulics.velocity.circular_area_m2(diameter_m)** -> `float`
  - calls: float
  - doc: Return the internal area of a circular pipe.
- **ndc_core.hydraulics.velocity.velocity_m_s(flow_m3_s, internal_diameter_m)** -> `float`
  - calls: circular_area_m2, float
  - doc: Return mean velocity from flow and internal diameter in SI units.
- **ndc_core.hydraulics.velocity.velocity_from_l_s_and_mm(flow_l_s, internal_diameter_mm)** -> `float`
  - calls: diameter_mm_to_m, flow_l_s_to_m3_s, velocity_m_s
  - doc: Return mean velocity from flow in L/s and internal diameter in mm.
- **ndc_core.hydraulics.velocity.theoretical_diameter_m_for_velocity(flow_m3_s, target_velocity_m_s)** -> `float`
  - calls: float, sqrt
  - doc: Return theoretical internal diameter for a target velocity.
- **ndc_core.hydraulics.velocity.theoretical_diameter_mm_for_velocity(flow_l_s, target_velocity_m_s)** -> `float`
  - calls: flow_l_s_to_m3_s, theoretical_diameter_m_for_velocity
  - doc: Return theoretical internal diameter in mm from flow in L/s.

## C:\dev\PythonProject_v4\ndc_core\networks\cold_water\engine.py

- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.from_network(cls, network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog)** -> `ColdWaterNetworkEngine`
  - calls: cls
  - doc: Build an EFS facade from the domain Network object.
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.side(self)** -> `DomesticWaterSide`
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.domestic_engine(self)** -> `DomesticWaterNetworkEngine`
  - calls: DomesticWaterNetworkEngine.cold_water, DomesticWaterNetworkEngine.cold_water_from_network
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.pressure_network_engine(self)** -> `DomesticWaterPressureNetworkEngine`
  - calls: DomesticWaterPressureNetworkEngine
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.compute_sections(self, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: self.domestic_engine, self.domestic_engine().compute_sections
  - doc: Compute EFS section sizing and pressure losses.
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.compute_all(self, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: self.domestic_engine, self.domestic_engine().compute_all
  - doc: Compute full EFS network.
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.propagate_pressures(self, source_node_id, source_pressure_pa)** -> `Result[DomesticWaterPressurePropagationResult]`
  - calls: self.pressure_network_engine, self.pressure_network_engine().propagate_pressures
  - doc: Propagate EFS pressures using already computed section pressure losses.
- **ndc_core.networks.cold_water.engine.ColdWaterNetworkEngine.summarize_worst_terminal_pressure(self, source_node_id, source_pressure_bar, min_required_pressure_bar)** -> `Result[DomesticWaterPressureSummary]`
  - calls: self.pressure_network_engine, self.pressure_network_engine().summarize_worst_terminal_pressure
  - doc: Compute EFS worst terminal pressure summary from existing pressure losses.
- **ndc_core.networks.cold_water.engine.compute_cold_water_network(nodes, sections, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: ColdWaterNetworkEngine, ColdWaterNetworkEngine(nodes=nodes, sections=sections, appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog, fluid_catalog=fluid_catalog, singular_loss_catalog=singular_loss_catalog).compute_all
  - doc: Functional EFS entry point.
- **ndc_core.networks.cold_water.engine.compute_cold_water_network_from_network(network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: compute_cold_water_network_from_domain
  - doc: Functional EFS entry point from the domain Network aggregate.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\appliance_counts.py

- **ndc_core.networks.domestic_water.appliance_counts.normalize_appliance_counts(raw_counts)** -> `dict[str, int]`
  - calls: int, isinstance, normalized.get, raw_counts.items, str, str(raw_code or '').strip
  - doc: Normalize an appliance count mapping.
- **ndc_core.networks.domestic_water.appliance_counts.merge_appliance_counts(*count_maps)** -> `dict[str, int]`
  - calls: merged.get, normalize_appliance_counts, normalized.items
  - doc: Merge several appliance count mappings using the shared normalization rules.
- **ndc_core.networks.domestic_water.appliance_counts.apply_machine_exclusivity(counts, exclusive_codes)** -> `dict[str, int]`
  - calls: code.strip, code.strip().upper, next, normalize_appliance_counts, normalized_counts.items, str, str(code or '').strip, str(code or '').strip().upper, sum
  - doc: Apply the domestic water washing-machine exclusivity rule.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\appliance_propagation.py

- **ndc_core.networks.domestic_water.appliance_propagation.DomesticWaterAppliancePropagationResult.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.appliance_propagation.DomesticWaterAppliancePropagationResult.has_errors(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.appliance_propagation.DomesticWaterAppliancePropagationResult.propagated_section_count(self)** -> `int`
  - calls: len
- **ndc_core.networks.domestic_water.appliance_propagation.DomesticWaterAppliancePropagationEngine.propagate(self)** -> `Result[DomesticWaterAppliancePropagationResult]`
  - calls: DomesticWaterAppliancePropagationResult, EngineMessage.warning, Result.success, any, bool, children_by_node[upstream_node_id].append, clean_entity_id, defaultdict, getattr, messages.append, node_local_counts.values, read_node_local_appliance_counts, section_matches_domestic_water_side, self.nodes.items, self.sections.items ...
- **ndc_core.networks.domestic_water.appliance_propagation.DomesticWaterAppliancePropagationEngine.compute_node_downstream_counts(node_id)** -> `dict[str, int]`
  - calls: EngineMessage.error, children_by_node.get, compute_node_downstream_counts, cycle_reported.add, dict, merge_appliance_counts, messages.append, node_local_counts.get, self.nodes.get, self.sections.get, visiting.add, visiting.remove, write_node_downstream_appliance_counts, write_section_downstream_appliance_counts
- **ndc_core.networks.domestic_water.appliance_propagation.propagate_domestic_water_appliances(nodes, sections, side)** -> `Result[DomesticWaterAppliancePropagationResult]`
  - calls: DomesticWaterAppliancePropagationEngine, DomesticWaterAppliancePropagationEngine(nodes=nodes, sections=sections, side=side).propagate
  - doc: Convenience function for Cell/Node -> Section appliance propagation.
- **ndc_core.networks.domestic_water.appliance_propagation.propagate_cold_water_appliances(nodes, sections)** -> `Result[DomesticWaterAppliancePropagationResult]`
  - calls: propagate_domestic_water_appliances
  - doc: Convenience function for EFS appliance propagation.
- **ndc_core.networks.domestic_water.appliance_propagation.propagate_hot_water_appliances(nodes, sections)** -> `Result[DomesticWaterAppliancePropagationResult]`
  - calls: propagate_domestic_water_appliances
  - doc: Convenience function for ECS appliance propagation.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\appliance_rules.py

- **ndc_core.networks.domestic_water.appliance_rules.appliance_flow_for_profile(appliance, profile)** -> `float`
  - calls: float, getattr, max
  - doc: Return the appliance unit design flow for the requested domestic water profile.
- **ndc_core.networks.domestic_water.appliance_rules.minimum_appliance_internal_diameter_mm(appliance_catalog, appliance_counts, profile)** -> `float`
  - calls: _optional_positive_float, appliance_catalog.get, appliance_counts.items, appliance_flow_for_profile
  - doc: Return the maximum appliance minimum internal diameter required by a profile.
- **ndc_core.networks.domestic_water.appliance_rules._optional_positive_float(value)** -> `float | None`
  - calls: float

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\demand.py

- **ndc_core.networks.domestic_water.demand.DomesticWaterDemandBuilder.cold_water(cls, appliance_catalog)** -> `DomesticWaterDemandBuilder`
  - calls: cls
- **ndc_core.networks.domestic_water.demand.DomesticWaterDemandBuilder.hot_water(cls, appliance_catalog)** -> `DomesticWaterDemandBuilder`
  - calls: cls
- **ndc_core.networks.domestic_water.demand.DomesticWaterDemandBuilder.compute_from_counts(self, appliance_counts)** -> `Result[DomesticWaterDemand]`
  - calls: ApplianceDemandItem, DomesticWaterDemand, EngineMessage.info, EngineMessage.warning, Result.success, appliance_flow_for_profile, apply_machine_exclusivity, declared_counts.get, declared_counts.values, effective_counts.values, items.append, messages.append, normalize_appliance_counts, self._simultaneity_factor, self.appliance_catalog.get ...
- **ndc_core.networks.domestic_water.demand.DomesticWaterDemandBuilder._simultaneity_factor(self, effective_appliance_count)** -> `float`
  - calls: clamp_simultaneity_factor, collective_dtu_simultaneity_factor
- **ndc_core.networks.domestic_water.demand.compute_cold_water_demand(appliance_catalog, appliance_counts)** -> `Result[DomesticWaterDemand]`
  - calls: DomesticWaterDemandBuilder.cold_water, DomesticWaterDemandBuilder.cold_water(appliance_catalog).compute_from_counts
  - doc: Convenience function for EFS demand.
- **ndc_core.networks.domestic_water.demand.compute_hot_water_demand(appliance_catalog, appliance_counts)** -> `Result[DomesticWaterDemand]`
  - calls: DomesticWaterDemandBuilder.hot_water, DomesticWaterDemandBuilder.hot_water(appliance_catalog).compute_from_counts
  - doc: Convenience function for ECS forward demand.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\entity_access.py

- **ndc_core.networks.domestic_water.entity_access.SectionPressureLossRead.ok(self)** -> `bool`
- **ndc_core.networks.domestic_water.entity_access.clean_entity_id(value)** -> `str`
  - calls: str, str(value or '').strip
  - doc: Return a normalized non-optional entity id string.
- **ndc_core.networks.domestic_water.entity_access.clean_optional_code(value)** -> `str | None`
  - calls: clean_entity_id
  - doc: Return a normalized optional code, or None when empty.
- **ndc_core.networks.domestic_water.entity_access.read_downstream_section_ids(node)** -> `tuple[str, ...]`
  - calls: clean_entity_id, getattr, ids.append, tuple
  - doc: Read downstream section ids from a Node-like object.
- **ndc_core.networks.domestic_water.entity_access.read_cell_appliance_counts(cell)** -> `dict[str, int]`
  - calls: getattr, isinstance, merge_appliance_counts, normalize_appliance_counts
  - doc: Read normalized appliance counts from a Cell-like object.
- **ndc_core.networks.domestic_water.entity_access.read_node_local_appliance_counts(node)** -> `dict[str, int]`
  - calls: callable, getattr, isinstance, local_counts_method, merge_appliance_counts, normalize_appliance_counts, read_cell_appliance_counts
  - doc: Read normalized local appliance counts from a Node-like object.
- **ndc_core.networks.domestic_water.entity_access.read_section_downstream_appliance_counts(section)** -> `dict[str, int]`
  - calls: getattr, normalize_appliance_counts
  - doc: Read normalized downstream appliance counts from a Section-like object.
- **ndc_core.networks.domestic_water.entity_access.read_section_pressure_loss_pa(section)** -> `SectionPressureLossRead`
  - calls: SectionPressureLossRead, float, getattr, isfinite
  - doc: Read a safe total pressure loss from a Section-like object.
- **ndc_core.networks.domestic_water.entity_access.write_section_downstream_appliance_counts(section, counts)** -> `None`
  - calls: _write_mapping_attribute, normalize_appliance_counts
  - doc: Write normalized downstream appliance counts on a Section-like object.
- **ndc_core.networks.domestic_water.entity_access.write_node_downstream_appliance_counts(node, counts)** -> `None`
  - calls: _write_mapping_attribute, normalize_appliance_counts
  - doc: Write normalized downstream appliance counts on a Node-like object.
- **ndc_core.networks.domestic_water.entity_access.apply_section_pressures(section, pressure_start_pa, pressure_end_pa)** -> `None`
  - doc: Write computed start/end pressures on a Section-like object.
- **ndc_core.networks.domestic_water.entity_access.apply_node_pressures(nodes, node_states)** -> `None`
  - calls: getattr, node_states.items, nodes.get
  - doc: Write computed pressures on Node-like objects.
- **ndc_core.networks.domestic_water.entity_access._write_mapping_attribute(entity, attribute_name, values)** -> `None`
  - calls: dict, getattr, isinstance, setattr, target.clear, target.update

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\fluid_rules.py

- **ndc_core.networks.domestic_water.fluid_rules.default_domestic_water_fluid_code(side)** -> `str`
  - doc: Return the default fluid catalog code for a domestic water side.
- **ndc_core.networks.domestic_water.fluid_rules.resolve_domestic_water_fluid(fluid_catalog, side, water_temperature_c, messages)** -> `Fluid | None`
  - calls: EngineMessage.error, _temperature_is_inside_catalog_range, default_domestic_water_fluid_code, fluid_catalog.get, fluid_catalog.get_water_at_temperature, messages.append
  - doc: Resolve water properties for a domestic water pressure-loss calculation.
- **ndc_core.networks.domestic_water.fluid_rules._temperature_is_inside_catalog_range(fluid_catalog, temperature_c)** -> `bool`
  - calls: sorted, tuple

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\message_binding.py

- **ndc_core.networks.domestic_water.message_binding.DomesticWaterMessageBindingResult.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.message_binding.DomesticWaterMessageBindingResult.has_errors(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.message_binding.DomesticWaterMessageBinder.bind(self)** -> `Result[DomesticWaterMessageBindingResult]`
  - calls: DomesticWaterMessageBindingResult, Result.failure, Result.partial, Result.success, _dedupe_messages, _safe_set_messages, getattr, len, section_messages.items, self._collect_section_messages, self.sections.get, tuple
- **ndc_core.networks.domestic_water.message_binding.DomesticWaterMessageBinder._collect_section_messages(self)** -> `dict[str, tuple[EngineMessage, ...]]`
  - calls: _dedupe_messages, _message_section_id, getattr, section_messages.items, section_messages.setdefault, section_messages.setdefault(section_id, []).append, section_messages.setdefault(str(section_id), []).extend, section_results.items, str, tuple
- **ndc_core.networks.domestic_water.message_binding.bind_domestic_water_messages_to_entities(side, sections, compute_result, network)** -> `Result[DomesticWaterMessageBindingResult]`
  - calls: DomesticWaterMessageBinder, DomesticWaterMessageBinder(side=side, sections=sections, compute_result=compute_result, network=network).bind
  - doc: Convenience function for binding domestic water compute messages.
- **ndc_core.networks.domestic_water.message_binding._safe_set_messages(entity, primary_attr, secondary_attr, messages, warning_context, binding_messages)** -> `None`
  - calls: EngineMessage.warning, binding_messages.append, setattr, tuple
- **ndc_core.networks.domestic_water.message_binding._message_section_id(message)** -> `str | None`
  - calls: context.get, getattr, isinstance, str, str(value or '').strip
- **ndc_core.networks.domestic_water.message_binding._dedupe_messages(messages)** -> `tuple[EngineMessage, ...]`
  - calls: _message_fingerprint, deduped.append, seen.add, set, tuple
- **ndc_core.networks.domestic_water.message_binding._message_fingerprint(message)** -> `tuple[str, str, str, str]`
  - calls: getattr, repr, str

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\network_compute_result.py

- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterSectionComputeResult.sizing_ok(self)** -> `bool`
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterSectionComputeResult.pressure_loss_ok(self)** -> `bool`
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterSectionComputeResult.has_pressure_loss(self)** -> `bool`
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterSectionComputeResult.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterSectionComputeResult.has_errors(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.section_count(self)** -> `int`
  - calls: len
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.sized_section_count(self)** -> `int`
  - calls: self.section_results.values, sum
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.pressure_loss_section_count(self)** -> `int`
  - calls: self.section_results.values, sum
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.has_pressure_propagation(self)** -> `bool`
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.has_pressure_summary(self)** -> `bool`
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.network_compute_result.DomesticWaterNetworkComputeResult.has_errors(self)** -> `bool`
  - calls: any

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\network_engine.py

- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.cold_water(cls, nodes, sections, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, network)** -> `DomesticWaterNetworkEngine`
  - calls: cls
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.hot_water(cls, nodes, sections, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, network)** -> `DomesticWaterNetworkEngine`
  - calls: cls
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.from_network(cls, network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, side)** -> `DomesticWaterNetworkEngine`
  - calls: cls
  - doc: Build a domestic water engine from the domain Network object.
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.cold_water_from_network(cls, network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog)** -> `DomesticWaterNetworkEngine`
  - calls: cls.from_network
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.hot_water_from_network(cls, network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog)** -> `DomesticWaterNetworkEngine`
  - calls: cls.from_network
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.compute_sections(self, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: DomesticWaterNetworkComputeResult, Result.failure, Result.partial, Result.success, any, messages.extend, propagate_domestic_water_appliances, section_matches_domestic_water_side, self._bind_messages_to_entities, self._compute_one_section, self._validate_topology, self.sections.items, str, tuple
  - doc: Compute sizing and pressure losses for all sections matching the engine side.
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine.compute_all(self, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: DomesticWaterNetworkComputeResult, DomesticWaterPressureNetworkEngine, Result.failure, Result.partial, Result.success, messages.extend, pressure_bar_to_pa, pressure_engine.propagate_pressures, pressure_engine.summarize_worst_terminal_pressure, self._bind_messages_to_entities, self.compute_sections, tuple
  - doc: Compute sections, then optionally propagate pressure and summarize terminals.
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine._validate_topology(self)** -> `tuple[EngineMessage, ...]`
  - calls: EngineMessage, context.setdefault, dict, messages.append, self.network.validate_topology, tuple
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine._bind_messages_to_entities(self, result)** -> `None`
  - calls: bind_domestic_water_messages_to_entities
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine._compute_one_section(self, section_id, section, max_velocity_m_s, water_temperature_c)** -> `DomesticWaterSectionComputeResult`
  - calls: DomesticWaterSectionComputeResult, EngineMessage.warning, getattr, messages.append, messages.extend, read_section_downstream_appliance_counts, self._compute_section_pressure_loss, self._size_section, tuple
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine._size_section(self, section, appliance_counts, max_velocity_m_s)** -> `Result[DomesticWaterSectionSizing]`
  - calls: size_cold_water_section_from_counts, size_hot_water_section_from_counts
- **ndc_core.networks.domestic_water.network_engine.DomesticWaterNetworkEngine._compute_section_pressure_loss(self, section, water_temperature_c)** -> `Result[DomesticWaterPressureLossResult]`
  - calls: compute_cold_water_section_pressure_loss, compute_hot_water_section_pressure_loss
- **ndc_core.networks.domestic_water.network_engine.compute_cold_water_network(nodes, sections, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: DomesticWaterNetworkEngine.cold_water, DomesticWaterNetworkEngine.cold_water(nodes=nodes, sections=sections, appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog, fluid_catalog=fluid_catalog, singular_loss_catalog=singular_loss_catalog).compute_all
  - doc: Convenience function for full EFS network computation.
- **ndc_core.networks.domestic_water.network_engine.compute_hot_water_network(nodes, sections, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: DomesticWaterNetworkEngine.hot_water, DomesticWaterNetworkEngine.hot_water(nodes=nodes, sections=sections, appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog, fluid_catalog=fluid_catalog, singular_loss_catalog=singular_loss_catalog).compute_all
  - doc: Convenience function for full ECS forward network computation.
- **ndc_core.networks.domestic_water.network_engine.compute_cold_water_network_from_domain(network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: DomesticWaterNetworkEngine.cold_water_from_network, DomesticWaterNetworkEngine.cold_water_from_network(network=network, appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog, fluid_catalog=fluid_catalog, singular_loss_catalog=singular_loss_catalog).compute_all
  - doc: Convenience function for full EFS computation from a domain Network.
- **ndc_core.networks.domestic_water.network_engine.compute_hot_water_network_from_domain(network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: DomesticWaterNetworkEngine.hot_water_from_network, DomesticWaterNetworkEngine.hot_water_from_network(network=network, appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog, fluid_catalog=fluid_catalog, singular_loss_catalog=singular_loss_catalog).compute_all
  - doc: Convenience function for full ECS forward computation from a domain Network.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\numeric.py

- **ndc_core.networks.domestic_water.numeric.safe_float(value, default)** -> `float`
  - calls: float, isfinite
  - doc: Convert a value to float.
- **ndc_core.networks.domestic_water.numeric.safe_positive_float(value)** -> `float | None`
  - calls: safe_float
  - doc: Convert a value to a strictly positive float.
- **ndc_core.networks.domestic_water.numeric.positive_optional_float(value)** -> `float | None`
  - calls: safe_positive_float
  - doc: Alias for optional strictly positive user inputs.
- **ndc_core.networks.domestic_water.numeric.safe_non_negative_float(value, default)** -> `float`
  - calls: safe_float
  - doc: Convert a value to a non-negative float.
- **ndc_core.networks.domestic_water.numeric.safe_pressure_pa(value)** -> `float`
  - calls: safe_non_negative_float
  - doc: Convert a pressure value in Pa to a safe non-negative pressure.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\pipe_rules.py

- **ndc_core.networks.domestic_water.pipe_rules.relative_roughness_for_section(section, pipe_catalog, internal_diameter_m)** -> `float`
  - calls: clean_optional_code, getattr, pipe_catalog.get_size, pipe_catalog.materials_by_code.get, relative_roughness
  - doc: Resolve the relative roughness for a Section-like pipe.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\pressure_loss.py

- **ndc_core.networks.domestic_water.pressure_loss.DomesticWaterPressureLossEngine.compute_section_pressure_loss(self, section, water_temperature_c, singular_zeta_values)** -> `Result[DomesticWaterPressureLossResult]`
  - calls: Result.failure, build_section_pressure_loss_result, collect_section_singular_zeta_values, prepare_section_hydraulic_inputs, relative_roughness_for_section, resolve_domestic_water_fluid, total_pressure_loss, tuple
- **ndc_core.networks.domestic_water.pressure_loss.compute_cold_water_section_pressure_loss(section, fluid_catalog, pipe_catalog, singular_loss_catalog, water_temperature_c, singular_zeta_values)** -> `Result[DomesticWaterPressureLossResult]`
  - calls: DomesticWaterPressureLossEngine, DomesticWaterPressureLossEngine(fluid_catalog=fluid_catalog, pipe_catalog=pipe_catalog, singular_loss_catalog=singular_loss_catalog, side=DomesticWaterSide.COLD_WATER).compute_section_pressure_loss
  - doc: Convenience function for EFS section pressure loss.
- **ndc_core.networks.domestic_water.pressure_loss.compute_hot_water_section_pressure_loss(section, fluid_catalog, pipe_catalog, singular_loss_catalog, water_temperature_c, singular_zeta_values)** -> `Result[DomesticWaterPressureLossResult]`
  - calls: DomesticWaterPressureLossEngine, DomesticWaterPressureLossEngine(fluid_catalog=fluid_catalog, pipe_catalog=pipe_catalog, singular_loss_catalog=singular_loss_catalog, side=DomesticWaterSide.HOT_WATER).compute_section_pressure_loss
  - doc: Convenience function for ECS forward section pressure loss.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\pressure_loss_result.py

- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.reynolds(self)** -> `float | None`
- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.linear_pressure_loss_pa(self)** -> `float`
- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.singular_pressure_loss_pa(self)** -> `float`
- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.elevation_pressure_change_pa(self)** -> `float`
- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.total_pressure_change_pa(self)** -> `float`
- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.pressure_loss_result.DomesticWaterPressureLossResult.has_errors(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.pressure_loss_result.build_section_pressure_loss_result(section, side, fluid, inputs, breakdown, relative_roughness_value, messages)** -> `Result[DomesticWaterPressureLossResult]`
  - calls: DomesticWaterPressureLossResult, Result.failure, Result.success, apply_section_pressure_loss_state, tuple
  - doc: Build, write and wrap a domestic water section pressure-loss result.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\pressure_network.py

- **ndc_core.networks.domestic_water.pressure_network.DomesticWaterPressureNetworkEngine.propagate_pressures(self, source_node_id, source_pressure_pa)** -> `Result[DomesticWaterPressurePropagationResult]`
  - calls: DomesticWaterPressurePropagationResult, EngineMessage.error, EngineMessage.warning, NodePressureState, Result.failure, Result.success, apply_node_pressures, apply_section_pressures, clean_optional_code, deque, getattr, max, messages.append, node_is_terminal_for_domestic_water_side, pressure_pa_to_bar ...
- **ndc_core.networks.domestic_water.pressure_network.DomesticWaterPressureNetworkEngine.summarize_worst_terminal_pressure(self, source_node_id, source_pressure_bar, min_required_pressure_bar)** -> `Result[DomesticWaterPressureSummary]`
  - calls: DomesticWaterPressurePropagationResult, DomesticWaterPressureSummary, EngineMessage.warning, Result.failure, Result.partial, Result.success, TerminalPressureStatus, messages.append, messages.extend, min, pressure_bar_to_pa, propagation_result.value.node_pressures.items, safe_non_negative_float, self.propagate_pressures, str ...
- **ndc_core.networks.domestic_water.pressure_network.propagate_cold_water_pressures(nodes, sections, source_node_id, source_pressure_pa)** -> `Result[DomesticWaterPressurePropagationResult]`
  - calls: DomesticWaterPressureNetworkEngine, DomesticWaterPressureNetworkEngine(nodes=nodes, sections=sections, side=DomesticWaterSide.COLD_WATER).propagate_pressures
  - doc: Convenience function for EFS pressure propagation.
- **ndc_core.networks.domestic_water.pressure_network.propagate_hot_water_pressures(nodes, sections, source_node_id, source_pressure_pa)** -> `Result[DomesticWaterPressurePropagationResult]`
  - calls: DomesticWaterPressureNetworkEngine, DomesticWaterPressureNetworkEngine(nodes=nodes, sections=sections, side=DomesticWaterSide.HOT_WATER).propagate_pressures
  - doc: Convenience function for ECS forward pressure propagation.
- **ndc_core.networks.domestic_water.pressure_network.summarize_cold_water_worst_terminal_pressure(nodes, sections, source_node_id, source_pressure_bar, min_required_pressure_bar)** -> `Result[DomesticWaterPressureSummary]`
  - calls: DomesticWaterPressureNetworkEngine, DomesticWaterPressureNetworkEngine(nodes=nodes, sections=sections, side=DomesticWaterSide.COLD_WATER).summarize_worst_terminal_pressure
  - doc: Convenience function for EFS worst terminal summary.
- **ndc_core.networks.domestic_water.pressure_network.summarize_hot_water_worst_terminal_pressure(nodes, sections, source_node_id, source_pressure_bar, min_required_pressure_bar)** -> `Result[DomesticWaterPressureSummary]`
  - calls: DomesticWaterPressureNetworkEngine, DomesticWaterPressureNetworkEngine(nodes=nodes, sections=sections, side=DomesticWaterSide.HOT_WATER).summarize_worst_terminal_pressure
  - doc: Convenience function for ECS forward worst terminal summary.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\pressure_network_result.py

- **ndc_core.networks.domestic_water.pressure_network_result.DomesticWaterPressurePropagationResult.reached_node_ids(self)** -> `tuple[str, ...]`
  - calls: tuple
- **ndc_core.networks.domestic_water.pressure_network_result.DomesticWaterPressurePropagationResult.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.pressure_network_result.DomesticWaterPressurePropagationResult.has_errors(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.pressure_network_result.DomesticWaterPressureSummary.has_worst_terminal(self)** -> `bool`
- **ndc_core.networks.domestic_water.pressure_network_result.DomesticWaterPressureSummary.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.pressure_network_result.DomesticWaterPressureSummary.has_errors(self)** -> `bool`
  - calls: any

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\profiles.py

- **ndc_core.networks.domestic_water.profiles.DomesticWaterProfile.flow_attribute_name(self)** -> `str`

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\section_hydraulic_inputs.py

- **ndc_core.networks.domestic_water.section_hydraulic_inputs.prepare_section_hydraulic_inputs(section, messages)** -> `DomesticWaterSectionHydraulicInputs | None`
  - calls: DomesticWaterSectionHydraulicInputs, EngineMessage.error, EngineMessage.info, diameter_mm_to_m, max, messages.append, safe_float, safe_positive_float, velocity_from_l_s_and_mm
  - doc: Prepare safe hydraulic inputs from a Section-like object.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\section_sizing.py

- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine.cold_water(cls, appliance_catalog, pipe_catalog)** -> `DomesticWaterSectionSizingEngine`
  - calls: cls
- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine.hot_water(cls, appliance_catalog, pipe_catalog)** -> `DomesticWaterSectionSizingEngine`
  - calls: cls
- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine.size_section_from_counts(self, section, appliance_counts, max_velocity_m_s)** -> `Result[DomesticWaterSectionSizing]`
  - calls: DomesticWaterDemandBuilder, DomesticWaterDemandBuilder(appliance_catalog=self.appliance_catalog, profile=self.profile).compute_from_counts, DomesticWaterSectionSizing, EngineMessage.warning, Result.failure, Result.partial, Result.success, apply_section_sizing_state, max, messages.append, messages.extend, minimum_appliance_internal_diameter_mm, normalize_appliance_counts, self._select_or_force_diameter, tuple ...
- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine._select_or_force_diameter(self, section, demand, raw_counts, effective_counts, min_required_diameter_mm, max_velocity_m_s, messages)** -> `DomesticWaterSectionSizing`
  - calls: clean_optional_code, positive_optional_float, self._size_automatically, self._size_with_forced_internal_diameter, self._size_with_forced_pipe
- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine._size_automatically(self, section, demand, raw_counts, effective_counts, min_required_diameter_mm, max_velocity_m_s, messages)** -> `DomesticWaterSectionSizing`
  - calls: DomesticWaterSectionSizing, EngineMessage.error, list, messages.append, section.fluid_code.lower, select_pipe_size_by_velocity, self.pipe_catalog.list_sizes_for_material, self.pipe_catalog.sizes_by_code.values, tuple
- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine._size_with_forced_pipe(self, section, demand, forced_pipe_code, min_required_diameter_mm, max_velocity_m_s, messages)** -> `DomesticWaterSectionSizing`
  - calls: DomesticWaterSectionSizing, EngineMessage.error, EngineMessage.warning, messages.append, select_pipe_size_by_velocity, self.pipe_catalog.get_size, self.pipe_catalog.sizes_by_code.values, tuple, velocity_from_l_s_and_mm
- **ndc_core.networks.domestic_water.section_sizing.DomesticWaterSectionSizingEngine._size_with_forced_internal_diameter(self, section, demand, forced_diameter_mm, min_required_diameter_mm, max_velocity_m_s, messages)** -> `DomesticWaterSectionSizing`
  - calls: DomesticWaterSectionSizing, EngineMessage.warning, messages.append, select_pipe_size_by_velocity, self.pipe_catalog.sizes_by_code.values, tuple, velocity_from_l_s_and_mm
- **ndc_core.networks.domestic_water.section_sizing.size_cold_water_section_from_counts(section, appliance_counts, appliance_catalog, pipe_catalog, max_velocity_m_s)** -> `Result[DomesticWaterSectionSizing]`
  - calls: DomesticWaterSectionSizingEngine.cold_water, DomesticWaterSectionSizingEngine.cold_water(appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog).size_section_from_counts
  - doc: Convenience function for EFS section sizing.
- **ndc_core.networks.domestic_water.section_sizing.size_hot_water_section_from_counts(section, appliance_counts, appliance_catalog, pipe_catalog, max_velocity_m_s)** -> `Result[DomesticWaterSectionSizing]`
  - calls: DomesticWaterSectionSizingEngine.hot_water, DomesticWaterSectionSizingEngine.hot_water(appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog).size_section_from_counts
  - doc: Convenience function for ECS forward section sizing.
- **ndc_core.networks.domestic_water.section_sizing.velocity_limit_for_context(usage_context)** -> `float`
  - calls: isinstance, str, value.strip, value.strip().lower
  - doc: Return default velocity limit for domestic water.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\section_sizing_result.py

- **ndc_core.networks.domestic_water.section_sizing_result.DomesticWaterSectionSizing.sized(self)** -> `bool`
- **ndc_core.networks.domestic_water.section_sizing_result.DomesticWaterSectionSizing.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.section_sizing_result.DomesticWaterSectionSizing.has_errors(self)** -> `bool`
  - calls: any

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\section_state.py

- **ndc_core.networks.domestic_water.section_state.apply_section_sizing_state(section, sizing, raw_counts, effective_counts)** -> `None`
  - calls: _replace_mapping_attribute, normalize_appliance_counts
  - doc: Apply domestic water sizing outputs to a Section-like object.
- **ndc_core.networks.domestic_water.section_state.apply_section_pressure_loss_state(section, pressure_loss)** -> `None`
  - doc: Apply domestic water pressure-loss outputs to a Section-like object.
- **ndc_core.networks.domestic_water.section_state._replace_mapping_attribute(entity, attribute_name, values)** -> `None`
  - calls: dict, getattr, isinstance, setattr, target.clear, target.update

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\side_matching.py

- **ndc_core.networks.domestic_water.side_matching.normalize_domestic_water_fluid_code(value)** -> `str`
  - calls: str, str(value or '').strip, str(value or '').strip().lower, str(value or '').strip().lower().replace, str(value or '').strip().lower().replace('-', '_').replace
  - doc: Normalize a domestic water section fluid code.
- **ndc_core.networks.domestic_water.side_matching.cold_water_fluid_codes()** -> `tuple[str, ...]`
  - doc: Return canonical fluid codes accepted for EFS sections.
- **ndc_core.networks.domestic_water.side_matching.hot_water_fluid_codes()** -> `tuple[str, ...]`
  - doc: Return canonical fluid codes accepted for ECS sections.
- **ndc_core.networks.domestic_water.side_matching.domestic_water_fluid_codes_for_side(side)** -> `tuple[str, ...]`
  - calls: cold_water_fluid_codes, hot_water_fluid_codes
  - doc: Return accepted fluid codes for the requested domestic water side.
- **ndc_core.networks.domestic_water.side_matching.domestic_water_side_from_fluid_code(value)** -> `DomesticWaterSide | None`
  - calls: cold_water_fluid_codes, hot_water_fluid_codes, normalize_domestic_water_fluid_code
  - doc: Resolve a domestic water side from a fluid code.
- **ndc_core.networks.domestic_water.side_matching.section_matches_domestic_water_side(section, side)** -> `bool`
  - calls: domestic_water_fluid_codes_for_side, getattr, normalize_domestic_water_fluid_code
  - doc: Return whether a section belongs to the requested domestic water side.
- **ndc_core.networks.domestic_water.side_matching.node_is_terminal_for_domestic_water_side(node, sections, side)** -> `bool`
  - calls: read_downstream_section_ids, section_matches_domestic_water_side, sections.get
  - doc: Return whether a node is terminal for the requested domestic water side.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\simultaneity.py

- **ndc_core.networks.domestic_water.simultaneity.collective_dtu_simultaneity_factor(appliance_count, threshold)** -> `float`
  - calls: int, sqrt
  - doc: Return DTU collective simultaneity factor.
- **ndc_core.networks.domestic_water.simultaneity.clamp_simultaneity_factor(value)** -> `float`
  - calls: float, min
  - doc: Keep a simultaneity factor in a safe range.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\singular_loss_rules.py

- **ndc_core.networks.domestic_water.singular_loss_rules.collect_section_singular_zeta_values(section, singular_loss_catalog, flow_l_s, velocity_m_s, density_kg_m3, messages)** -> `tuple[float, ...]`
  - calls: tuple, zeta_from_section_singular_loss_item, zeta_values.append
  - doc: Collect positive singular zeta values declared on a section.
- **ndc_core.networks.domestic_water.singular_loss_rules.zeta_from_section_singular_loss_item(item, section, singular_loss_catalog, flow_l_s, velocity_m_s, density_kg_m3, messages)** -> `float`
  - calls: EngineMessage.warning, clean_optional_code, getattr, messages.append, safe_positive_float, singular_loss_catalog.get, zeta_from_catalog_singular_loss
  - doc: Resolve one section singular-loss item to an equivalent zeta value.
- **ndc_core.networks.domestic_water.singular_loss_rules.zeta_from_catalog_singular_loss(loss, quantity, section, flow_l_s, velocity_m_s, density_kg_m3, messages)** -> `float`
  - calls: EngineMessage.warning, equivalent_zeta_from_kv, float, max, messages.append
  - doc: Resolve one catalog singular loss to an equivalent zeta value.

## C:\dev\PythonProject_v4\ndc_core\networks\domestic_water\types.py

- **ndc_core.networks.domestic_water.types.DomesticWaterDemand.has_flow(self)** -> `bool`
- **ndc_core.networks.domestic_water.types.DomesticWaterDemand.has_warnings(self)** -> `bool`
  - calls: any
- **ndc_core.networks.domestic_water.types.DomesticWaterDemand.has_errors(self)** -> `bool`
  - calls: any

## C:\dev\PythonProject_v4\ndc_core\networks\hot_water\engine.py

- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.from_network(cls, network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog)** -> `HotWaterNetworkEngine`
  - calls: cls
  - doc: Build an ECS facade from the domain Network object.
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.side(self)** -> `DomesticWaterSide`
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.domestic_engine(self)** -> `DomesticWaterNetworkEngine`
  - calls: DomesticWaterNetworkEngine.hot_water, DomesticWaterNetworkEngine.hot_water_from_network
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.pressure_network_engine(self)** -> `DomesticWaterPressureNetworkEngine`
  - calls: DomesticWaterPressureNetworkEngine
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.compute_sections(self, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: self.domestic_engine, self.domestic_engine().compute_sections
  - doc: Compute ECS section sizing and pressure losses.
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.compute_all(self, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: self.domestic_engine, self.domestic_engine().compute_all
  - doc: Compute full ECS forward network.
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.propagate_pressures(self, source_node_id, source_pressure_pa)** -> `Result[DomesticWaterPressurePropagationResult]`
  - calls: self.pressure_network_engine, self.pressure_network_engine().propagate_pressures
  - doc: Propagate ECS pressures using already computed section pressure losses.
- **ndc_core.networks.hot_water.engine.HotWaterNetworkEngine.summarize_worst_terminal_pressure(self, source_node_id, source_pressure_bar, min_required_pressure_bar)** -> `Result[DomesticWaterPressureSummary]`
  - calls: self.pressure_network_engine, self.pressure_network_engine().summarize_worst_terminal_pressure
  - doc: Compute ECS worst terminal pressure summary from existing pressure losses.
- **ndc_core.networks.hot_water.engine.compute_hot_water_network(nodes, sections, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: HotWaterNetworkEngine, HotWaterNetworkEngine(nodes=nodes, sections=sections, appliance_catalog=appliance_catalog, pipe_catalog=pipe_catalog, fluid_catalog=fluid_catalog, singular_loss_catalog=singular_loss_catalog).compute_all
  - doc: Functional ECS forward entry point.
- **ndc_core.networks.hot_water.engine.compute_hot_water_network_from_network(network, appliance_catalog, pipe_catalog, fluid_catalog, singular_loss_catalog, source_node_id, source_pressure_bar, min_required_pressure_bar, max_velocity_m_s, water_temperature_c)** -> `Result[DomesticWaterNetworkComputeResult]`
  - calls: compute_hot_water_network_from_domain
  - doc: Functional ECS forward entry point from the domain Network aggregate.

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

## C:\dev\PythonProject_v4\tests\hydraulics\test_conversions.py

- **tests.hydraulics.test_conversions.test_flow_conversions()** -> `None`
  - calls: flow_l_s_to_m3_s, flow_m3_s_to_l_s
- **tests.hydraulics.test_conversions.test_diameter_conversions()** -> `None`
  - calls: diameter_m_to_mm, diameter_mm_to_m
- **tests.hydraulics.test_conversions.test_pressure_conversions()** -> `None`
  - calls: pressure_bar_to_pa, pressure_pa_to_bar

## C:\dev\PythonProject_v4\tests\hydraulics\test_friction.py

- **tests.hydraulics.test_friction.test_relative_roughness()** -> `None`
  - calls: isclose, relative_roughness
- **tests.hydraulics.test_friction.test_laminar_friction_factor()** -> `None`
  - calls: laminar_friction_factor
- **tests.hydraulics.test_friction.test_darcy_friction_factor_turbulent_returns_positive_value()** -> `None`
  - calls: darcy_friction_factor, isclose

## C:\dev\PythonProject_v4\tests\hydraulics\test_pipe_sizing.py

- **tests.hydraulics.test_pipe_sizing.test_select_smallest_usable_pipe_size()** -> `None`
  - calls: PipeSize, select_smallest_usable_pipe_size
- **tests.hydraulics.test_pipe_sizing.test_select_pipe_size_by_velocity()** -> `None`
  - calls: PipeSize, select_pipe_size_by_velocity
- **tests.hydraulics.test_pipe_sizing.test_select_pipe_size_by_velocity_returns_largest_if_all_too_small()** -> `None`
  - calls: PipeSize, select_pipe_size_by_velocity

## C:\dev\PythonProject_v4\tests\hydraulics\test_pressure_losses.py

- **tests.hydraulics.test_pressure_losses.test_linear_pressure_loss_pa()** -> `None`
  - calls: linear_pressure_loss_pa
- **tests.hydraulics.test_pressure_losses.test_sum_zeta_ignores_invalid_values()** -> `None`
  - calls: sum_zeta
- **tests.hydraulics.test_pressure_losses.test_singular_pressure_loss_pa()** -> `None`
  - calls: singular_pressure_loss_pa
- **tests.hydraulics.test_pressure_losses.test_equivalent_zeta_from_kv()** -> `None`
  - calls: equivalent_zeta_from_kv
- **tests.hydraulics.test_pressure_losses.test_elevation_pressure_change_positive_when_downstream_is_higher()** -> `None`
  - calls: elevation_pressure_change_pa, isclose
- **tests.hydraulics.test_pressure_losses.test_elevation_pressure_change_negative_when_downstream_is_lower()** -> `None`
  - calls: elevation_pressure_change_pa, isclose

## C:\dev\PythonProject_v4\tests\hydraulics\test_reynolds.py

- **tests.hydraulics.test_reynolds.test_reynolds_number_with_kinematic_viscosity()** -> `None`
  - calls: reynolds_number
- **tests.hydraulics.test_reynolds.test_reynolds_number_with_dynamic_viscosity()** -> `None`
  - calls: reynolds_number
- **tests.hydraulics.test_reynolds.test_flow_regime()** -> `None`
  - calls: flow_regime

## C:\dev\PythonProject_v4\tests\hydraulics\test_total_pressure_loss.py

- **tests.hydraulics.test_total_pressure_loss.test_total_pressure_loss_breakdown()** -> `None`
  - calls: total_pressure_loss
- **tests.hydraulics.test_total_pressure_loss.test_total_pressure_loss_keeps_elevation_when_no_flow()** -> `None`
  - calls: total_pressure_loss

## C:\dev\PythonProject_v4\tests\hydraulics\test_velocity.py

- **tests.hydraulics.test_velocity.test_circular_area_m2()** -> `None`
  - calls: circular_area_m2, isclose
- **tests.hydraulics.test_velocity.test_velocity_from_l_s_and_mm()** -> `None`
  - calls: isclose, velocity_from_l_s_and_mm
- **tests.hydraulics.test_velocity.test_theoretical_diameter_mm_for_velocity()** -> `None`
  - calls: theoretical_diameter_mm_for_velocity

## C:\dev\PythonProject_v4\tests\integration\test_domestic_water_mixed_network.py

- **tests.integration.test_domestic_water_mixed_network._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.integration.test_domestic_water_mixed_network._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.integration.test_domestic_water_mixed_network._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.integration.test_domestic_water_mixed_network._mixed_network()** -> `Network`
  - calls: Cell, Network, Node, Section, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node
  - doc: Mixed domestic water network.
- **tests.integration.test_domestic_water_mixed_network.test_cold_water_engine_from_mixed_network_only_computes_cold_sections()** -> `None`
  - calls: ColdWaterNetworkEngine.from_network, _appliance_catalog, _fluid_catalog, _mixed_network, _pipe_catalog, engine.compute_all, network.get_section, set
- **tests.integration.test_domestic_water_mixed_network.test_hot_water_engine_from_mixed_network_only_computes_hot_sections()** -> `None`
  - calls: HotWaterNetworkEngine.from_network, _appliance_catalog, _fluid_catalog, _mixed_network, _pipe_catalog, engine.compute_all, network.get_section, set
- **tests.integration.test_domestic_water_mixed_network.test_functional_entry_points_from_mixed_network_keep_side_isolation()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _mixed_network, _pipe_catalog, cold_network.get_section, compute_cold_water_network_from_network, compute_hot_water_network_from_network, hot_network.get_section, set
- **tests.integration.test_domestic_water_mixed_network.test_running_cold_then_hot_on_same_mixed_network_computes_both_without_cross_sizing()** -> `None`
  - calls: ColdWaterNetworkEngine.from_network, ColdWaterNetworkEngine.from_network(network=network, appliance_catalog=_appliance_catalog(), pipe_catalog=_pipe_catalog(), fluid_catalog=_fluid_catalog()).compute_all, HotWaterNetworkEngine.from_network, HotWaterNetworkEngine.from_network(network=network, appliance_catalog=_appliance_catalog(), pipe_catalog=_pipe_catalog(), fluid_catalog=_fluid_catalog()).compute_all, _appliance_catalog, _fluid_catalog, _mixed_network, _pipe_catalog, network.get_section, set

## C:\dev\PythonProject_v4\tests\networks\cold_water\test_engine.py

- **tests.networks.cold_water.test_engine._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.cold_water.test_engine._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.cold_water.test_engine._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.cold_water.test_engine._network()** -> `tuple[dict[str, _Node], dict[str, Section]]`
  - calls: Section, _Node, section.downstream_appliance_counts.update
- **tests.networks.cold_water.test_engine.test_cold_water_facade_exposes_cold_water_side()** -> `None`
  - calls: ColdWaterNetworkEngine, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.domestic_engine
- **tests.networks.cold_water.test_engine.test_cold_water_facade_compute_sections()** -> `None`
  - calls: ColdWaterNetworkEngine, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.compute_sections
- **tests.networks.cold_water.test_engine.test_compute_cold_water_network_functional_entry_point()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, compute_cold_water_network

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_appliance_counts.py

- **tests.networks.domestic_water.test_appliance_counts.test_normalize_appliance_counts_ignores_invalid_values()** -> `None`
  - calls: normalize_appliance_counts
- **tests.networks.domestic_water.test_appliance_counts.test_normalize_appliance_counts_merges_duplicate_codes()** -> `None`
  - calls: normalize_appliance_counts
- **tests.networks.domestic_water.test_appliance_counts.test_normalize_appliance_counts_accepts_non_mapping_input()** -> `None`
  - calls: normalize_appliance_counts
- **tests.networks.domestic_water.test_appliance_counts.test_merge_appliance_counts()** -> `None`
  - calls: merge_appliance_counts
- **tests.networks.domestic_water.test_appliance_counts.test_apply_machine_exclusivity_counts_ll_lv_as_one()** -> `None`
  - calls: apply_machine_exclusivity
- **tests.networks.domestic_water.test_appliance_counts.test_apply_machine_exclusivity_keeps_single_machine()** -> `None`
  - calls: apply_machine_exclusivity
- **tests.networks.domestic_water.test_appliance_counts.test_apply_machine_exclusivity_is_case_insensitive()** -> `None`
  - calls: apply_machine_exclusivity

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_appliance_propagation.py

- **tests.networks.domestic_water.test_appliance_propagation._node(node_id, kind)** -> `Node`
  - calls: Node
- **tests.networks.domestic_water.test_appliance_propagation._section(section_id, upstream_node_id, downstream_node_id, fluid_code)** -> `Section`
  - calls: Section
- **tests.networks.domestic_water.test_appliance_propagation.test_propagates_terminal_cell_appliances_to_upstream_sections()** -> `None`
  - calls: Cell, Network, _node, _section, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node, network.get_section, propagate_cold_water_appliances
- **tests.networks.domestic_water.test_appliance_propagation.test_propagates_branch_appliances_independently()** -> `None`
  - calls: Cell, Network, _node, _section, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node, network.get_section, propagate_cold_water_appliances
- **tests.networks.domestic_water.test_appliance_propagation.test_no_local_appliances_preserves_manual_section_counts()** -> `None`
  - calls: Network, _node, _section, network.add_node, network.add_section, propagate_cold_water_appliances, section.downstream_appliance_counts.update
- **tests.networks.domestic_water.test_appliance_propagation.test_hot_water_propagation_ignores_cold_water_sections()** -> `None`
  - calls: Cell, Network, _node, _section, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node, propagate_hot_water_appliances
- **tests.networks.domestic_water.test_appliance_propagation.test_cycle_is_reported_without_exception()** -> `None`
  - calls: Cell, Network, _node, _section, any, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node, propagate_cold_water_appliances

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_appliance_rules.py

- **tests.networks.domestic_water.test_appliance_rules._catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.domestic_water.test_appliance_rules.test_appliance_flow_for_profile()** -> `None`
  - calls: Appliance, appliance_flow_for_profile
- **tests.networks.domestic_water.test_appliance_rules.test_appliance_flow_for_profile_clamps_negative_value()** -> `None`
  - calls: Appliance, appliance_flow_for_profile
- **tests.networks.domestic_water.test_appliance_rules.test_minimum_appliance_internal_diameter_mm_uses_only_profile_flow()** -> `None`
  - calls: _catalog, minimum_appliance_internal_diameter_mm
- **tests.networks.domestic_water.test_appliance_rules.test_minimum_appliance_internal_diameter_mm_ignores_cold_only_for_hot_water()** -> `None`
  - calls: _catalog, minimum_appliance_internal_diameter_mm
- **tests.networks.domestic_water.test_appliance_rules.test_minimum_appliance_internal_diameter_mm_ignores_unknown_and_zero_counts()** -> `None`
  - calls: _catalog, minimum_appliance_internal_diameter_mm

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_demand.py

- **tests.networks.domestic_water.test_demand._catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.domestic_water.test_demand.test_compute_cold_water_demand_raw_below_threshold()** -> `None`
  - calls: _catalog, compute_cold_water_demand
- **tests.networks.domestic_water.test_demand.test_compute_cold_water_demand_with_collective_simultaneity()** -> `None`
  - calls: _catalog, compute_cold_water_demand, isclose, sqrt
- **tests.networks.domestic_water.test_demand.test_compute_hot_water_demand_ignores_cold_only_appliances()** -> `None`
  - calls: _catalog, any, compute_hot_water_demand
- **tests.networks.domestic_water.test_demand.test_unknown_appliance_creates_warning_without_failure()** -> `None`
  - calls: _catalog, any, compute_cold_water_demand
- **tests.networks.domestic_water.test_demand.test_machine_exclusivity_counts_ll_lv_as_one_effective_machine()** -> `None`
  - calls: _catalog, any, compute_cold_water_demand, isclose, len
- **tests.networks.domestic_water.test_demand.test_demand_builder_accepts_lowercase_catalog_lookup()** -> `None`
  - calls: DomesticWaterDemandBuilder.cold_water, DomesticWaterDemandBuilder.cold_water(_catalog()).compute_from_counts, _catalog
- **tests.networks.domestic_water.test_demand.test_invalid_counts_are_ignored()** -> `None`
  - calls: _catalog, compute_cold_water_demand

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_entity_access.py

- **tests.networks.domestic_water.test_entity_access.test_clean_entity_id()** -> `None`
  - calls: clean_entity_id
- **tests.networks.domestic_water.test_entity_access.test_clean_optional_code()** -> `None`
  - calls: clean_optional_code
- **tests.networks.domestic_water.test_entity_access.test_read_downstream_section_ids()** -> `None`
  - calls: _Node, read_downstream_section_ids
- **tests.networks.domestic_water.test_entity_access.test_write_section_downstream_appliance_counts()** -> `None`
  - calls: _Section, write_section_downstream_appliance_counts
- **tests.networks.domestic_water.test_entity_access.test_read_section_downstream_appliance_counts()** -> `None`
  - calls: _Section, read_section_downstream_appliance_counts
- **tests.networks.domestic_water.test_entity_access.test_write_node_downstream_appliance_counts()** -> `None`
  - calls: _Node, write_node_downstream_appliance_counts
- **tests.networks.domestic_water.test_entity_access.test_apply_section_pressures()** -> `None`
  - calls: _Section, apply_section_pressures
- **tests.networks.domestic_water.test_entity_access.test_apply_node_pressures()** -> `None`
  - calls: _Node, _NodeState, apply_node_pressures
- **tests.networks.domestic_water.test_entity_access.test_read_cell_appliance_counts()** -> `None`
  - calls: _Cell, read_cell_appliance_counts
- **tests.networks.domestic_water.test_entity_access.test_read_node_local_appliance_counts_from_method()** -> `None`
- **tests.networks.domestic_water.test_entity_access.NodeWithMethod.local_appliance_counts(self)** -> `dict[str, object]`
- **tests.networks.domestic_water.test_entity_access.test_read_node_local_appliance_counts_from_attributes_and_cells()** -> `None`
  - calls: _Cell, _Node, read_node_local_appliance_counts
- **tests.networks.domestic_water.test_entity_access.test_read_node_local_appliance_counts_handles_invalid_method()** -> `None`
- **tests.networks.domestic_water.test_entity_access.NodeWithInvalidMethod.local_appliance_counts(self)** -> `None`
  - raises: TypeError('invalid')
  - calls: TypeError
- **tests.networks.domestic_water.test_entity_access.test_read_section_pressure_loss_pa()** -> `None`
  - calls: _Section, isinstance, read_section_pressure_loss_pa
- **tests.networks.domestic_water.test_entity_access.test_read_section_pressure_loss_pa_missing()** -> `None`
  - calls: _Section, read_section_pressure_loss_pa
- **tests.networks.domestic_water.test_entity_access.test_read_section_pressure_loss_pa_invalid()** -> `None`
  - calls: _Section, read_section_pressure_loss_pa
- **tests.networks.domestic_water.test_entity_access.test_read_section_pressure_loss_pa_not_finite()** -> `None`
  - calls: _Section, float, read_section_pressure_loss_pa

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_fluid_rules.py

- **tests.networks.domestic_water.test_fluid_rules._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.domestic_water.test_fluid_rules.test_default_domestic_water_fluid_code()** -> `None`
  - calls: default_domestic_water_fluid_code
- **tests.networks.domestic_water.test_fluid_rules.test_resolve_domestic_water_fluid_uses_cold_default()** -> `None`
  - calls: _fluid_catalog, resolve_domestic_water_fluid
- **tests.networks.domestic_water.test_fluid_rules.test_resolve_domestic_water_fluid_uses_hot_default()** -> `None`
  - calls: _fluid_catalog, resolve_domestic_water_fluid
- **tests.networks.domestic_water.test_fluid_rules.test_resolve_domestic_water_fluid_temperature_override_has_priority()** -> `None`
  - calls: _fluid_catalog, resolve_domestic_water_fluid
- **tests.networks.domestic_water.test_fluid_rules.test_resolve_domestic_water_fluid_unknown_temperature_adds_error()** -> `None`
  - calls: _fluid_catalog, len, resolve_domestic_water_fluid
- **tests.networks.domestic_water.test_fluid_rules.test_resolve_domestic_water_fluid_missing_default_adds_error()** -> `None`
  - calls: FluidCatalog, len, resolve_domestic_water_fluid

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_message_binding.py

- **tests.networks.domestic_water.test_message_binding._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.domestic_water.test_message_binding._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.domestic_water.test_message_binding._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.domestic_water.test_message_binding._network_with_cell()** -> `Network`
  - calls: Cell, Network, Node, Section, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node
- **tests.networks.domestic_water.test_message_binding._network_without_appliances()** -> `Network`
  - calls: Network, Node, Section, network.add_node, network.add_section
- **tests.networks.domestic_water.test_message_binding.test_compute_from_network_binds_messages_to_network_and_sections()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network_with_cell, _pipe_catalog, compute_cold_water_network_from_network, hasattr, isinstance, network.get_section
- **tests.networks.domestic_water.test_message_binding.test_section_warning_is_bound_to_section_messages()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network_without_appliances, _pipe_catalog, any, compute_cold_water_network_from_network, hasattr, network.get_section
- **tests.networks.domestic_water.test_message_binding.test_facade_from_network_keeps_message_binding()** -> `None`
  - calls: ColdWaterNetworkEngine.from_network, ColdWaterNetworkEngine.from_network(network=network, appliance_catalog=_appliance_catalog(), pipe_catalog=_pipe_catalog(), fluid_catalog=_fluid_catalog()).compute_all, _appliance_catalog, _fluid_catalog, _network_with_cell, _pipe_catalog, hasattr, network.get_section
- **tests.networks.domestic_water.test_message_binding.test_public_api_exports_message_binding_tools()** -> `None`
  - calls: callable

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_network_compute_result.py

- **tests.networks.domestic_water.test_network_compute_result.test_network_compute_result_exports_are_kept_from_network_engine()** -> `None`
- **tests.networks.domestic_water.test_network_compute_result.test_domestic_water_network_step_values()** -> `None`
- **tests.networks.domestic_water.test_network_compute_result.test_section_compute_result_status_helpers()** -> `None`
  - calls: DomesticWaterSectionComputeResult, EngineMessage.warning, SimpleNamespace
- **tests.networks.domestic_water.test_network_compute_result.test_section_compute_result_error_helpers()** -> `None`
  - calls: DomesticWaterSectionComputeResult, EngineMessage.error, SimpleNamespace
- **tests.networks.domestic_water.test_network_compute_result.test_network_compute_result_count_helpers()** -> `None`
  - calls: DomesticWaterNetworkComputeResult, DomesticWaterSectionComputeResult, SimpleNamespace

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_network_engine.py

- **tests.networks.domestic_water.test_network_engine._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.domestic_water.test_network_engine._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.domestic_water.test_network_engine._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.domestic_water.test_network_engine._section(section_id, downstream_node_id, counts, elevation_change_m)** -> `Section`
  - calls: Section, section.downstream_appliance_counts.update
- **tests.networks.domestic_water.test_network_engine.test_compute_sections_sizes_and_computes_pressure_losses()** -> `None`
  - calls: DomesticWaterNetworkEngine.cold_water, _Node, _appliance_catalog, _fluid_catalog, _pipe_catalog, _section, engine.compute_sections
- **tests.networks.domestic_water.test_network_engine.test_compute_all_sizes_losses_and_propagates_pressure()** -> `None`
  - calls: _Node, _appliance_catalog, _fluid_catalog, _pipe_catalog, _section, compute_cold_water_network
- **tests.networks.domestic_water.test_network_engine.test_compute_all_without_source_only_computes_sections()** -> `None`
  - calls: _Node, _appliance_catalog, _fluid_catalog, _pipe_catalog, _section, compute_cold_water_network
- **tests.networks.domestic_water.test_network_engine.test_section_without_appliance_counts_returns_partial_without_exception()** -> `None`
  - calls: _Node, _appliance_catalog, _fluid_catalog, _pipe_catalog, _section, any, compute_cold_water_network
- **tests.networks.domestic_water.test_network_engine.test_hot_water_engine_ignores_cold_water_sections()** -> `None`
  - calls: DomesticWaterNetworkEngine.hot_water, _Node, _appliance_catalog, _fluid_catalog, _pipe_catalog, _section, engine.compute_sections

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_network_engine_appliance_propagation.py

- **tests.networks.domestic_water.test_network_engine_appliance_propagation._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.domestic_water.test_network_engine_appliance_propagation._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.domestic_water.test_network_engine_appliance_propagation._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.domestic_water.test_network_engine_appliance_propagation._network_with_terminal_cell()** -> `Network`
  - calls: Cell, Network, Node, Section, network.add_cell, network.add_node, network.add_section, network.attach_cell_to_node
- **tests.networks.domestic_water.test_network_engine_appliance_propagation.test_network_engine_uses_cell_node_appliance_propagation_before_sizing()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network_with_terminal_cell, _pipe_catalog, compute_cold_water_network_from_network, network.get_node, network.get_section
- **tests.networks.domestic_water.test_network_engine_appliance_propagation.test_network_engine_preserves_manual_section_counts_when_no_cells_are_attached()** -> `None`
  - calls: Network, Node, Section, _appliance_catalog, _fluid_catalog, _pipe_catalog, compute_cold_water_network_from_network, network.add_node, network.add_section, section.downstream_appliance_counts.update

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_numeric.py

- **tests.networks.domestic_water.test_numeric.test_safe_float()** -> `None`
  - calls: float, safe_float
- **tests.networks.domestic_water.test_numeric.test_safe_positive_float()** -> `None`
  - calls: float, safe_positive_float
- **tests.networks.domestic_water.test_numeric.test_positive_optional_float_alias()** -> `None`
  - calls: positive_optional_float
- **tests.networks.domestic_water.test_numeric.test_safe_non_negative_float()** -> `None`
  - calls: float, safe_non_negative_float
- **tests.networks.domestic_water.test_numeric.test_safe_pressure_pa()** -> `None`
  - calls: float, safe_pressure_pa

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_pipe_rules.py

- **tests.networks.domestic_water.test_pipe_rules._section()** -> `Section`
  - calls: Section
- **tests.networks.domestic_water.test_pipe_rules._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.domestic_water.test_pipe_rules.test_relative_roughness_for_section()** -> `None`
  - calls: _pipe_catalog, _section, isclose, relative_roughness_for_section
- **tests.networks.domestic_water.test_pipe_rules.test_relative_roughness_for_section_without_catalog_returns_zero()** -> `None`
  - calls: _section, relative_roughness_for_section
- **tests.networks.domestic_water.test_pipe_rules.test_relative_roughness_for_section_without_selected_pipe_returns_zero()** -> `None`
  - calls: _pipe_catalog, _section, relative_roughness_for_section
- **tests.networks.domestic_water.test_pipe_rules.test_relative_roughness_for_section_with_unknown_pipe_returns_zero()** -> `None`
  - calls: _pipe_catalog, _section, relative_roughness_for_section
- **tests.networks.domestic_water.test_pipe_rules.test_relative_roughness_for_section_with_unknown_material_returns_zero()** -> `None`
  - calls: PipeCatalog, PipeSize, _section, relative_roughness_for_section

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_pressure_loss.py

- **tests.networks.domestic_water.test_pressure_loss._DirectZeta.__init__(self, zeta, quantity)** -> `None`
- **tests.networks.domestic_water.test_pressure_loss._CatalogLoss.__init__(self, loss_code, quantity)** -> `None`
- **tests.networks.domestic_water.test_pressure_loss._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.domestic_water.test_pressure_loss._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.domestic_water.test_pressure_loss._singular_loss_catalog()** -> `SingularLossCatalog`
  - calls: SingularLoss, SingularLossCatalog
- **tests.networks.domestic_water.test_pressure_loss._section(**kwargs)** -> `Section`
  - calls: Section, values.update
- **tests.networks.domestic_water.test_pressure_loss.test_compute_cold_water_section_pressure_loss_with_direct_zeta()** -> `None`
  - calls: _DirectZeta, _fluid_catalog, _pipe_catalog, _section, compute_cold_water_section_pressure_loss, section.singular_losses.append
- **tests.networks.domestic_water.test_pressure_loss.test_compute_pressure_loss_uses_pipe_catalog_roughness()** -> `None`
  - calls: _fluid_catalog, _pipe_catalog, _section, compute_cold_water_section_pressure_loss
- **tests.networks.domestic_water.test_pressure_loss.test_compute_pressure_loss_from_catalog_zeta()** -> `None`
  - calls: _CatalogLoss, _fluid_catalog, _pipe_catalog, _section, _singular_loss_catalog, compute_cold_water_section_pressure_loss, isclose, section.singular_losses.append
- **tests.networks.domestic_water.test_pressure_loss.test_compute_pressure_loss_from_catalog_kv()** -> `None`
  - calls: _CatalogLoss, _fluid_catalog, _pipe_catalog, _section, _singular_loss_catalog, compute_cold_water_section_pressure_loss, section.singular_losses.append
- **tests.networks.domestic_water.test_pressure_loss.test_missing_diameter_returns_failure_without_exception()** -> `None`
  - calls: _fluid_catalog, _pipe_catalog, _section, any, compute_cold_water_section_pressure_loss
- **tests.networks.domestic_water.test_pressure_loss.test_zero_flow_keeps_elevation_only()** -> `None`
  - calls: _fluid_catalog, _pipe_catalog, _section, compute_cold_water_section_pressure_loss
- **tests.networks.domestic_water.test_pressure_loss.test_hot_water_uses_hot_water_fluid_by_default()** -> `None`
  - calls: _fluid_catalog, _pipe_catalog, _section, compute_hot_water_section_pressure_loss
- **tests.networks.domestic_water.test_pressure_loss.test_temperature_override_uses_interpolated_water()** -> `None`
  - calls: _fluid_catalog, _pipe_catalog, _section, compute_cold_water_section_pressure_loss
- **tests.networks.domestic_water.test_pressure_loss.test_unknown_singular_loss_creates_warning_without_failure()** -> `None`
  - calls: _CatalogLoss, _fluid_catalog, _pipe_catalog, _section, _singular_loss_catalog, any, compute_cold_water_section_pressure_loss, section.singular_losses.append

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_pressure_loss_result.py

- **tests.networks.domestic_water.test_pressure_loss_result._fluid()** -> `Fluid`
  - calls: Fluid
- **tests.networks.domestic_water.test_pressure_loss_result._inputs()** -> `DomesticWaterSectionHydraulicInputs`
  - calls: DomesticWaterSectionHydraulicInputs
- **tests.networks.domestic_water.test_pressure_loss_result._breakdown()** -> `PressureLossBreakdown`
  - calls: PressureLossBreakdown
- **tests.networks.domestic_water.test_pressure_loss_result.test_build_section_pressure_loss_result_success_writes_section_state()** -> `None`
  - calls: _Section, _breakdown, _fluid, _inputs, build_section_pressure_loss_result, isinstance
- **tests.networks.domestic_water.test_pressure_loss_result.test_build_section_pressure_loss_result_failure_when_messages_contain_error()** -> `None`
  - calls: EngineMessage.error, _Section, _breakdown, _fluid, _inputs, build_section_pressure_loss_result

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_pressure_network.py

- **tests.networks.domestic_water.test_pressure_network.test_propagate_pressures_on_simple_network()** -> `None`
  - calls: _Node, _Section, propagate_cold_water_pressures
- **tests.networks.domestic_water.test_pressure_network.test_branching_keeps_most_unfavorable_pressure_on_merge()** -> `None`
  - calls: DomesticWaterPressureNetworkEngine, _Node, _Section, engine.propagate_pressures
- **tests.networks.domestic_water.test_pressure_network.test_negative_pressure_loss_increases_downstream_pressure()** -> `None`
  - calls: _Node, _Section, propagate_cold_water_pressures
- **tests.networks.domestic_water.test_pressure_network.test_missing_pressure_loss_warns_and_uses_zero_delta_p()** -> `None`
  - calls: _Node, _Section, any, propagate_cold_water_pressures
- **tests.networks.domestic_water.test_pressure_network.test_unknown_source_returns_failure()** -> `None`
  - calls: any, propagate_cold_water_pressures
- **tests.networks.domestic_water.test_pressure_network.test_worst_terminal_summary()** -> `None`
  - calls: _Node, _Section, round, set, summarize_cold_water_worst_terminal_pressure
- **tests.networks.domestic_water.test_pressure_network.test_hot_water_sections_are_ignored_by_cold_water_engine()** -> `None`
  - calls: _Node, _Section, propagate_cold_water_pressures, set

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_pressure_network_result.py

- **tests.networks.domestic_water.test_pressure_network_result.test_pressure_network_result_exports_are_kept_from_pressure_network()** -> `None`
- **tests.networks.domestic_water.test_pressure_network_result.test_pressure_propagation_status_values()** -> `None`
- **tests.networks.domestic_water.test_pressure_network_result.test_pressure_propagation_result_helpers()** -> `None`
  - calls: DomesticWaterPressurePropagationResult, EngineMessage.warning, NodePressureState
- **tests.networks.domestic_water.test_pressure_network_result.test_pressure_propagation_result_error_helper()** -> `None`
  - calls: DomesticWaterPressurePropagationResult, EngineMessage.error
- **tests.networks.domestic_water.test_pressure_network_result.test_pressure_summary_helpers()** -> `None`
  - calls: DomesticWaterPressurePropagationResult, DomesticWaterPressureSummary, NodePressureState, TerminalPressureStatus

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_section_hydraulic_inputs.py

- **tests.networks.domestic_water.test_section_hydraulic_inputs._section()** -> `Section`
  - calls: Section
- **tests.networks.domestic_water.test_section_hydraulic_inputs.test_prepare_section_hydraulic_inputs_full_mode()** -> `None`
  - calls: _section, isinstance, prepare_section_hydraulic_inputs
- **tests.networks.domestic_water.test_section_hydraulic_inputs.test_prepare_section_hydraulic_inputs_elevation_only_mode()** -> `None`
  - calls: _section, len, prepare_section_hydraulic_inputs
- **tests.networks.domestic_water.test_section_hydraulic_inputs.test_prepare_section_hydraulic_inputs_missing_diameter_returns_none()** -> `None`
  - calls: _section, len, prepare_section_hydraulic_inputs
- **tests.networks.domestic_water.test_section_hydraulic_inputs.test_prepare_section_hydraulic_inputs_clamps_negative_length()** -> `None`
  - calls: _section, prepare_section_hydraulic_inputs

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_section_sizing.py

- **tests.networks.domestic_water.test_section_sizing._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.domestic_water.test_section_sizing._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.domestic_water.test_section_sizing._section(**kwargs)** -> `Section`
  - calls: Section, values.update
- **tests.networks.domestic_water.test_section_sizing.test_velocity_limit_for_context()** -> `None`
  - calls: velocity_limit_for_context
- **tests.networks.domestic_water.test_section_sizing.test_size_cold_water_section_automatic()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, size_cold_water_section_from_counts
- **tests.networks.domestic_water.test_section_sizing.test_size_section_respects_machine_exclusivity()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, size_cold_water_section_from_counts
- **tests.networks.domestic_water.test_section_sizing.test_size_cold_water_section_with_forced_pipe()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, size_cold_water_section_from_counts
- **tests.networks.domestic_water.test_section_sizing.test_size_cold_water_section_with_forced_internal_diameter()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, size_cold_water_section_from_counts
- **tests.networks.domestic_water.test_section_sizing.test_forced_diameter_below_minimum_creates_warning()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, any, size_cold_water_section_from_counts
- **tests.networks.domestic_water.test_section_sizing.test_unknown_forced_pipe_returns_failure()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, any, size_cold_water_section_from_counts
- **tests.networks.domestic_water.test_section_sizing.test_zero_hot_water_demand_returns_partial_without_exception()** -> `None`
  - calls: _appliance_catalog, _pipe_catalog, _section, any, size_hot_water_section_from_counts

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_section_sizing_result.py

- **tests.networks.domestic_water.test_section_sizing_result.test_section_sizing_result_exports_are_kept_from_section_sizing()** -> `None`
- **tests.networks.domestic_water.test_section_sizing_result.test_section_sizing_mode_values()** -> `None`
- **tests.networks.domestic_water.test_section_sizing_result.test_section_sizing_result_helpers_for_sized_section()** -> `None`
  - calls: DomesticWaterSectionSizing, EngineMessage.warning, SimpleNamespace
- **tests.networks.domestic_water.test_section_sizing_result.test_section_sizing_result_helpers_for_error()** -> `None`
  - calls: DomesticWaterSectionSizing, EngineMessage.error, SimpleNamespace

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_section_state.py

- **tests.networks.domestic_water.test_section_state.test_apply_section_sizing_state()** -> `None`
  - calls: SimpleNamespace, _Section, apply_section_sizing_state
- **tests.networks.domestic_water.test_section_state.test_apply_section_pressure_loss_state()** -> `None`
  - calls: SimpleNamespace, _Section, apply_section_pressure_loss_state

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_side_matching.py

- **tests.networks.domestic_water.test_side_matching.test_normalize_domestic_water_fluid_code()** -> `None`
  - calls: normalize_domestic_water_fluid_code
- **tests.networks.domestic_water.test_side_matching.test_domestic_water_fluid_codes_are_canonical()** -> `None`
  - calls: cold_water_fluid_codes, hot_water_fluid_codes
- **tests.networks.domestic_water.test_side_matching.test_domestic_water_fluid_codes_for_side()** -> `None`
  - calls: domestic_water_fluid_codes_for_side
- **tests.networks.domestic_water.test_side_matching.test_domestic_water_side_from_fluid_code()** -> `None`
  - calls: domestic_water_side_from_fluid_code
- **tests.networks.domestic_water.test_side_matching.test_section_matches_domestic_water_side()** -> `None`
  - calls: _Section, section_matches_domestic_water_side
- **tests.networks.domestic_water.test_side_matching.test_node_is_terminal_for_domestic_water_side()** -> `None`
  - calls: _Node, _Section, node_is_terminal_for_domestic_water_side

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_simultaneity.py

- **tests.networks.domestic_water.test_simultaneity.test_collective_dtu_simultaneity_is_one_below_threshold()** -> `None`
  - calls: collective_dtu_simultaneity_factor
- **tests.networks.domestic_water.test_simultaneity.test_collective_dtu_simultaneity_uses_formula_from_threshold()** -> `None`
  - calls: collective_dtu_simultaneity_factor, isclose, sqrt
- **tests.networks.domestic_water.test_simultaneity.test_collective_dtu_simultaneity_is_safe_for_invalid_values()** -> `None`
  - calls: collective_dtu_simultaneity_factor
- **tests.networks.domestic_water.test_simultaneity.test_clamp_simultaneity_factor()** -> `None`
  - calls: clamp_simultaneity_factor

## C:\dev\PythonProject_v4\tests\networks\domestic_water\test_singular_loss_rules.py

- **tests.networks.domestic_water.test_singular_loss_rules._section()** -> `Section`
  - calls: Section
- **tests.networks.domestic_water.test_singular_loss_rules._catalog()** -> `SingularLossCatalog`
  - calls: SingularLoss, SingularLossCatalog
- **tests.networks.domestic_water.test_singular_loss_rules.test_zeta_from_direct_section_item()** -> `None`
  - calls: _DirectZeta, _section, zeta_from_section_singular_loss_item
- **tests.networks.domestic_water.test_singular_loss_rules.test_zeta_from_catalog_zeta_loss()** -> `None`
  - calls: _CatalogLoss, _catalog, _section, isclose, zeta_from_section_singular_loss_item
- **tests.networks.domestic_water.test_singular_loss_rules.test_zeta_from_catalog_kv_loss()** -> `None`
  - calls: _CatalogLoss, _catalog, _section, zeta_from_section_singular_loss_item
- **tests.networks.domestic_water.test_singular_loss_rules.test_unknown_catalog_loss_adds_warning()** -> `None`
  - calls: _CatalogLoss, _catalog, _section, len, zeta_from_section_singular_loss_item
- **tests.networks.domestic_water.test_singular_loss_rules.test_missing_catalog_adds_warning()** -> `None`
  - calls: _CatalogLoss, _section, len, zeta_from_section_singular_loss_item
- **tests.networks.domestic_water.test_singular_loss_rules.test_kv_loss_without_flow_adds_warning()** -> `None`
  - calls: _CatalogLoss, _catalog, _section, len, zeta_from_section_singular_loss_item
- **tests.networks.domestic_water.test_singular_loss_rules.test_collect_section_singular_zeta_values()** -> `None`
  - calls: _CatalogLoss, _DirectZeta, _catalog, _section, collect_section_singular_zeta_values, section.singular_losses.append

## C:\dev\PythonProject_v4\tests\networks\hot_water\test_engine.py

- **tests.networks.hot_water.test_engine._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.hot_water.test_engine._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.hot_water.test_engine._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.hot_water.test_engine._network()** -> `tuple[dict[str, _Node], dict[str, Section]]`
  - calls: Section, _Node, section.downstream_appliance_counts.update
- **tests.networks.hot_water.test_engine.test_hot_water_facade_exposes_hot_water_side()** -> `None`
  - calls: HotWaterNetworkEngine, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.domestic_engine
- **tests.networks.hot_water.test_engine.test_hot_water_facade_compute_sections_uses_hot_water_flow()** -> `None`
  - calls: HotWaterNetworkEngine, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.compute_sections
- **tests.networks.hot_water.test_engine.test_compute_hot_water_network_functional_entry_point()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, compute_hot_water_network

## C:\dev\PythonProject_v4\tests\networks\test_network_domain_integration.py

- **tests.networks.test_network_domain_integration._appliance_catalog()** -> `ApplianceCatalog`
  - calls: Appliance, ApplianceCatalog
- **tests.networks.test_network_domain_integration._pipe_catalog()** -> `PipeCatalog`
  - calls: PipeCatalog, PipeMaterial, PipeSize
- **tests.networks.test_network_domain_integration._fluid_catalog()** -> `FluidCatalog`
  - calls: Fluid, FluidCatalog
- **tests.networks.test_network_domain_integration._network(fluid_code)** -> `Network`
  - calls: Network, Node, Section, network.add_node, network.add_section, section.downstream_appliance_counts.update
- **tests.networks.test_network_domain_integration._network_with_unknown_downstream_node()** -> `Network`
  - calls: Network, Node, Section, network.add_node, network.add_section, section.downstream_appliance_counts.update
- **tests.networks.test_network_domain_integration._network_without_section()** -> `Network`
  - calls: Network, Node, network.add_node
- **tests.networks.test_network_domain_integration.test_domestic_water_engine_can_be_created_from_domain_network()** -> `None`
  - calls: DomesticWaterNetworkEngine.cold_water_from_network, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.compute_all, network.get_node
- **tests.networks.test_network_domain_integration.test_cold_water_facade_from_network_computes_domain_network()** -> `None`
  - calls: ColdWaterNetworkEngine.from_network, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.compute_all, network.get_node, network.get_section
- **tests.networks.test_network_domain_integration.test_hot_water_facade_from_network_computes_domain_network()** -> `None`
  - calls: HotWaterNetworkEngine.from_network, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.compute_all, network.get_node
- **tests.networks.test_network_domain_integration.test_compute_cold_water_network_from_domain_entry_point()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, compute_cold_water_network_from_domain, network.get_section
- **tests.networks.test_network_domain_integration.test_compute_hot_water_network_from_domain_entry_point()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, compute_hot_water_network_from_domain, network.get_section
- **tests.networks.test_network_domain_integration.test_public_network_api_exports_domain_entry_points()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, compute_cold_water_network_from_network, compute_hot_water_network_from_network
- **tests.networks.test_network_domain_integration.test_facade_propagate_pressures_uses_existing_losses_without_resizing()** -> `None`
  - calls: ColdWaterNetworkEngine.from_network, _appliance_catalog, _fluid_catalog, _network, _pipe_catalog, engine.propagate_pressures, network.get_section
- **tests.networks.test_network_domain_integration.test_compute_from_invalid_domain_network_returns_managed_failure()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network_with_unknown_downstream_node, _pipe_catalog, any, compute_cold_water_network_from_network, network.get_section
- **tests.networks.test_network_domain_integration.test_compute_from_domain_network_with_topology_warning_keeps_best_effort_result()** -> `None`
  - calls: _appliance_catalog, _fluid_catalog, _network_without_section, _pipe_catalog, any, compute_cold_water_network_from_network

## C:\dev\PythonProject_v4\tests\networks\test_public_api.py

- **tests.networks.test_public_api.test_networks_public_api_exports_facades()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_engine_types()** -> `None`
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_domain_types()** -> `None`
- **tests.networks.test_public_api.test_networks_public_api_exports_section_sizing_types()** -> `None`
- **tests.networks.test_public_api.test_networks_public_api_exports_pressure_loss_types()** -> `None`
- **tests.networks.test_public_api.test_networks_public_api_exports_pressure_network_types()** -> `None`
- **tests.networks.test_public_api.test_networks_public_api_exports_appliance_propagation_types()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_message_binding_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_side_matching_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_appliance_count_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_entity_access_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_numeric_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_section_state_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_appliance_rules_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_singular_loss_rules()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_pipe_rules()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_fluid_rules()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_section_hydraulic_inputs()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_exports_domestic_water_pressure_loss_result_tools()** -> `None`
  - calls: callable
- **tests.networks.test_public_api.test_networks_public_api_all_is_unique_and_resolvable()** -> `None`
  - calls: hasattr, len, set
- **tests.networks.test_public_api.test_domestic_water_public_api_all_is_unique_and_resolvable()** -> `None`
  - calls: hasattr, len, set