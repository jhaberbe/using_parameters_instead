import tqdm
import scipy.stats
import numpy as np
import pandas as pd

class CoefficientStatistics:

    def __init__(self, df: pd.DataFrame, groupby: str = "group"):
        self.tables = {
            g: t for g, t in df.groupby(groupby)
        }

    def generate_stats_entry_dict(self, control_group: str, treatment_group: str, feature: str, **kwargs):
        test_result = self.generate_stats_entry(control_group, treatment_group, feature, **kwargs)

        return {
            "logFC": np.mean(self.tables[treatment_group][feature]) - np.mean(self.tables[control_group][feature]),
            "control_group_mean": np.mean(self.tables[control_group][feature]),
            "treatment_group_mean": np.mean(self.tables[treatment_group][feature]),
            "pvalue": test_result.pvalue,
            "-log10p": -np.log10(test_result.pvalue),
            "statistic": test_result.statistic,
        }

    def generate_stats_entry(self, control_group: str, treatment_group: str, feature: str, **kwargs):
        test_result = scipy.stats.ttest_ind(
            self.tables[treatment_group][feature],
            self.tables[control_group][feature],
            **kwargs
        )

        return test_result

