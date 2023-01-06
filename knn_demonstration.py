# import matplotlib to plot the graph to visualize the data
import matplotlib.pyplot as plt

# pre-defined data set
data = [(1.11, 1.6, 'red'),
        (1.99, 2, 'red'),
        (5.19, 5.61, 'red'),
        (6.8, 3, 'red'),
        (3.19, 6.2, 'red'),
        (1.58, 8, 'red'),
        (2.09, 8.5, 'red'),
        (8.04, 9.05, 'red'),
        (3.89, 1.5, 'green'),
        (3.5, 2.5, 'green'),
        (2.25, 3.5, 'green'),
        (3.1, 4.5, 'green'),
        (2.4, 6.6, 'green'),
        (1.87, 7.18, 'green'),
        (4.27, 8.31, 'green'),
        (6.99, 1.5, 'blue'),
        (8.49, 2.01, 'blue'),
        (8.9, 2.6, 'blue'),
        (4.5, 3, 'blue'),
        (7.36, 4.07, 'blue'),
        (4.18, 5.5, 'blue'),
        (2.49, 5.8, 'blue'),
        (5.09, 7, 'blue'),
        (6.93, 6.95, 'blue'),
        (8.99, 6, 'blue'),
        (7.29, 8, 'blue'),
        (9.08, 8.6, 'blue')]

# flag to determine either KNN or weighted KNN algorithm to use
# set use_weighted_knn = True to use weighted KNN algorithm to do classification
use_weighted_knn = False

# flag to determine use default test data or manual input
# set manual_input_test_data = True to change to manual input X and Y coordination
# set manual_input_test_data = False to use default test data (3.3, 5.0)
manual_input_test_data = False

# default test data values
testX = 3.3
testY = 5

# function to calculate euclidean distance between two points with multi-dimensions
def euclidean(x, test_data):
    dist = 0
    for i in range(len(test_data)):
        dist += (x[i] - test_data[i]) ** 2
    #    dist = ((x[0] - test[0])** 2 + (x[1] - test[1])** 2)** 0.5
    return dist ** 0.5


# function only allows integer input
def input_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Only Integer value is allowed!")
            continue


# function only allows float input
def input_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Only Float value is allowed!")
            continue


# function to analyze data with KNN algorithm
def vote_knn(vote_list):
    result = dict()
    # count the vote of each color
    for color in vote_list:
        if color not in result:
            result[color] = vote_list.count(color)
    return result


# function to analyze data with weighted KNN algorithm
def vote_weighted_knn(vote_list):
    result = dict()
    # count the vote of each type
    for vote_data in vote_list:  # evaluate each possible vote
        color = vote_data[3]
        distance = vote_data[0]
        if color not in result:
            result[color] = 0
        # the weighting is calculated by 1/distance
        # so closer data with higher weighting
        result[color] += 1 / distance
    return result


# user input test's X and Y coordination values
if(manual_input_test_data):
    testX = input_float("Input Test's X coordination: ")
    testY = input_float("Input Test's Y coordination: ")

# user input positive integer K value for KNN
k = 0
while k <= 0:
    k = input_integer('Input K value (positive integer): ')

# define test data from user input
test = (testX, testY)

# obtain the trained data [euclidean, x, y, color] with distance between test and each point of data
train_set = [(euclidean(datum, test), datum[0], datum[1], datum[2]) for datum in data]
# use the euclidean distance to sort data with ascending order
train_set.sort(key=lambda i: i[0])
[print(f"{train_datum[0]:.2f} | {train_datum[1]} | {train_datum[2]} |{train_datum[3]}") for train_datum in train_set]

# K-NN data
nearest_neighbors = train_set[:k]

if use_weighted_knn:
    # count the vote with KNN weighted algorithm
    count_votes = vote_weighted_knn(nearest_neighbors)
else:
    # count the vote with KNN algorithm
    count_votes = vote_knn([x[3] for x in nearest_neighbors])

# sort the votes with descending order and predict the color as the first element with the highest vote
sorted_votes = sorted(count_votes, key=lambda i: count_votes[i], reverse=True)
# print the result of votes
print(f'Result of Vote: {count_votes}')
# handles TIE situation
if len(count_votes) > 1 and count_votes[sorted_votes[0]] == count_votes[sorted_votes[1]]:
    predicted_color = 'black'
    print('Prediction of test color: Unknown with Tie')
else:
    predicted_color = sorted_votes[0]  # predicted color with the highest vote
    print(f'Prediction of test color: {predicted_color}')

# plot the data points with matplotlib
[plt.scatter(datum[0], datum[1], label="data", color=datum[2], marker=".", s=200) for datum in data]
# circle the K nearest neighbor data with vote
[plt.scatter(neighbor[1], neighbor[2], s=300, facecolors='none', edgecolors='black') for neighbor in nearest_neighbors]
# plot the test data in graph with predicted color
plt.scatter(testX, testY, label="test", color=predicted_color, marker="*", s=200)
# render the graph
plt.axis('equal')
plt.title('Data Color Plot')
plt.show()
