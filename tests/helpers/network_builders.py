from __future__ import annotations

from ndc_core.domain.networks.cell import Cell
from ndc_core.domain.networks.network import Network
from ndc_core.domain.networks.node import Node
from ndc_core.domain.networks.section import Section
from ndc_core.domain.networks.types import NodeKind, SectionUsageContext
from ndc_core.domain.singular_losses import SingularLoss


def domestic_water_branching_network() -> Network:
    """
    Mixed EFS/ECS reference network.

    Topology:

        N0 source
        ├── S_EFS_MAIN → N_EFS_SPLIT
        │   ├── S_EFS_A → N_EFS_A → Cell A cold
        │   └── S_EFS_B → N_EFS_B → Cell B cold
        └── S_ECS_MAIN → N_ECS_SPLIT
            ├── S_ECS_A → N_ECS_A → Cell A hot
            └── S_ECS_B → N_ECS_B → Cell B hot
    """

    network = Network(id="N_REF", name="Domestic water branching reference")

    nodes = [
        Node(id="N0", name="Source", kind=NodeKind.SOURCE),
        Node(id="N_EFS_SPLIT", name="EFS split", kind=NodeKind.JUNCTION),
        Node(id="N_EFS_A", name="EFS terminal A", kind=NodeKind.TERMINAL),
        Node(id="N_EFS_B", name="EFS terminal B", kind=NodeKind.TERMINAL),
        Node(id="N_ECS_SPLIT", name="ECS split", kind=NodeKind.JUNCTION),
        Node(id="N_ECS_A", name="ECS terminal A", kind=NodeKind.TERMINAL),
        Node(id="N_ECS_B", name="ECS terminal B", kind=NodeKind.TERMINAL),
    ]

    for node in nodes:
        network.add_node(node)

    cells = [
        Cell(
            id="C_EFS_A",
            name="Cold dwelling A",
            appliance_counts={
                "L": 1,
                "D": 1,
                "WC": 1,
            },
        ),
        Cell(
            id="C_EFS_B",
            name="Cold dwelling B",
            appliance_counts={
                "L": 1,
                "E": 1,
                "WC": 1,
                "LL": 1,
                "LV": 1,
            },
        ),
        Cell(
            id="C_ECS_A",
            name="Hot dwelling A",
            appliance_counts={
                "L": 1,
                "D": 1,
            },
        ),
        Cell(
            id="C_ECS_B",
            name="Hot dwelling B",
            appliance_counts={
                "L": 1,
                "E": 1,
                "D": 1,
            },
        ),
    ]

    for cell in cells:
        network.add_cell(cell)

    sections = [
        Section(
            id="S_EFS_MAIN",
            name="EFS main",
            upstream_node_id="N0",
            downstream_node_id="N_EFS_SPLIT",
            fluid_code="EFS",
            usage_context=SectionUsageContext.BASEMENT,
            length_m=18.0,
            elevation_change_m=2.0,
            forced_pipe_size_code="EFS26",
        ),
        Section(
            id="S_EFS_A",
            name="EFS dwelling A",
            upstream_node_id="N_EFS_SPLIT",
            downstream_node_id="N_EFS_A",
            fluid_code="EFS",
            usage_context=SectionUsageContext.DWELLING,
            length_m=8.0,
            elevation_change_m=1.0,
        ),
        Section(
            id="S_EFS_B",
            name="EFS dwelling B",
            upstream_node_id="N_EFS_SPLIT",
            downstream_node_id="N_EFS_B",
            fluid_code="EFS",
            usage_context=SectionUsageContext.DWELLING,
            length_m=14.0,
            elevation_change_m=4.0,
        ),
        Section(
            id="S_ECS_MAIN",
            name="ECS main",
            upstream_node_id="N0",
            downstream_node_id="N_ECS_SPLIT",
            fluid_code="ECS",
            usage_context=SectionUsageContext.BASEMENT,
            length_m=16.0,
            elevation_change_m=2.0,
            forced_pipe_size_code="ECS26",
        ),
        Section(
            id="S_ECS_A",
            name="ECS dwelling A",
            upstream_node_id="N_ECS_SPLIT",
            downstream_node_id="N_ECS_A",
            fluid_code="ECS",
            usage_context=SectionUsageContext.DWELLING,
            length_m=8.0,
            elevation_change_m=1.0,
        ),
        Section(
            id="S_ECS_B",
            name="ECS dwelling B",
            upstream_node_id="N_ECS_SPLIT",
            downstream_node_id="N_ECS_B",
            fluid_code="ECS",
            usage_context=SectionUsageContext.DWELLING,
            length_m=15.0,
            elevation_change_m=4.5,
        ),
    ]

    for section in sections:
        section.add_singular_loss(
            SingularLoss(
                code="ELBOW_90",
                name="Coude 90",
                quantity=2,
                zeta=0.7,
            )
        )
        network.add_section(section)

    network.attach_cell_to_node("C_EFS_A", "N_EFS_A")
    network.attach_cell_to_node("C_EFS_B", "N_EFS_B")
    network.attach_cell_to_node("C_ECS_A", "N_ECS_A")
    network.attach_cell_to_node("C_ECS_B", "N_ECS_B")

    return network