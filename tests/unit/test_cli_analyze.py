from pathlib import Path
from unittest.mock import patch

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.lakebridge import cli

from databricks.labs.lakebridge.contexts.application import ApplicationContext


from databricks.labs.bladespector.analyzer import Analyzer


def test_analyze(mock_workspace_client, tmp_path: Path):

    supported_tech = sorted(Analyzer.supported_source_technologies(), key=str.casefold)
    tech_enum = next((i for i, tech in enumerate(supported_tech) if tech == "Informatica - PC"), 12)

    source_dir = Path(__file__).parent.parent / "resources" / "functional" / "informatica"
    output_dir = tmp_path / "results"

    mock_prompts = MockPrompts(
        {
            "Select the source technology": str(tech_enum),
            "Enter full path to the source directory": str(source_dir),
            "Enter report file name or custom export path including file name without extension": str(output_dir),
        }
    )
    with patch.object(ApplicationContext, "prompts", mock_prompts):
        cli.analyze(mock_workspace_client)
