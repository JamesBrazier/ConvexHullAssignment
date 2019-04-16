from results import RESULTS
from time import time
from convexhull import *
"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: James Brazier
   Usercode: jbr185
   Testing file
"""
def runTests(name, function, amount, file=None):
    """Runs the inputted amount of trials for each dataset for the given
       function and reports the time averages and total for all data in
       sets A & B, if a file is given the data will be saved to it also
    """
    i = 0
    for dataset in ['A', 'B']:
        averages = []
        for points in range(1, 11):
            times = []
            points = 3000 * points
            for trial in range(amount):
                percentage = (trial / amount) * 100
                print("  [{:-<20}]  {:.1f}%".format("#" * int(percentage // 5),
                                                    percentage), end='\r')
                times.append(runTest(name, function, dataset, points, 
                                     RESULTS[i], file))
            times = average(times)
            averages.append(times)
            report("{} - {}_{}.dat average {:.4f} seconds".format(name, dataset,
                                            points, times), file)
            i += 1
        averages = sum(averages)
        report("\n{} - dataset_{} total {:.4f} seconds\n".format(name, dataset,
                                                        averages), file)

def runTest(name, function, dataset, points, results, file=None):
    """The function for running an indivisual test for a data file
       stops if a discrepancy between the functions results and the
       expected results given, returns the running time
    """
    startTime = time()
    listPts = readDataPts("Points data\{}_{}.dat".format(dataset, points), 
                          points)
    if sorted(function(listPts)) != results:
        print("ERROR incorrect results")
        return input()
    return time() - startTime

def report(string, file=None):
    """Prints the string to the commandline and the file if given
    """
    print(string)
    if file != None:
        file.write(string + "\n")
        
def average(alist):
    """Gives the average for a list of numbers (who would have guessed)
    """
    return sum(alist) / len(alist)

def main():
    try:
        file = open("Data.txt", "x")
        amount = int(input("Number of trials?\n> ")) 
        print()        
        runTests('Giftwrap', giftwrap, amount, file)
        runTests('Graham Scan', grahamscan, amount, file)
        runTests('Quick Hull', amethod, amount, file)
        file.close()
        print("finished!")
        print("Results saved in Data.txt")
        input()        
    except FileExistsError:
        print("Data is already saved, please delete Data.txt to regenerate")
        input()
    except:
        print("Error, invalid input!")
        input()
    
main()