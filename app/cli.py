import subprocess
import sys
from pathlib import Path

import uvicorn

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def dev() -> None:
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


def prod() -> None:
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


def docker_build() -> None:
    sys.exit(subprocess.run(["docker", "build", "-t", "fastapi-app", "."]).returncode)


def docker_up() -> None:
    sys.exit(
        subprocess.run(
            ["docker", "compose", "up", "--build", "-d"],
            cwd=_PROJECT_ROOT,
        ).returncode
    )
