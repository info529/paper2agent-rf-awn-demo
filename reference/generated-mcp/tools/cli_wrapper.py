"""Bounded CLI reuse of pinned AWN, with explicit compatibility provenance."""
import hashlib
import json
import os
import platform
from pathlib import Path
import re
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from typing import Annotated, Literal

from fastmcp import FastMCP

cli_wrapper_mcp = FastMCP(name="cli_wrapper")
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "repo" / "AWN"
REVISION = "0b3d2b2d3d5d4761e73eb91e223844b4b8585b53"
REFERENCE = f"https://github.com/zjwfufu/AWN/blob/{REVISION}/main.py"
DATA_FILES = {
    "2016.10a": "RML2016.10a_dict.pkl",
    "2016.10b": "RML2016.10b.dat",
    "2018.01a": "GOLD_XYZ_OSC.0001_1024.hdf5",
}


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _runtime() -> tuple[str, dict]:
    configured = os.environ.get("AWN_PYTHON")
    if not configured:
        raise ValueError(
            "AWN_PYTHON must explicitly identify the verified scientific "
            "Python 3.8 / torch 1.8.1+cpu executable"
        )
    executable = Path(configured).expanduser().resolve()
    if not executable.is_file():
        raise ValueError(f"AWN_PYTHON does not exist: {executable}")
    probe = (
        "import json,sys,torch,importlib.metadata as m; "
        "print(json.dumps({'executable':sys.executable,'python':sys.version,"
        "'python_minor':list(sys.version_info[:2]),'torch':torch.__version__,"
        "'torch_file':torch.__file__,'packages':{p:m.version(p) for p in "
        "['numpy','scipy','scikit-learn','matplotlib','PyYAML','h5py']}}))"
    )
    check = subprocess.run(
        [str(executable), "-c", probe],
        shell=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    identity = json.loads(check.stdout) if check.returncode == 0 else {}
    if (
        identity.get("python_minor") != [3, 8]
        or identity.get("torch") != "1.8.1+cpu"
        or Path(identity.get("executable", "")).resolve() != executable
    ):
        raise ValueError(
            "Incompatible AWN_PYTHON; require Python 3.8 and "
            f"torch 1.8.1+cpu: {identity}; {check.stderr[-1000:]}"
        )
    return str(executable), identity


@cli_wrapper_mcp.tool()
def awn_evaluate_dataset(
    dataset: Annotated[
        Literal["2016.10a", "2016.10b", "2018.01a"],
        "Source-supported RadioML family; only 2016.10a has full-data verification",
    ],
    dataset_path: Annotated[
        str,
        "Authorized local dataset in source native format; "
        "2016 dictionary modulation keys must already be ASCII bytes",
    ],
    checkpoint_path: Annotated[
        str, "Provided pretrained source-compatible AWN checkpoint file"
    ],
    output_dir: Annotated[
        str, "Base output directory for a unique invocation directory"
    ],
    seed: Annotated[
        int, "Source fix_seed parameter controlling the original split"
    ] = 2022,
    device: Annotated[Literal["cpu"], "Verified CPU execution only"] = "cpu",
    timeout_seconds: Annotated[
        int, "Subprocess wall-clock timeout, 1 to 3600 seconds"
    ] = 300,
) -> dict:
    """Evaluate a pretrained AWN on a supported RadioML dataset with the original source CLI."""
    if dataset not in DATA_FILES or device != "cpu":
        raise ValueError("Unsupported dataset or device")
    if not 1 <= timeout_seconds <= 3600:
        raise ValueError("timeout_seconds must be between 1 and 3600")

    inputs = [Path(p).expanduser().resolve() for p in (dataset_path, checkpoint_path)]
    for path in inputs:
        if not path.is_file():
            raise ValueError(f"Required input file does not exist: {path}")

    executable, identity = _runtime()
    base = Path(output_dir).expanduser().resolve()
    base.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="awn-eval-", dir=base))

    for name in ("main.py", "util", "models", "data_loader", "config"):
        (run / name).symlink_to(
            SOURCE / name, target_is_directory=(SOURCE / name).is_dir()
        )
    for name in ("data", "checkpoint"):
        (run / name).mkdir()

    (run / "data" / DATA_FILES[dataset]).symlink_to(inputs[0])
    (run / "checkpoint" / f"{dataset}_AWN.pkl").symlink_to(inputs[1])

    command = [
        executable,
        "main.py",
        "--mode",
        "eval",
        "--dataset",
        dataset,
        "--device",
        device,
        "--seed",
        str(seed),
        "--ckpt_path",
        "./checkpoint",
    ]

    environment = os.environ.copy()
    environment.update(
        {"OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "MPLBACKEND": "Agg"}
    )

    record = {
        "classification": "SOURCE + COMPATIBILITY REPAIR + CLI WRAPPER",
        "source_revision": REVISION,
        "command": command,
        "cwd": str(run),
        "start_utc": datetime.now(timezone.utc).isoformat(),
        "os_architecture": platform.platform(),
        "runtime_identity": identity,
        "configuration_sha256": _hash(SOURCE / "config" / f"{dataset}.yml"),
        "main_sha256": _hash(SOURCE / "main.py"),
        "inputs": [
            {"path": str(p), "size_bytes": p.stat().st_size, "sha256": _hash(p)}
            for p in inputs
        ],
        "seed": seed,
        "device": device,
        "compatibility_repairs": [
            "External RadioML Python str -> ASCII bytes key normalization "
            "required for 2016 dictionary inputs; arrays unchanged",
            "Source eval torch.load uses map_location=cfg.device",
        ],
        "limitations": [
            "Source equal-block split assumptions and missing-class "
            "confusion-matrix failures preserved",
            "Other dataset families source-supported but not full-data verified",
            "Metrics parsed at source log precision; wrapper does not recompute "
            "metrics or predictions",
        ],
    }

    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=run,
            env=environment,
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        stdout, stderr, exit_status = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr = error.stdout or b"", error.stderr or b""
        stdout = stdout.decode(errors="replace") if isinstance(stdout, bytes) else stdout
        stderr = stderr.decode(errors="replace") if isinstance(stderr, bytes) else stderr
        record.update(
            {
                "end_utc": datetime.now(timezone.utc).isoformat(),
                "runtime_seconds": time.monotonic() - started,
                "exit_status": None,
                "timed_out": True,
            }
        )
        (run / "stdout.txt").write_text(stdout)
        (run / "stderr.txt").write_text(stderr)
        (run / "provenance.json").write_text(json.dumps(record, indent=2))
        raise RuntimeError(
            f"AWN timed out after {timeout_seconds} seconds; "
            f"provenance: {run / 'provenance.json'}"
        )

    record.update(
        {
            "end_utc": datetime.now(timezone.utc).isoformat(),
            "runtime_seconds": time.monotonic() - started,
            "exit_status": exit_status,
            "timed_out": False,
        }
    )
    (run / "stdout.txt").write_text(stdout)
    (run / "stderr.txt").write_text(stderr)

    artifacts = [
        p
        for p in run.rglob("*")
        if p.is_file()
        and not p.is_symlink()
        and (p.suffix == ".svg" or p.name in ("log.txt", "stdout.txt", "stderr.txt"))
    ]
    record["artifacts"] = [
        {"path": str(p), "sha256": _hash(p), "size_bytes": p.stat().st_size}
        for p in sorted(artifacts)
    ]
    (run / "provenance.json").write_text(json.dumps(record, indent=2))

    if exit_status != 0:
        raise RuntimeError(
            f"AWN exited with status {exit_status}; "
            f"provenance: {run / 'provenance.json'}; stderr: {stderr[-2000:]}"
        )

    logs = list((run / "inference").glob("*/log/log.txt"))
    if len(logs) != 1:
        raise RuntimeError(
            f"AWN did not produce exactly one source log; "
            f"provenance: {run / 'provenance.json'}"
        )

    log = logs[0].read_text()
    metrics = {}
    for key, label in {
        "overall_accuracy": "overall accuracy is",
        "macro_f1": "macro F1-score is",
        "cohens_kappa": "kappa coefficient is",
    }.items():
        match = re.search(re.escape(label) + r":\s*([0-9.eE+-]+)", log)
        if not match:
            raise RuntimeError(f"Missing source metric {key}; log: {logs[0]}")
        metrics[key] = float(match.group(1))

    return {
        "message": "Original AWN CPU evaluation completed",
        "reference": REFERENCE,
        "metrics": metrics,
        "runtime_seconds": record["runtime_seconds"],
        "output_directory": str(run),
        "settings": {"dataset": dataset, "seed": seed, "device": device},
        "artifacts": [
            {"description": "Source figure or execution log", "path": str(p)}
            for p in sorted(artifacts)
        ]
        + [
            {
                "description": "Execution and explicit compatibility provenance",
                "path": str(run / "provenance.json"),
            }
        ],
        "limitations": record["limitations"],
    }
