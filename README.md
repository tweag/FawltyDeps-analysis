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

Create `data` directory and copy data from S3 buckets:
- s3://fawltydeps-tweag/pypi_analysis/results_biomed_20240423
- s3://fawltydeps-tweag/pypi_analysis/results_pypi_20240423

We use two datasets: biomedical and top PyPI 2023 repositories. Detailed description TBD.