# Analysis of Python projects

Analysis of Python repositories with use of FawltyDeps [experiments branch](https://github.com/tweag/FawltyDeps/tree/zhihan/PyPI-analyis-download-and-analyze/PyPI_analysis).

Data format (example):
```
{
    "project_name": "ProjectName",
    "code_dirs": {
        "scripts": {
            "py": 29,
            "ipynb": 0,
            "total": 29
        }, 
        "notebooks": {
            "py": 0,
            "ipynb": 12,
            "total": 12
        }
    },
    "deps_file": [        
        {
            "source_type": "DepsSource",
            "path": "requirements.txt",
            "parser_choice": "requirements.txt",
            "deps_count": 4,
            "warnings": false
        }],
    "imports": [
        {
            "Docstring": {
                "name": "anndata",
                "source": {
                    "path": "scvi/autotune/_tuner.py",
                    "lineno": 8
                }
            }
        }
    ],
    "fawltydeps_version": "0.13.1"
}
```

## Data

Collect data from [Zhihan's experiment](https://github.com/tweag/FawltyDeps/tree/zhihan/PyPI-analyis-download-and-analyze/PyPI_analysis/experiments/biomedical_projects_experiment/results).

Dorran's data may be found on [Tweag Google Drive](https://drive.google.com/drive/folders/1Umd6GHW64iq-AG-CDjxoHG2TpOfS4xkF?usp=drive_link).