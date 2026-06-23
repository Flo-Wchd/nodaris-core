from __future__ import annotations

from ndc_core.networks.domestic_water.numeric import (
    positive_optional_float,
    safe_float,
    safe_non_negative_float,
    safe_positive_float,
    safe_pressure_pa,
)


def test_safe_float() -> None:
    assert safe_float("12.5") == 12.5
    assert safe_float(3) == 3.0
    assert safe_float(None) == 0.0
    assert safe_float("bad") == 0.0
    assert safe_float("bad", default=4.0) == 4.0
    assert safe_float(float("nan")) == 0.0
    assert safe_float(float("inf")) == 0.0


def test_safe_positive_float() -> None:
    assert safe_positive_float("12.5") == 12.5
    assert safe_positive_float(0.0) is None
    assert safe_positive_float(-1.0) is None
    assert safe_positive_float(None) is None
    assert safe_positive_float("bad") is None
    assert safe_positive_float(float("nan")) is None
    assert safe_positive_float(float("inf")) is None


def test_positive_optional_float_alias() -> None:
    assert positive_optional_float("18") == 18.0
    assert positive_optional_float(0) is None
    assert positive_optional_float(None) is None


def test_safe_non_negative_float() -> None:
    assert safe_non_negative_float("12.5") == 12.5
    assert safe_non_negative_float(0.0) == 0.0
    assert safe_non_negative_float(-1.0) == 0.0
    assert safe_non_negative_float(None) == 0.0
    assert safe_non_negative_float("bad", default=3.0) == 3.0
    assert safe_non_negative_float(float("nan"), default=3.0) == 3.0
    assert safe_non_negative_float(float("inf"), default=3.0) == 3.0


def test_safe_pressure_pa() -> None:
    assert safe_pressure_pa("300000") == 300000.0
    assert safe_pressure_pa(0.0) == 0.0
    assert safe_pressure_pa(-1.0) == 0.0
    assert safe_pressure_pa(None) == 0.0
    assert safe_pressure_pa("bad") == 0.0
    assert safe_pressure_pa(float("nan")) == 0.0
    assert safe_pressure_pa(float("inf")) == 0.0