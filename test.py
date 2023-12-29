import pandas as pd
url = "https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z29.html"

df = pd.read_html(url, header=[0,1,2,3])[1].droplevel([0,1], axis=1).dropna(axis=1, how='all').iloc[:,1:]
print(df)