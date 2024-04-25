# Preparation of the data for the analysis

from collections import defaultdict
import json
from pathlib import Path
from typing import List, Dict, Any, Set
import pandas as pd


def filter_corrupt_files(paths: List[Path]) -> (List[Dict[str, Any]], List[str]):
    """
    Filter out files that are not valid json files
    """
    data = {}
    corrupt_files = []
    for path in paths:
        try:
            with open(path, "r") as f:
                single_result = json.load(f)
            data[path.name] = single_result
        except json.decoder.JSONDecodeError:
            corrupt_files.append(path.name)
    return data, corrupt_files

def exctract_code_directories(codedir: Dict[str, Dict[str, Any]], project_name: str) -> Dict[str, Dict[str, Any]]:
    """Exctract code directories and sum up the number of files in each directory."""
    code_dirs = defaultdict(int)
    for folder, source_type_dict in codedir.items():
        if folder.lower() == project_name.lower():
            code_dirs |= {
                ("PROJECT_NAME", "py"): source_type_dict["py"], 
                ("PROJECT_NAME","ipynb"): source_type_dict["ipynb"]
                }
        else:
            code_dirs |= {
                (folder, "py"): source_type_dict["py"], 
                (folder,"ipynb"): source_type_dict["ipynb"]
                }
    return code_dirs


def get_python_projects(data: Dict[str, Dict[str, Any]]) -> Set[str]:
    """Get all projects that have Python code. Create a set of Python project names."""
    codedirs = defaultdict(dict)
    for k, d in data.items():
        project_name = d["metadata"]["project_name"]
        # There should be .py or .ipynb files in the code_dirs
        # If there are only .ipynb files and no imports, then
        # it is most likely an R project
        # There are some projects written in Python 2.X,
        # example: https://github.com/mattloose/RUFigs
        # For those, FawltyDeps does not work and the results are not reliable.
        # We assume that all Python projects have 3-rd party imports.
        if d["code_dirs"] and d["imports"]:
            code_dirs = exctract_code_directories(d["code_dirs"], project_name)
            codedirs[project_name] = code_dirs


    df_codedirs = pd.DataFrame.from_dict(codedirs, orient="index")

    python_projects = set(df_codedirs.index)
    return python_projects

def get_depsfiles(data) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all dependencies files for Python projects.
    Create a dictionary with project names as keys and dependencies files as values.
    """
    python_data = get_python_projects(data)
    depsfiles = defaultdict(list)
    for d in data.values():
        if d["metadata"]["project_name"] in python_data:
            if d["deps_file"]:
                depsfiles[d["metadata"]["project_name"]] = d["deps_file"]

    print(len(depsfiles))
    return depsfiles

def get_parser_choices(depsfiles):
    """Find all parser choices where deps_count > 0"""
    parser_choices = defaultdict(dict)
    for k, dd in depsfiles.items():
        _pc = defaultdict(int)
        for d in dd:
            if d["deps_count"] > 0:
                _pc[d["parser_choice"]] += d["deps_count"]
        parser_choices[k] = _pc
    return parser_choices


def reduce_directory_levels(code_dirs: Dict[str, Any], deps_file: Dict[str, Any], level: int = 2) -> Dict[str, Any]:
    """
    Reduce the directory levels of code_dirs to `level` number of levels.
    Sums all the values of the same key.
    Also, remove setup.py files from the count
    """
    reduced_dirs = defaultdict(lambda: {"py": 0, "ipynb": 0, "total": 0})
    for k, v in code_dirs.items():
        reduced_dirs["/".join(k.split("/")[:level])]["py"] += v["py"]
        reduced_dirs["/".join(k.split("/")[:level])]["ipynb"] += v["ipynb"]
        reduced_dirs["/".join(k.split("/")[:level])]["total"] += v["total"]

    for k in deps_file:
        if k["parser_choice"] == "setup.py":
            setup_path = k["path"].split("/")[:-1]
            index = "/".join(["."] if not setup_path else setup_path[:level])
            reduced_dirs[index]["py"] -= 1
            reduced_dirs[index]["total"] -= 1

    return reduced_dirs