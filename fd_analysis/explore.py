# Module for auxilary functions for data exploration
import pandas as pd
from typing import Tuple, Set

def codedirs_per_filetype (df_codedirs: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

    # How many subcolumns nave both nonzero values, compared to one column having zero value?

    codedirs_py = df_codedirs.xs('py', level=1, axis=1)
    codedirs_ipynb = df_codedirs.xs('ipynb', level=1, axis=1)

    # only_py_df = (codedirs_ipynb == 0) & (codedirs_py > 0)
    # only_ipynb_df = (codedirs_ipynb > 0) & (codedirs_py == 0)
    # both_df = (codedirs_ipynb > 0) & (codedirs_py > 0)

    return codedirs_py, codedirs_ipynb 


def get_dependencies_declaration(project_analysis_result) -> Set[str]:
    """
    Check the project declares dependencies and if yes, what types of parsers are used
    """
    return {dep["parser_choice"] for dep in project_analysis_result if dep.get("deps_count", 0) > 0} 