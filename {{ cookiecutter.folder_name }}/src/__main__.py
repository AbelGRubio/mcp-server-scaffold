import os

from {{ cookiecutter.project_slug }}.server import mcp


def run_mcp():
    if os.getenv("RUN_MAIN", "false") == "true":
        mcp.run(
            transport="stdio",
        )
    else:
        mcp.run(
            transport="streamable-http",
            host="localhost",
            port=8000,
        )


if __name__ == "__main__":
    run_mcp()
