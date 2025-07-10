from pathlib import Path

from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.lakebridge import cli


from databricks.labs.bladespector.analyzer import Analyzer


INPUT_PATH = Path(__file__).parent.parent / "resources" / "functional" / "informatica"
SUPPORTED_TECH = sorted(Analyzer.supported_source_technologies(), key=str.casefold)
TECH_ENUM = next((i for i, tech in enumerate(SUPPORTED_TECH) if tech == "Informatica - PC"), 12)


def test_analyze(mock_workspace_client):
    prompts = MockPrompts(
        {
            "Select the source technology": TECH_ENUM,
            "Enter full path to the source directory": INPUT_PATH,
            "Enter report filename": "",
        }
    )
    cli.analyze(mock_workspace_client, prompts)

    expected_filename = "lakebridge-analyzer-results.xlsx"
    created_file = list(INPUT_PATH.glob(expected_filename))
    assert any(f.name == expected_filename for f in created_file)
    if created_file:
        created_file[0].unlink()
