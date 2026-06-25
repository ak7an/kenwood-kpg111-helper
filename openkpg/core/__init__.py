"""Core application model and workflow state for OpenKPG."""

from .project import OpenKPGProject
from .recent import RecentProject, RecentProjects
from .workspace import Workspace

__all__ = ["OpenKPGProject", "RecentProject", "RecentProjects", "Workspace"]
