import os
import subprocess
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("hayabusa-mcp")

HAYABUSA_PATH = os.environ.get("HAYABUSA_PATH", r"C:\Tools\hayabusa\hayabusa-3.10.0-win-x64.exe")

_last_scan = {"path": None}

@mcp.tool()
def scan_evtx(evtx_directory: str, min_level: str = "informational", output_path: str = "hayabusa_output.csv") -> str:
    """
    Scans a directory of Windows Event Log (.evtx) files with Hayabusa and
    returns a CSV timeline of Sigma-based detections.

    Args:
        evtx_directory: Folder containing .evtx files to scan.
        min_level: Minimum severity to include (informational, low, medium, high, critical).
        output_path: Where to write the resulting CSV timeline.
    """
    if not Path(evtx_directory).is_dir():
        return f"Error: {evtx_directory} is not a valid directory."

    cmd = [HAYABUSA_PATH, "csv-timeline", "-d", evtx_directory, "-o", output_path, "-m", min_level, "-w"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL)

    if result.returncode != 0:
        return f"Hayabusa exited with an error:\n{result.stderr[-1500:]}"

    output_file = Path(output_path)
    if not output_file.exists():
        return "Scan ran, but produced no output. Check that evtx_directory has valid .evtx files."

    _last_scan["path"] = str(output_file)
    preview = output_file.read_text(errors="ignore").splitlines()[:50]
    return "Scan complete. First 50 lines:\n" + "\n".join(preview)


@mcp.tool()
def update_hayabusa_rules() -> str:
    """Updates Hayabusa's Sigma detection rules to the latest version."""
    result = subprocess.run([HAYABUSA_PATH, "update-rules"], capture_output=True, text=True, timeout=120)
    return result.stdout or result.stderr


@mcp.resource("hayabusa://last-scan")
def last_scan_results() -> str:
    """Read-only reference to the full CSV timeline from the most recent scan."""
    if not _last_scan["path"]:
        return "No scan has been run yet."
    return Path(_last_scan["path"]).read_text(errors="ignore")


if __name__ == "__main__":
    mcp.run()
