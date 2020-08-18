from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro
import pandas as pd

# seed the random number generator
seed(1)
# generate univariate observations
data = 5 * randn(100) + 50
datax = {'A':  data}
df = pd.DataFrame (datax, columns = ['A'])


# normality test
stat, p = shapiro(df['A'].values)



print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpret
alpha = 0.05
if p > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')


print(df)
