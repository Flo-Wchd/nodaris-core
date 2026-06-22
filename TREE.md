PythonProject_v4
├── bin/
│   ├── __init__.py
│   ├── audit_io.py
│   └── generate_tree.py
├── data/
│   ├── standards/
│   │   ├── nf_dtu_60_11_domestic_water.yaml
│   │   ├── nf_dtu_60_11_drainage.yaml
│   │   ├── nf_dtu_60_11_hot_water_loop.yaml
│   │   └── nf_dtu_60_11_rainwater.yaml
│   ├── appliances.yaml
│   ├── pipes.yaml
│   ├── singular_losses_cold_water.yaml
│   ├── singular_losses_hot_water.yaml
│   └── water_atm_table.yaml
├── docs/
│   ├── api/
│   │   ├── catalogs.md
│   │   ├── common.md
│   │   ├── domain.md
│   │   ├── exporters.md
│   │   ├── hydraulics.md
│   │   ├── io.md
│   │   └── networks.md
│   ├── calculations/
│   │   ├── cold_water.md
│   │   ├── domestic_water.md
│   │   ├── drainage.md
│   │   ├── heating.md
│   │   ├── hot_water.md
│   │   ├── hot_water_loop.md
│   │   ├── pressure_losses.md
│   │   ├── rainwater.md
│   │   └── ventilation.md
│   ├── architecture.md
│   ├── data_catalogs.md
│   ├── development_workflow.md
│   ├── index.md
│   └── naming_and_glossary.md
├── gui/
│   ├── assets/
│   │   ├── icons/
│   │   ├── images/
│   │   └── themes/
│   │       ├── dark/
│   │       │   ├── palette.json
│   │       │   └── qss.qss
│   │       └── light/
│   │           ├── palette.json
│   │           └── qss.qss
│   ├── common/
│   │   ├── __init__.py
│   │   ├── formatting.py
│   │   ├── icon_registry.py
│   │   ├── message_bus.py
│   │   ├── ressource_paths.py
│   │   ├── theme.py
│   │   ├── undo.py
│   │   └── validators.py
│   ├── modules/
│   │   ├── cold_water/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   ├── drainage/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   ├── heating/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   ├── hot_water/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   ├── hot_water_loop/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   ├── rainwater/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   ├── ventilation/
│   │   │   ├── __init__.py
│   │   │   └── context.py
│   │   └── __init__.py
│   ├── persistence/
│   │   ├── schema/
│   │   │   ├── __init__.py
│   │   │   └── project_v1.py
│   │   ├── __init__.py
│   │   └── project_store.py
│   ├── qt_adapters/
│   │   ├── delegates/
│   │   │   ├── __init__.py
│   │   │   └── pipe_delegate.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── appliances_table_model.py
│   │   │   ├── network_qmodel.py
│   │   │   ├── section_qmodel.py
│   │   │   └── section_table_model.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── demo_loader.py
│   │   └── project_runtime_network_sync.py
│   ├── viewmodels/
│   │   ├── modules/
│   │   │   ├── __init__.py
│   │   │   ├── cold_water_vm.py
│   │   │   ├── drainage_vm.py
│   │   │   ├── heating_vm.py
│   │   │   ├── hot_water_loop_vm.py
│   │   │   ├── hot_water_vm.py
│   │   │   ├── rainwater_vm.py
│   │   │   └── ventilation_vm.py
│   │   ├── __init__.py
│   │   ├── main_vm.py
│   │   └── project_vm.py
│   ├── views/
│   │   ├── main/
│   │   │   ├── __init__.py
│   │   │   ├── actions.py
│   │   │   ├── cell_tree_builder.py
│   │   │   ├── commands.py
│   │   │   ├── controller.py
│   │   │   ├── layout.py
│   │   │   ├── network_tree_builder.py
│   │   │   ├── page_navigation.py
│   │   │   ├── properties_wiring.py
│   │   │   ├── startup_loading.py
│   │   │   └── synoptic_builder.py
│   │   ├── modules/
│   │   │   ├── cold_water/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   ├── drainage/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   ├── heating/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   ├── hot_water/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   ├── hot_water_loop/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   ├── rainwater/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   ├── ventilation/
│   │   │   │   ├── __init__.py
│   │   │   │   └── dialogs.py
│   │   │   └── __init__.py
│   │   ├── project/
│   │   │   ├── __init__.py
│   │   │   ├── project_dashboard.py
│   │   │   ├── project_settings.py
│   │   │   └── project_welcome.py
│   │   ├── __init__.py
│   │   └── main_window.py
│   ├── widgets/
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   ├── add_cell_appliance_dialog.py
│   │   │   └── add_cell_dialog.py
│   │   ├── tables/
│   │   │   ├── __init__.py
│   │   │   ├── appliances_table.py
│   │   │   └── sections_table.py
│   │   ├── __init__.py
│   │   ├── collapsible_console.py
│   │   ├── module_tile.py
│   │   ├── network_tree.py
│   │   ├── project_header.py
│   │   ├── properties_panel.py
│   │   ├── status_bar.py
│   │   ├── synoptic_editor.py
│   │   └── top_bar.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py
│   └── bootstrap.py
├── ndc_core/
│   ├── catalogs/
│   │   ├── loaders/
│   │   │   ├── __init__.py
│   │   │   ├── catalog_paths.py
│   │   │   └── yaml_loader.py
│   │   ├── __init__.py
│   │   ├── appliance_catalog.py
│   │   ├── fluid_catalog.py
│   │   ├── pipe_catalog.py
│   │   ├── singular_loss_catalog.py
│   │   └── standards_catalog.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── messages.py
│   │   ├── result.py
│   │   ├── status.py
│   │   └── units.py
│   ├── demo/
│   │   ├── __init__.py
│   │   ├── cold_water_demo.py
│   │   ├── hot_water_demo.py
│   │   └── project_demo.py
│   ├── domain/
│   │   ├── networks/
│   │   │   ├── __init__.py
│   │   │   ├── cell.py
│   │   │   ├── network.py
│   │   │   ├── node.py
│   │   │   ├── section.py
│   │   │   └── types.py
│   │   ├── __init__.py
│   │   ├── appliances.py
│   │   ├── fluids.py
│   │   ├── pipes.py
│   │   └── singular_losses.py
│   ├── exporters/
│   │   ├── cold_water/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_exporter.py
│   │   │   ├── report_data.py
│   │   │   └── word_exporter.py
│   │   ├── common/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_theme.py
│   │   │   ├── report_data.py
│   │   │   ├── report_sections.py
│   │   │   └── word_theme.py
│   │   ├── hot_water/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_exporter.py
│   │   │   ├── report_data.py
│   │   │   └── word_exporter.py
│   │   ├── hot_water_loop/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_exporter.py
│   │   │   ├── report_data.py
│   │   │   └── word_exporter.py
│   │   └── __init__.py
│   ├── hydraulics/
│   │   ├── __init__.py
│   │   ├── conversions.py
│   │   ├── elevation_pressure_loss.py
│   │   ├── friction.py
│   │   ├── linear_pressure_loss.py
│   │   ├── pipe_sizing.py
│   │   ├── reynolds.py
│   │   ├── singular_pressure_loss.py
│   │   ├── total_pressure_loss.py
│   │   ├── types.py
│   │   └── velocity.py
│   ├── io/
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── cold_water_serializer.py
│   │   │   ├── drainage_serializer.py
│   │   │   ├── hot_water_loop_serializer.py
│   │   │   ├── hot_water_serializer.py
│   │   │   ├── network_serializer.py
│   │   │   └── rainwater_serializer.py
│   │   ├── __init__.py
│   │   ├── project_reader.py
│   │   ├── project_schema.py
│   │   └── project_writer.py
│   ├── networks/
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py
│   │   │   ├── pipeline.py
│   │   │   ├── result.py
│   │   │   ├── types.py
│   │   │   └── validation.py
│   │   ├── cold_water/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py
│   │   │   ├── profile.py
│   │   │   └── types.py
│   │   ├── domestic_water/
│   │   │   ├── __init__.py
│   │   │   ├── demand.py
│   │   │   ├── engine.py
│   │   │   ├── pressure.py
│   │   │   ├── pressure_loss.py
│   │   │   ├── profiles.py
│   │   │   ├── section_sizing.py
│   │   │   ├── simultaneity.py
│   │   │   ├── types.py
│   │   │   └── worst_path.py
│   │   ├── drainage/
│   │   │   ├── __init__.py
│   │   │   ├── branch_sizing.py
│   │   │   ├── collector_sizing.py
│   │   │   ├── discharge_units.py
│   │   │   ├── engine.py
│   │   │   ├── simultaneity.py
│   │   │   ├── stack_sizing.py
│   │   │   └── types.py
│   │   ├── heating/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py
│   │   │   ├── profile.py
│   │   │   └── types.py
│   │   ├── hot_water/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py
│   │   │   ├── profile.py
│   │   │   └── types.py
│   │   ├── hot_water_loop/
│   │   │   ├── __init__.py
│   │   │   ├── balancing.py
│   │   │   ├── engine.py
│   │   │   ├── loop_flow.py
│   │   │   ├── pump_head.py
│   │   │   ├── return_sizing.py
│   │   │   ├── thermal_losses.py
│   │   │   └── types.py
│   │   ├── rainwater/
│   │   │   ├── __init__.py
│   │   │   ├── collector_sizing.py
│   │   │   ├── downpipe_sizing.py
│   │   │   ├── engine.py
│   │   │   ├── gutter_sizing.py
│   │   │   ├── rainfall.py
│   │   │   ├── roof_area.py
│   │   │   └── types.py
│   │   ├── ventilation/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py
│   │   │   ├── profile.py
│   │   │   └── types.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── paths.py
│   └── __init__.py
├── scripts/
│   ├── __init__.py
│   ├── generate_demo_project.py
│   └── run_smoke_tests.py
├── tests/
│   ├── catalogs/
│   │   ├── __init__.py
│   │   ├── test_appliance_catalog.py
│   │   ├── test_catalog_paths.py
│   │   ├── test_fluid_catalog.py
│   │   ├── test_pipe_catalog.py
│   │   ├── test_real_catalog_file.py
│   │   ├── test_singular_loss_catalog.py
│   │   ├── test_standards_catalog.py
│   │   └── test_yaml_loader.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── test_messages.py
│   │   └── test_result.py
│   ├── domain/
│   │   ├── networks/
│   │   │   ├── __init__.py
│   │   │   ├── test_cell.py
│   │   │   ├── test_network.py
│   │   │   ├── test_node.py
│   │   │   └── test_section.py
│   │   ├── __init__.py
│   │   ├── test_appliances.py
│   │   ├── test_fluids.py
│   │   ├── test_pipes.py
│   │   └── test_singular_losses.py
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── test_cold_water_report_data.py
│   │   └── test_hot_water_report_data.py
│   ├── gui/
│   │   ├── __init__.py
│   │   └── test_gui_smoke.py
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── catalog_builders.py
│   │   └── network_builders.py
│   ├── hydraulics/
│   │   ├── __init__.py
│   │   ├── test_conversions.py
│   │   ├── test_elevation_pressure_loss.py
│   │   ├── test_friction.py
│   │   ├── test_linear_pressure_loss.py
│   │   ├── test_pipe_sizing.py
│   │   ├── test_pressure_losses.py
│   │   ├── test_reynolds.py
│   │   ├── test_singular_pressure_loss.py
│   │   ├── test_total_pressure_loss.py
│   │   └── test_velocity.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_cold_water_full_workflow.py
│   │   ├── test_hot_water_full_workflow.py
│   │   └── test_project_save_open_compute_workflow.py
│   ├── io/
│   │   ├── __init__.py
│   │   ├── test_project_reader.py
│   │   ├── test_project_writer.py
│   │   └── test_serializers.py
│   ├── networks/
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   ├── test_engine.py
│   │   │   ├── test_pipeline.py
│   │   │   └── test_result.py
│   │   ├── cold_water/
│   │   │   ├── __init__.py
│   │   │   ├── test_engine.py
│   │   │   └── test_profile.py
│   │   ├── domestic_water/
│   │   │   ├── __init__.py
│   │   │   ├── test_demand.py
│   │   │   ├── test_engine.py
│   │   │   ├── test_pressure.py
│   │   │   ├── test_pressure_loss.py
│   │   │   ├── test_profiles.py
│   │   │   ├── test_section_sizing.py
│   │   │   └── test_simultaneity.py
│   │   ├── drainage/
│   │   │   ├── __init__.py
│   │   │   ├── test_branch_sizing.py
│   │   │   ├── test_collector_sizing.py
│   │   │   ├── test_discharge_units.py
│   │   │   ├── test_engine.py
│   │   │   ├── test_simultaneity.py
│   │   │   └── test_stack_sizing.py
│   │   ├── hot_water/
│   │   │   ├── __init__.py
│   │   │   ├── test_engine.py
│   │   │   └── test_profile.py
│   │   ├── hot_water_loop/
│   │   │   ├── __init__.py
│   │   │   ├── test_balancing.py
│   │   │   ├── test_engine.py
│   │   │   ├── test_loop_flow.py
│   │   │   ├── test_return_sizing.py
│   │   │   └── test_thermal_losses.py
│   │   ├── rainwater/
│   │   │   ├── __init__.py
│   │   │   ├── test_collector_sizing.py
│   │   │   ├── test_downpipe_sizing.py
│   │   │   ├── test_engine.py
│   │   │   ├── test_gutter_sizing.py
│   │   │   ├── test_rainfall.py
│   │   │   └── test_roof_area.py
│   │   └── __init__.py
│   └── __init__.py
├── AUDIT_IO.md
├── mkdocs.yml
├── poetry.lock
├── poetry.toml
├── pyproject.toml
├── README.md
└── TREE.md
