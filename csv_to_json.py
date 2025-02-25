import pandas as pd

in_file = "X:\\OwenEC\\Projects\\InvoiceAssembly\\assets\\source_data\\24001_InvoiceData.csv"
out_file = "X:\\OwenEC\\Projects\\fastapi\\data\\test_data_1.json"
df = pd.read_csv(in_file)


df.to_json(out_file, orient="records", indent=4)
# print(df)