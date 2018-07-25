import copy
import time
# Node expansion counters
BTCounter = 0
FCCounter = 0
CPCounter = 0

def NodeCounter(count):
    '''Increments the number of nodes by 1'''
    return count + 1

def BTHelper(L, M, moveI, markCount, marks, domain):
    '''
    The main recursion function for the backtracking search
    :param L:           Length of the ruler given. | int Eg: L = 6
    :param M:           Number of marks on the ruler. | int Eg: M = 4
    :param moveI:       The ith mark assignment on the ruler. | int Eg: 4
    :param markCount:   Number of marks on the ruler at a given time. | int Eg: 4
    :param marks:       List containing the mark positions on the ruler.
    :param domain:      Range of values that a mark can take. Initially [0,1,...,L]
    :return:            Boolean stating whether a solution exists for the given L, M
    '''
    global BTCounter
    # The recursion end condition
    if markCount == M:
        return True
    # Return false if domain becomes empty
    if domain == set():
        return False
    # For each value in domain
    for nextI in domain:
        # Check if the value taken from domain is a valid assignment
        dValid, diffList = checkDomain(L, marks, nextI)
        # Increment the nodes expanded count
        BTCounter = NodeCounter(BTCounter)
        # If the assignment is valid
        if dValid == True:
            # Add the current value to the marks list
            marks.append(nextI)
            # Nothing is removed from the domain for pure BT
            distSet = set()
            tempDomain = domain - distSet
            # Recursively check for valid assignments to marks
            if BTHelper(L, M, nextI, markCount + 1, marks, tempDomain) == True:
                return True
            # If the assignments do not give a solution, remove the last mark added (Backtrack)
            else:
                del marks[-1]
    return False

def BT(L, M):
    "*** YOUR CODE HERE ***"
    # Initialize the ith move, marks-list, domain and markCount
    moveI = 0
    markCount = 1
    marks = []
    marks.append(0)
    domain = set()
    # Single assignment case
    if M == 1:
        return 1, marks
    for i in range(1, L + 1):
        domain.add(i)
    # Call the helper to find a solution for given L, M
    if BTHelper(L, M, moveI, markCount, marks, domain) == True:
        # If solution exists, call BT again with decreased L and same M
        tempLength , tempMarks = BT(marks[-1] - 1, M)
        # If there is no solution for a given L, return the previous L for which solution exists
        if tempLength == -1:
            return L, marks
        return tempMarks[-1], tempMarks
    # Return no solution if above all fails
    return -1, []

def FCHelper(L, M, moveI, markCount, marks, domain):
    '''
    The main recursion function for the backtracking search
    :param L:           Length of the ruler given. | int Eg: L = 6
    :param M:           Number of marks on the ruler. | int Eg: M = 4
    :param moveI:       The ith mark assignment on the ruler. | int Eg: 4
    :param markCount:   Number of marks on the ruler at a given time. | int Eg: 4
    :param marks:       List containing the mark positions on the ruler.
    :param domain:      Range of values that a mark can take. Initially [0,1,...,L]
    :return:            Boolean stating whether a solution exists for the given L, M
    '''
    global FCCounter
    if markCount == M:
        return True
    if domain == set():
        return False
    for nextI in domain:
        dValid, diffList = checkDomain(L, marks, nextI)
        FCCounter = NodeCounter(FCCounter)
        if dValid == True:
            marks.append(nextI)
            distSet = {nextI}
            # Remove the current assignment from domain
            tempDomain = domain - distSet
            if FCHelper(L, M, nextI, markCount + 1, marks, tempDomain) == True:
                return True
            else:
                del marks[-1]
    return False

def FC(L, M):
    "*** YOUR CODE HERE ***"
    moveI = 0
    markCount = 1
    marks = []
    marks.append(0)
    domain = set()
    if M == 1:
        return 1, marks
    for i in range(1, L + 1):
        domain.add(i)
    if FCHelper(L, M, moveI, markCount, marks, domain) == True:
        tempLength , tempMarks = FC(marks[-1] - 1, M)
        if tempLength == -1:
            return L, marks
        return tempMarks[-1], tempMarks
    return -1, []

def checkDomain(L, marks, nextI):
    '''
    Checks if a given marking sequence is valid
    Computes distinct lengths from the marks and checks if the assignment violates the constraint
    :param L:       Length of the ruler | int
    :param marks:   List containing mark positions
    :param nextI:   The new mark that has to be assigned. | int
    :return:        A boolean stating whether the mark list is valid and list of distinct differences
    '''
    diffList = set()
    isValid = True
    if nextI > L:
        return False, diffList
    tempMarks = copy.deepcopy(marks)
    tempMarks.append(nextI)
    for i in range(len(tempMarks)):
        for j in range(i + 1, len(tempMarks)):
            temp = abs(tempMarks[j] - tempMarks[i])
            if temp in diffList:
                return False, diffList
            else:
                diffList.add(temp)
    return isValid, diffList

def CPHelper(L, M, moveI, markCount, marks, domain):
    '''
    The main recursion function for the backtracking search
    :param L:           Length of the ruler given. | int Eg: L = 6
    :param M:           Number of marks on the ruler. | int Eg: M = 4
    :param moveI:       The ith mark assignment on the ruler. | int Eg: 4
    :param markCount:   Number of marks on the ruler at a given time. | int Eg: 4
    :param marks:       List containing the mark positions on the ruler.
    :param domain:      Range of values that a mark can take. Initially [0,1,...,L]
    :return:            Boolean stating whether a solution exists for the given L, M
    '''
    global CPCounter
    if markCount == M:
        return True
    if domain == set():
        return False
    for nextI in domain:
        dValid, diffList = checkDomain(L, marks, nextI)
        CPCounter = NodeCounter(CPCounter)
        if dValid == True:
            marks.append(nextI)
            distSet = set()
            # Find all future illegal values by adding distinct lengths to current assignments
            for m in marks:
                for j in diffList:
                    distSet.add(m + j)
            # Remove the above values from the domain
            tempDomain = domain - distSet
            # Call the recursion with the reduced domain
            if CPHelper(L, M, nextI, markCount + 1, marks, tempDomain) == True:
                return True
            else:
                del marks[-1]
    return False

def CP(L, M):
    "*** YOUR CODE HERE ***"
    moveI = 0
    markCount = 1
    marks = []
    marks.append(0)
    domain = set()
    if M == 1:
        return 1, marks
    for i in range(1, L + 1):
        domain.add(i)
    if CPHelper(L, M, moveI, markCount, marks, domain) == True:
        m1 = sorted(marks)
        tempLength, tempMarks = CP(m1[-1] - 1, M)
        if tempLength == -1:
            return L, sorted(marks)
        return tempMarks[-1], sorted(tempMarks)
    return -1, []

# Uncomment this to test for nodes expanded and time taken

# def main():
#     L,M = 30,7
#     print("----------------------------------------------------------")
#     a = time.time()
#     print("Solution by BT+CP: ", CP(L,M))
#     print ("Nodes Expanded: ", CPCounter)
#     b = time.time()
#     print ("Time taken: ", round(b - a, 2), "s")
#     print("----------------------------------------------------------")
#     a = time.time()
#     print("Solution by BT+FC: ", FC(L,M))
#     print ("Nodes Expanded: ", FCCounter)
#     b = time.time()
#     print ("Time Taken: ", round(b - a, 2), "s")
#     print("----------------------------------------------------------")
#     a = time.time()
#     print("Solution by BT: ", BT(L,M))
#     print ("Nodes Expanded: ", BTCounter)
#     b = time.time()
#     print ("Time taken: ", round(b - a, 2), "s")
#     print("----------------------------------------------------------")
#
# main()
