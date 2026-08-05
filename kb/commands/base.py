import argparse
from abc import ABC, abstractmethod

from kb.config import Config
from kb.services.knowledge_service import KnowledgeService


class BaseCommand(ABC):
    """Abstract base class for all kb subcommands."""

    name: str = ""
    help_text: str = ""

    def __init__(self, service: KnowledgeService, config: Config):
        self.service = service
        self.config = config

    @classmethod
    @abstractmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        """Configures subcommand arguments."""

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """Executes subcommand logic. Returns exit status code (0 for success)."""
