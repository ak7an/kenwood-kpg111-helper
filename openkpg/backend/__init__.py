"""Backend adapters that connect OpenKPG to the read-only kpg111 library."""

from .project_backend import OpenKPGProjectBackend

__all__ = ["OpenKPGProjectBackend"]
