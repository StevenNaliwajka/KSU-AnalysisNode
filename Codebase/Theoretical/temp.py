import pandas as pd
file = r"C:\Users\steve\PycharmProjects\KSU-AnalysisNode\Data\Train\TVWS\TVWSdirt_0_2025-06-06_11-04-00.csv"
df = pd.read_csv(file)
print(df.columns)
print(df.head())