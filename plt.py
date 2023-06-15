import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

df = pd.read_csv("sample_data_2.csv")

pp = PdfPages("plt.pdf")

for col in df.select_dtypes(include="number").columns:
    plt.hist(df[col], bins=10)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    pp.savefig(plt.gcf())
    plt.clf()

pp.close()