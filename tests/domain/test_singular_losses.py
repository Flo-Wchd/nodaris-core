from ndc_core.domain.singular_losses import SingularLoss, SingularLossMethod


def test_singular_loss_normalizes_values() -> None:
    loss = SingularLoss(
        code=" elbow_90 ",
        name=" Coude 90 ",
        method=SingularLossMethod.ZETA,
        zeta=0.7,
        quantity=2,
    )

    assert loss.code == "elbow_90"
    assert loss.name == "Coude 90"
    assert loss.method is SingularLossMethod.ZETA
    assert loss.zeta == 0.7
    assert loss.quantity == 2


def test_singular_loss_negative_values_are_clamped() -> None:
    loss = SingularLoss(
        code="invalid",
        name="Invalid",
        zeta=-1.0,
        kv=-2.0,
        quantity=-3,
    )

    assert loss.zeta == 0.0
    assert loss.kv == 0.0
    assert loss.quantity == 0
    assert not loss.is_active


def test_singular_loss_method_helpers() -> None:
    zeta_loss = SingularLoss(
        code="zeta",
        name="Zeta",
        method=SingularLossMethod.ZETA,
    )
    kv_loss = SingularLoss(
        code="kv",
        name="Kv",
        method=SingularLossMethod.KV,
    )

    assert zeta_loss.is_zeta_based
    assert not zeta_loss.is_kv_based

    assert kv_loss.is_kv_based
    assert not kv_loss.is_zeta_based