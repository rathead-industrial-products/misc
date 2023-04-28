# Creating a Figure and Axes
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x = [1, 2, 3, 4, 5, 6, 7]
y = [10, 23, 45, 33, 22, 45, 55]

ax.plot(x, y)
plt.show()

import pandas as pd

df = pd.DataFrame.from_dict({
    'Year': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'Computer Sales': [12500, 13000, 13500, 15000, 14000, 16000, 17000, 18000, 16500, 17000, 19000],
    'TV Sales': [13000, 20000, 18000, 19000, 19500, 21000, 23000, 24000, 22000, 22500, 25000]
})

print(df.head())