import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Define dataset with NBA team payroll and wins data
data = {
    'team_payroll': [
        209354737, 201366679, 193838882, 187346674, 186940921, 180922992, 177143542, 169876920, 167755884, 167403924,
        166874287, 166434327, 166271894, 165630436, 165263993, 164990518, 163054678, 162649524, 162515272, 159153393,
        155015136, 153564021, 150856313, 149356730, 148722330, 142867770, 139233014, 135774484, 133738448, 132643598
    ],
    'wins': [
        46, 51, 49, 49, 64, 57, 46, 47, 50, 49, 48, 56, 47, 39, 21, 50, 25, 27, 57, 32,
        46, 15, 41, 47, 44, 22, 14, 21, 31, 47
    ]
}

# Create a DataFrame from the dataset
df = pd.DataFrame(data)

# Check for missing values
print("Missing values:")
print(df.isnull().sum())

# Display the data types of the columns
print("\nData Types:")
print(df.dtypes)


# Create a scatter plot to visualize the relationship between payroll and wins
plt.figure(figsize=(10,6))
sns.scatterplot(x=df['team_payroll'], y=df['wins'])
plt.title('Correlation Between NBA Team Payroll and Wins')
plt.xlabel('Team Payroll (in dollars)')
plt.ylabel('Team Wins')

# Format the x-axis to display values in millions
plt.xticks(ticks=np.arange(100000000, 220000000, 10000000), labels=[f'{x//1000000}' for x in np.arange(100000000, 220000000, 10000000)])
plt.gca().tick_params(axis='x', labelsize=10)
plt.xlabel('Team Payroll (in millions)')

# Display the plot
plt.show()


