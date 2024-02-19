import pandas as pd
import os
files = [file for file in os.listdir() if file.endswith('.csv')]

df = pd.concat([pd.read_csv(file) for file in files])


pd.DataFrame(df['make'].unique()).to_clipboard()
pd.DataFrame(df['body_styles'].unique()).to_clipboard()


import ast
# Convert string representations to actual lists
nested_lists = [ast.literal_eval(item) for item in list(df['body_styles'].unique()) ]

# Flatten the list of lists
flattened_list = [item for sublist in nested_lists for item in sublist]

print(flattened_list)

flattened_list = set(flattened_list)

pd.DataFrame(flattened_list).to_clipboard()

df.groupby(['body_styles']).sum().reset_index().to_clipboard()

df.to_csv("cars.csv", index=False)