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


def get_python_projects(data: Dict[str, Dict[str, Any]]) -> Set[str]:
    """Get all projects that have Python code. Create a set of Python project names."""
    codedirs = defaultdict(dict)
    for k, d in data.items():
        if d["code_dirs"]:
            for folder, source_type_dict in d["code_dirs"].items():
                if folder.lower() == d["metadata"]["project_name"].lower():
                    codedirs[d["metadata"]["project_name"]] |= {
                        ("PROJECT_NAME", "py"): source_type_dict["py"], 
                        ("PROJECT_NAME","ipynb"): source_type_dict["ipynb"]
                        }
                else:
                    codedirs[d["metadata"]["project_name"]] |= {
                        (folder, "py"): source_type_dict["py"], 
                        (folder,"ipynb"): source_type_dict["ipynb"]
                        }

    df_codedirs = pd.DataFrame.from_dict(codedirs, orient="index")

    python_projects = set(df_codedirs.index)
    print("Number of Python projects: ", len(python_projects))
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