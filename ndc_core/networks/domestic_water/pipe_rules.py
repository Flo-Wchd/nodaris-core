from __future__ import annotations

from ndc_core.catalogs.pipe_catalog import PipeCatalog
from ndc_core.domain.networks.section import Section
from ndc_core.hydraulics.friction import relative_roughness
from ndc_core.networks.domestic_water.entity_access import clean_optional_code


def relative_roughness_for_section(
    *,
    section: Section,
    pipe_catalog: PipeCatalog | None,
    internal_diameter_m: float,
) -> float:
    """
    Resolve the relative roughness for a Section-like pipe.

    Missing catalog, missing selected pipe, unknown pipe size or unknown material
    return 0.0 instead of failing. This keeps the pressure-loss engine usable in
    degraded mode and avoids blocking GUI workflows.
    """

    if pipe_catalog is None:
        return 0.0

    pipe_code = clean_optional_code(section.selected_pipe_size_code)
    if pipe_code is None:
        return 0.0

    pipe_size = pipe_catalog.get_size(pipe_code)
    if pipe_size is None:
        return 0.0

    material = pipe_catalog.materials_by_code.get(pipe_size.material_code)
    if material is None:
        return 0.0

    roughness_m = getattr(material, "default_roughness_m", 0.0)

    return relative_roughness(
        roughness_m=roughness_m,
        internal_diameter_m=internal_diameter_m,
    )