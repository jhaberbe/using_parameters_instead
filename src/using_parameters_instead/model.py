"""Main module."""

from IPython.display import clear_output
import pandas as pd
from tqdm import tqdm
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.discrete.discrete_model as discrete_model

from src.using_parameters_instead.formula import DesignMatrixFactory


class GeneralizedLinearModelFitter:

    def __init__(self, family: sm.families):
        self.family = family

    def fit_model(self, endog, exog, **kwargs):
        model = sm.GLM(
            endog, 
            exog, 
            family=self.family, 
            **kwargs
        ).fit()
        return model


class NegativeBinomialModelFitter(GeneralizedLinearModelFitter):

    def __init__(self):
        pass  # no family needed here

    def fit_model(self, endog, exog, **kwargs):
        model = discrete_model.NegativeBinomial(
            endog, 
            exog, 
            **kwargs
        ).fit()
        return model


class DifferentialExpressionTesting:

    def __init__(self, model: GeneralizedLinearModelFitter, design_matrix_factory: DesignMatrixFactory):
        self.results = {}
        self.model = model
        self.design_matrix_factory = design_matrix_factory

    def fit_model_over_features(self, adata, min_expression = 0.05, reset = False, layer = "counts", **kwargs):
        # Not sure if this is good default behavior.
        if reset:
            self.results = {}

        for feature in tqdm(adata.var_names):
            try:
                if layer == None:
                    if (adata[:, feature].X > 0).mean() > min_expression:
                        endog, exog = self.design_matrix_factory.apply_formula(adata, feature)
                        self.results[feature] = self.model.fit_model(endog, exog, **kwargs)

                if type(layer) == str:
                    if (adata[:, feature].layers[layer] > 0).mean() > min_expression:
                        endog, exog = self.design_matrix_factory.apply_formula(adata, feature, layer=layer)
                        self.results[feature] = self.model.fit_model(endog, exog, **kwargs)
            except:
                pass
            clear_output()

        return self.results