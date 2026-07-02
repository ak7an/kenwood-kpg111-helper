"""OpenKPG application scaffold for KPG111 helper workflows."""

from importlib import import_module
from typing import Any

_BUILDER_EXPORTS = {
    "BuildLimits",
    "BuildProject",
    "BuildRequest",
    "BuildResult",
    "BuildStatistics",
    "ValidationIssue",
}

__all__ = [*_BUILDER_EXPORTS, "__version__"]

__version__ = "0.1.0"


def __getattr__(name: str) -> Any:
    if name in _BUILDER_EXPORTS:
        module = import_module(".project_builder", __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
