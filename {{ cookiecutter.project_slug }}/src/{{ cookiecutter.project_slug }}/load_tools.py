import importlib
import os
from pathlib import Path
from typing import get_type_hints

import yaml  # type: ignore[import-untyped]
from fastmcp.tools.tool import Tool


def import_handler(handler_path: str):
    """
    Recibe un string tipo 'package.module.func' y devuelve la función
    junto con sus parámetros y tipos.
    """
    module_path, func_name = handler_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    func = getattr(module, func_name)

    # Inferir tipos de salida si hay type hints
    output_schema = get_type_hints(func).get("return", None)

    return func, output_schema


TOOLS_DIR = Path(os.getenv("TOOLS_DIR", "tools"))


def load_tools():
    tools = []
    for file in TOOLS_DIR.glob("*.yml"):
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            for t in data.get("tools", []):
                handler_func, output_schema = import_handler(t["handler"])
                tool = Tool.from_function(
                    name=t["name"],
                    description=t.get("description", ""),
                    output_schema=output_schema,
                    fn=handler_func,
                    tags=set(t.get("tags", [])),
                )
                tools.append(tool)
    return tools
