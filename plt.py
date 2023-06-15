import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_hist(df, filename = "plt.pdf"):
    pp = PdfPages(filename)
    for col in df.select_dtypes(include="number").columns:
        plt.hist(df[col], bins=10)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        # plt.show()
        pp.savefig(plt.gcf())
        plt.clf()
    pp.close()
