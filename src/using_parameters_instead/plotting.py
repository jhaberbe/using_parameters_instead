import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text

def volcano_plot(df, lfc_threshold=1, pvalue_threshold=0.05, top_n_genes=15, fig_size = (7, 5)):
    """
    Generates a volcano plot from a DataFrame.

    Args:
        df: DataFrame with 'logFC', '-log10p', and feature names in the index.
        lfc_threshold: Log fold change threshold for significance lines.
        pvalue_threshold: p-value threshold for significance lines.
        top_n_genes: Number of top genes to label.
    """

    df["color"] = "grey"
    df.loc[(df["pvalue"].lt(pvalue_threshold) & df["logFC"].gt(lfc_threshold)), "color"] = "red"
    df.loc[(df["pvalue"].lt(pvalue_threshold) & df["logFC"].lt(-lfc_threshold)), "color"] = "blue"

    plt.figure(figsize=fig_size)
    plt.scatter(df['logFC'], df['-log10p'], 
                c=df["color"],
                alpha=0.7)
    
    # Significance lines
    plt.axvline(x=lfc_threshold, color='gray', linestyle='--')
    plt.axvline(x=-lfc_threshold, color='gray', linestyle='--')
    plt.axhline(y=-np.log10(pvalue_threshold), color='gray', linestyle='--')

    # Label top N genes
    texts = []
    for index, row in df.sort_values('-log10p', ascending=False).head(top_n_genes).iterrows():
        texts.append(plt.text(row['logFC'], row['-log10p'], index))

    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black', lw=0.5))

    plt.xlabel('logFC')
    plt.ylabel('-log10p(p-value)')
