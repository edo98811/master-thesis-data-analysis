import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd

pd.



a = random.sample(range(100000, 999999), 10)
b = random.sample(range(100000, 999999), 10)

fig, axs = plt.subplots(2, 2, figsize=(20, 10))
ax = axs[1, 1]
ax.scatter(a, b)
md = np.mean(a)
sd = np.std(a, axis=0)
ax.axhline(md, color='gray', linestyle='--')
ax.axhline(md + 1.96 * sd, color='gray', linestyle='--')
ax.axhline(md - 1.96 * sd, color='gray', linestyle='--')
ax.set_xlabel('Mean')
ax.set_ylabel('Difference')
ax.set_title("provissima")  # query.split("=")[-1])
ax.legend(['Mean difference', '95% limits of agreement'])
ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0), useMathText=True)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
# ax.tick_params(axis='both', which='major', labelsize=20)

plt.show()
