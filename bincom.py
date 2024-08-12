import pandas as pd
from io import StringIO
import os
import postgres as pg
import psycopg2
import random

# Copied the HTML content from the link and saved in a variable
html_content = """
<html>
<head>
<title>Our Python Class exam</title>
<style type="text/css">
    body{ width:1000px; margin: auto; }
    table,tr,td{ border:solid; padding: 5px; }
    table{ border-collapse: collapse; width:100%; }
    h3{ font-size: 25px; color:green; text-align: center; margin-top: 100px; }
    p{ font-size: 18px; font-weight: bold; }
</style>
</head>
<body>
<h3>TABLE SHOWING COLOURS OF DRESS BY WORKERS AT BINCOM ICT FOR THE WEEK</h3>
<table>
    <thead>
        <th>DAY</th><th>COLOURS</th>
    </thead>
    <tbody>
    <tr>
        <td>MONDAY</td>
        <td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
    </tr>
    <tr>
        <td>TUESDAY</td>
        <td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td>
    </tr>
    <tr>
        <td>WEDNESDAY</td>
        <td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td>
    </tr>
    <tr>
        <td>THURSDAY</td>
        <td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
    </tr>
    <tr>
        <td>FRIDAY</td>
        <td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td>
    </tr>
    </tbody>
</table>
<p>Examine the sequence below very well, you will discover that for every 1s that appear 3 times, the output will be one, otherwise the output will be 0.</p>
<p>0101101011101011011101101000111 <span style="color:orange;">Input</span></p>
<p>0000000000100000000100000000001 <span style="color:orange;">Output</span></p>
<p>
</body>
</html>
"""

# Read the HTML into a DataFrame
dfs = pd.read_html(StringIO(html_content))

# Since there's only one table, we take the first DataFrame
df = dfs[0]

# Convert DataFrame to dictionary
data = df.to_dict(orient='records')

# Initialize a dictionary to count colors
color_counts = {}

# Iterate through each row in the DataFrame

total_count = 0


for row in data:
    colors = row['COLOURS']
    color_list = colors.split(", ")
    for color in color_list:
        total_count += 1
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1

#1.      Which color of shirt is the mean color?
'''
I don't understand this question, It says find the mean, but color is a Categorical data type, the answer below assumes it was meant to be 'find the "min"'
'''

min_color = min(color_counts, key=color_counts.get)

#2.      Which color is mostly worn throughout the week?
#most occuring color

most_frequent_color = max(color_counts, key = color_counts.get)



#3.      Which color is the median?

def is_median(index, total):
    return round(total/2) == index

def get_median():
    counter = 0
    for row in data:
        colors = row['COLOURS']
        color_list = colors.split(", ")
        for color in color_list:
            counter += 1
            if is_median(counter, total_count):
                return color
median = get_median()        
print(f"median color is: ", median)

# variance = df.var()
# print(f"variance is: ", variance)


#5.      BONUS if a colour is chosen at random, what is the probability that the color is red?

prob_red = color_counts["RED"] / total_count

print(f"the probability that the color is red is: ", prob_red)

#6. Save the colours and their frequencies in postgresql database

# configure db
db_config = {

}
try:
    conn = psycopg2.connect(
        dbname=os.environ["db_name"],
        user=os.environ["db_user"],
        password=os.environ["db_password"],
        host=os.environ["db_host"],
        port=int(os.environ["db_port"])
    )
    cursor = conn.cursor()
    #create color-frequesncy map table
    query1 = f"CREATE TABLE IF NOT EXISTS colors (name VARCHAR(50) PRIMARY KEY, frequency INT NOT NULL DEFAULT 0 );"

    cursor.execute(query1)

    def get_query(color, frequency):
        return f"INSERT INTO colors (name, frequency) VALUES('{color}', {frequency}) ON CONFLICT (name) DO NOTHING;"
    
    for name, frequency in color_counts.items():
        cursor.execute(get_query(name, frequency))


except psycopg2.Error as error:
    print("Error connecting to PostgreSQL database:", error)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
# configure table





# 7. Recursive search algorithm

#assuming the list contains unordered integers
def recurive_search(list, target, start=0):
    if start == len(list):
        return -1
    if list[start] == target:
        return start
    else: 
        return recurive_search(list, target, start + 1)


# 8. Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.

choices = "01"
result = ""
for i in range(4):
    result += random.choice(choices)

print(f"result of 4 random binary numbers: {result}")
decimal = int(result, 2)
print(f"result of 4 random binary numbers({result}) to decimal is: {decimal}")

# Write a program to sum the first 50 fibonacci sequence.

def sum_fibonacci_sequence(n):
    if n <= 0:
        return 0
    
    fibs = [0, 1]
    total_sum = 1
    
    while len(fibs) < n:
        next_fib = fibs[-1] + fibs[-2]
        fibs.append(next_fib)
        total_sum += next_fib
    
    return total_sum

# 9. Example usage
n = 50
result = sum_fibonacci_sequence(n)
print(f"The sum of the first {n} Fibonacci numbers is: {result}")
