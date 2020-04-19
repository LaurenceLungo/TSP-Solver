# Hybrid Solver for Travelling Salesman Problem (TSP)
This is a Python project which computes a sub-optimal solution to the TSP in ~3 minutes.\
<br>
The program applies different strateges to datasets of different sizes using a combination of greedy, 2-opt, dismantling cross path, and simulated annealing algorithms.\
<br>
It also provides a visualization module to present to result graphically.\
<br>
This project runs on Python3.

## Project structure
| -- TSP-Solver/\
&nbsp;&nbsp;&nbsp;&nbsp;| -- solve_tsp.py\
&nbsp;&nbsp;&nbsp;&nbsp;| -- requirements.txt\
&nbsp;&nbsp;&nbsp;&nbsp;| -- algo/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- greedy_rotate.py\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- two_opt.py\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- cross_path_dismantling.py\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- simulated_annealing.py\
&nbsp;&nbsp;&nbsp;&nbsp;| -- plotter/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- plotter.py\
&nbsp;&nbsp;&nbsp;&nbsp;| -- datasets/\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- ...\
<br>
+ **solve_tsp.py** is the main script which parses the input dataset and outputs the result.
+ **algo/** contains the 4 algorithm modules.
+ **plotter/** contains the TSP tour visualization module.
+ **datasets/** contains a collection of datasets for demonstration.

## Installation
Install all the dependencies from Pypi:
```sh
$ pip install -r requirements.txt
```
## Usage
For a quick start, run
```sh
$ python solve_tsp.py <input-file-directory>
# example: python solve_tsp.py datasets/wi29.txt
```
The result will be stored in a newly created **output-tour.txt** in the same directory.\
<br>
To specify the output file, run
```sh
$ python solve_tsp.py <input-file-directory> <output-file-directory>
# example: python solve_tsp.py datasets/wi29.txt output.txt
```
To visualize the result, add the -v flag
```sh
$ python solve_tsp.py <input-file-directory> <output-file-directory> -v
# example: python solve_tsp.py datasets/wi29.txt output.txt -v
```
To see more information about the usage, run
```sh
$ python solve_tsp.py -h
```
### Input dataset format
The program takes a dataset formatted as follows:
```sh
1 20833.3333 17100.0000
2 20900.0000 17066.6667
3 21300.0000 13016.6667
4 21600.0000 14150.0000
5 21600.0000 14966.6667
6 21600.0000 16500.0000
7 22183.3333 13133.3333
8 22583.3333 14300.0000
9 22683.3333 12716.6667
10 23616.6667 15866.6667
```
### Output format
The program creates an output file formatted as follows:
```sh
tour cost: 27767
tour: [7, 3, 2, 6, 8, 12, 13, 15, 23, 24, 26, 19, 25, 27, 28, 22, 21, 20, 16, 17, 18, 14, 11, 9, 10, 5, 0, 1, 4, 7]
```

## Algorithm modules included
+ **algo.greedy_rotate**: a greedy path finder, except it takes every node in the dataset as the starting point and computes the greedy path once, then returns the shortest one among them.
+ **algo.two_opt**: a basic 2-opt path optimizer.
+ **algo.cross_path_dismantling**: a path optimizer which detects cross paths and dismantles them.
+ **algo.simulated_annealing**: a basic simulated annealing path optimizer.

## Path finding strategy
The program applies different strategies to datasets of different sizes to get the best tour possible in ~3 minutes.
<br>
It first uses *greedy_rotate* to find a reasonably short path to begin with.\
Then,
- for datasets with **<= 50 nodes**:\
&nbsp;&nbsp;&nbsp;&nbsp;*simulated_annealing* is used to further optimize the path.\
&nbsp;&nbsp;&nbsp;&nbsp;If you have good luck it might find you the optimal path.
- for datasets with **> 50 and <= 500 nodes**:\
&nbsp;&nbsp;&nbsp;&nbsp;*cross_path_dismantling* followed by *two_opt* are used to further optimize the path,\
&nbsp;&nbsp;&nbsp;&nbsp;because the size of the dataset is too large for *simulated_annealing* to yield a good result in 3 minutes.
- for datasets with **>500 nodes**:\
&nbsp;&nbsp;&nbsp;&nbsp;only *two_opt* is used to further optimize the path,\
&nbsp;&nbsp;&nbsp;&nbsp;becasue the dataset size is tpp big even for *cross_path_dismantling* to complete within 3 minutes.
