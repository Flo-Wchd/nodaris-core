from ndc_core.catalogs.singular_loss_catalog import SingularLossCatalog
from ndc_core.domain.singular_losses import SingularLossMethod


def test_singular_loss_catalog_from_mapping() -> None:
    result = SingularLossCatalog.from_mapping(
        {
            "k_catalog": {
                "elbows": {
                    "family": "elbow",
                    "items": [
                        {
                            "id": "elbow_90_standard",
                            "label": "Coude 90 standard",
                            "k": 1.7,
                        }
                    ],
                }
            },
            "kv_catalog": {
                "ball_valves": {
                    "family": "ball_valve",
                    "items": [
                        {
                            "id": "ball_valve",
                            "label": "Vanne à bille",
                            "dn_kv": {"DN15": 70, "DN20": 190},
                        }
                    ],
                }
            },
            "mappings": {
                "by_keywords": {
                    "coude 90": "elbow_90_standard",
                    "vanne-bille": "ball_valve",
                }
            },
        }
    )

    assert result.ok
    assert result.value is not None

    catalog = result.value

    elbow = catalog.get("coude_90")
    valve = catalog.get("vanne bille")

    assert elbow is not None
    assert elbow.method is SingularLossMethod.ZETA
    assert elbow.zeta == 1.7

    assert valve is not None
    assert valve.method is SingularLossMethod.KV
    assert valve.kv == 190


def test_singular_loss_catalog_resolve_loss_code() -> None:
    result = SingularLossCatalog.from_mapping(
        {
            "k_catalog": {
                "elbows": {
                    "items": [
                        {
                            "id": "elbow_45_standard",
                            "label": "Coude 45",
                            "k": 0.8,
                        }
                    ],
                }
            },
            "mappings": {"by_keywords": {"coude_45": "elbow_45_standard"}},
        }
    )

    assert result.value is not None
    assert result.value.resolve_loss_code("coude 45") == "elbow_45_standard"


def test_singular_loss_catalog_invalid_k_catalog_adds_warning() -> None:
    result = SingularLossCatalog.from_mapping({"k_catalog": []})

    assert result.ok
    assert result.value is not None
    assert result.value.messages[0].code == "SINGULAR_K_CATALOG_INVALID"