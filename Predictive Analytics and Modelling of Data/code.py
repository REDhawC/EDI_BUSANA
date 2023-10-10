Series_1 = [9, 2, 1, 10, 5, 2, 2, 8, 6, 2]
Series_2 = [8, 8, 1, 1, 2, 2, 2, 1, 1, 8]

import pandas as pd

Series_1.sort()
Series_2.sort()

pd = pd.DataFrame({"Series_1": Series_1, "Series_2": Series_2})
print(pd["Series_1"].median())
print(pd["Series_2"].median())
print(pd["Series_1"].mean())
print(pd["Series_2"].mean())
print(pd["Series_1"].std())
print(pd["Series_2"].std())
print(pd["Series_1"].quantile(0.75) - pd["Series_1"].quantile(0.25))
print(pd["Series_2"].quantile(0.75) - pd["Series_2"].quantile(0.25))
