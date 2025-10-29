"""Smoke tests to verify basic import functionality."""


def test_import_src():
    """Verify src package can be imported."""
    import src

    assert hasattr(src, "__version__")


def test_import_agents():
    """Verify agents subpackage can be imported."""
    from src import agents

    assert agents is not None


def test_import_orchestration():
    """Verify orchestration subpackage can be imported."""
    from src import orchestration

    assert orchestration is not None


def test_import_predictive():
    """Verify predictive subpackage can be imported."""
    from src import predictive

    assert predictive is not None


def test_import_integrations():
    """Verify integrations subpackage can be imported."""
    from src import integrations

    assert integrations is not None


def test_import_utils():
    """Verify utils subpackage can be imported."""
    from src import utils

    assert utils is not None
