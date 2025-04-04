import pandas as pd
from src.using_parameters_instead.formula import DesignMatrixFactory

def interaction_term(x):
    if ":" in x:
        return x.split(":")[1]
    elif x=="alpha":
        return "alpha"
    else:
        return "group"

class ModelResultSummarizer:

    def __init__(self, design_matrix_factory: DesignMatrixFactory):
        self.design_matrix_factory = design_matrix_factory

    @property
    def dependent_variable(self):
        self.design_matrix_factory.dependent_variable

    @property
    def interaction_terms(self):
        self.design_matrix_factory.independent_variables

    def summary_dataframe(self, results_dictionary, covariate: str = None):
        df = pd.DataFrame({
            feature: model.params
            for feature, model in results_dictionary.items()
        }).reset_index()

        df = self.extract_coefficients_table(df, covariate)

        return df

    def extract_coefficients_table(self, df: pd.DataFrame, covariate: str = None):

        # Specimens
        df["specimen"] = df["index"] \
            .str.split(":").apply(lambda x: x[0]) \
            .str.split("[").apply(lambda x: x[-1]).str.rstrip("]")

        # Interactions
        if covariate:
            df = df.query("index.str.endswith(@covariate)")
            df["interaction_term"] = df["index"] \
                .str.split(":") \
                .apply(lambda x: x[1])
        else:
            # HACK: Fix me please.
            df = df.query("index.str.contains('\[') & ~index.str.contains(':')")
            # return df

        return df.set_index("index")

    def expected_term_variance(self, results_dictionary, covariate: str = None):
        df = pd.DataFrame({
            feature: model.bse
            for feature, model in results_dictionary.items()
        }).reset_index()

        df = self.extract_coefficients_table(df, covariate)

        return df

