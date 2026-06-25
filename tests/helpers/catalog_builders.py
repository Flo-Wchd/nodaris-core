from __future__ import annotations

from ndc_core.catalogs.appliance_catalog import ApplianceCatalog
from ndc_core.catalogs.fluid_catalog import FluidCatalog
from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.domain.appliances import Appliance
from ndc_core.domain.fluids import Fluid
from ndc_core.domain.pipes import PipeMaterial, PipeSize
from ndc_core.domain.singular_losses import SingularLoss


def domestic_water_appliance_catalog() -> ApplianceCatalog:
    return ApplianceCatalog(
        appliances_by_code={
            "L": Appliance(
                code="L",
                name="Lavabo",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=10.0,
            ),
            "D": Appliance(
                code="D",
                name="Douche",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=12.0,
            ),
            "WC": Appliance(
                code="WC",
                name="WC",
                cold_water_flow_l_s=0.12,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
            "E": Appliance(
                code="E",
                name="Evier",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.20,
                min_internal_diameter_mm=12.0,
            ),
            "LL": Appliance(
                code="LL",
                name="Lave-linge",
                cold_water_flow_l_s=0.20,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
            "LV": Appliance(
                code="LV",
                name="Lave-vaisselle",
                cold_water_flow_l_s=0.10,
                hot_water_flow_l_s=0.0,
                min_internal_diameter_mm=10.0,
            ),
        }
    )


def domestic_water_pipe_catalog() -> PipeCatalog:
    efs_material = PipeMaterial(
        code="EFS",
        name="EFS material",
        default_roughness_m=0.0000015,
    )
    ecs_material = PipeMaterial(
        code="ECS",
        name="ECS material",
        default_roughness_m=0.0000015,
    )

    return PipeCatalog(
        materials_by_code={
            "EFS": efs_material,
            "ECS": ecs_material,
        },
        sizes_by_code={
            "EFS12": PipeSize(
                code="EFS12",
                material_code="EFS",
                nominal_diameter="DN12",
                internal_diameter_mm=12.0,
            ),
            "EFS16": PipeSize(
                code="EFS16",
                material_code="EFS",
                nominal_diameter="DN16",
                internal_diameter_mm=16.0,
            ),
            "EFS20": PipeSize(
                code="EFS20",
                material_code="EFS",
                nominal_diameter="DN20",
                internal_diameter_mm=20.0,
            ),
            "EFS26": PipeSize(
                code="EFS26",
                material_code="EFS",
                nominal_diameter="DN26",
                internal_diameter_mm=26.0,
            ),
            "ECS12": PipeSize(
                code="ECS12",
                material_code="ECS",
                nominal_diameter="DN12",
                internal_diameter_mm=12.0,
            ),
            "ECS16": PipeSize(
                code="ECS16",
                material_code="ECS",
                nominal_diameter="DN16",
                internal_diameter_mm=16.0,
            ),
            "ECS20": PipeSize(
                code="ECS20",
                material_code="ECS",
                nominal_diameter="DN20",
                internal_diameter_mm=20.0,
            ),
            "ECS26": PipeSize(
                code="ECS26",
                material_code="ECS",
                nominal_diameter="DN26",
                internal_diameter_mm=26.0,
            ),
        },
        size_codes_by_material={
            "EFS": ["EFS12", "EFS16", "EFS20", "EFS26"],
            "ECS": ["ECS12", "ECS16", "ECS20", "ECS26"],
        },
    )


def domestic_water_fluid_catalog() -> FluidCatalog:
    cold = Fluid(
        code="cold_water",
        name="Cold water",
        temperature_c=10.0,
        density_kg_m3=1000.0,
        dynamic_viscosity_pa_s=0.001,
    )
    hot = Fluid(
        code="hot_water",
        name="Hot water",
        temperature_c=60.0,
        density_kg_m3=983.0,
        dynamic_viscosity_pa_s=0.000466,
    )

    return FluidCatalog(
        fluids_by_code={
            "cold_water": cold,
            "hot_water": hot,
        },
        water_points_by_temperature={
            10.0: cold,
            60.0: hot,
        },
    )


def domestic_water_singular_loss_catalog() -> SingularLossCatalog:
    return SingularLossCatalog(
        losses_by_code={
            "ELBOW_90": SingularLoss(
                code="ELBOW_90",
                name="Coude 90",
                zeta=0.7,
            ),
            "TEE_BRANCH": SingularLoss(
                code="TEE_BRANCH",
                name="Té dérivation",
                zeta=1.2,
            ),
        },
        mappings_by_keyword={
            "elbow_90": "ELBOW_90",
            "tee_branch": "TEE_BRANCH",
        },
    )