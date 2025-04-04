import patsy
import pandas as pd
import anndata as ad

class DesignMatrixFactory:

    def __init__(self, specimen_field: str, covariate_fields: list[str], additional_terms: list[str] = [], intercept: bool = True):
        self.intercept = intercept
        self._specimen_field = specimen_field
        self._covariate_fields = covariate_fields
        self._additional_terms = additional_terms
        self.formula = self.construct_formula(specimen_field, covariate_fields)
    
    @property
    def dependent_variable(self) -> str:
        # FIXME: Should this be updatable?
        return "expression"

    @property
    def independent_variables(self) -> list[str]:
        return [x.name() for x in patsy.ModelDesc.from_formula(self.formula).rhs_termlist]

    def construct_formula(self, specimen_field: str, covariate_fields: list[str]) -> str:
        if self.intercept:
            intercept = "1"
        else:
            intercept = "0"

        formula =  f"expression ~ {intercept} + {specimen_field} + " + \
            " + ".join([f"{specimen_field}:{covariate}" for covariate in covariate_fields])
        
        if len(self._additional_terms):
            formula += " + ".join(self._additional_terms)
        
        return formula

    def apply_formula(self, adata: ad.AnnData, feature: str, layer=None, return_type="dataframe"):
        if type(layer) == str:
            return patsy.dmatrices(
                self.formula,
                adata.obs.assign(expression = adata[:, feature].layers[layer].reshape(-1).tolist()),
                return_type="dataframe"
            )
        if type(layer) == None:
            return patsy.dmatrices(
                self.formula,
                adata.obs.assign(expression = adata[:, feature].layers[layer].reshape(-1).tolist()),
                return_type="dataframe"
            )