# SISO program convertCircuitSatToSat.py

# Convert an instance of CircuitSAT into an
# equivalent instance of SAT.

# inString: an instance of CircuitSAT, formatted as described in the textbook
# each gate is separated by a new line
# no spaces

# returns: an instance of SAT in the same string format.

# Example:
# >>> convertSatTo3Sat('(x1 OR x2 OR NOT x3 OR NOT x4)')
# '(d1 OR x1 OR x2) AND (NOT d1 OR NOT x3 OR NOT x4)'
import utils
from utils import rf
from sat import sat


def convertCircuitSatToSat(inString):
    # Store each gate/expression as an element of the list subExpressions
    subExpressions = inString.split("\n")

    # Step 1
    # Convert gates with three or more inputs to two input gates
    for i in range(len(subExpressions)):
        temp = subExpressions[i]

        count = temp.count(" AND ")
        count2 = temp.count(" OR ")
        if count >= 1:
            if count > 1:
                # e.g. w1 = x1 AND x2 AND x3 AND x4
                # temp1 : w1
                # temp2 : x1 AND x2 AND x3 AND x4
                # tempList[] : x1, x2, x3, x4
                (temp1, temp2) = temp.split(" = ")
                tempList = temp2.split(" AND ")

                # e.g. insertList[0] : w1a = x1 AND x2
                insertList = []
                insertList.append(temp1 + 'a' + " = " + tempList[0] + " AND " + tempList[1])
                subKey = 'b'

                length = len(tempList)
                # e.g. insertList[1] : w1b = w1a AND x3
                for j in range(2, length - 1):
                    insertList.append(temp1 + subKey + " = " + temp1 + chr(ord(subKey) - 1) + " AND " + tempList[j])
                    subKey = chr(ord(subKey) + 1)

                # e.g. insertList[2] : w1 = w1b AND x4
                insertList.append(temp1 + " = " + temp1 + chr(ord(subKey) - 1) + " AND " + tempList[length - 1])

                # replace subexpressions with 2 input gates
                subExpressions.pop(i)
                length = len(insertList)
                for j in range(length):
                    subExpressions.insert(i + j, insertList[j])
        elif count2 >= 1:
            if count2 > 1:
                # e.g. w1 = x1 OR x2 OR x3 OR x4
                # temp1 : w1
                # temp2 : x1 OR x2 OR x3 OR x4
                # tempList[] : x1, x2, x3, x4
                (temp1, temp2) = temp.split(" = ")
                tempList = temp2.split(" OR ")

                # e.g. insertList[0] : w1a = x1 OR x2
                insertList.append(temp1 + 'a' + " = " + tempList[0] + " OR " + tempList[1])
                subKey = 'b'

                length = len(tempList)
                # e.g. insertList[1] : w1b = w1a OR x3
                for j in range(2, length - 1):
                    insertList.append(temp1 + subKey + " = " + temp1 + chr(ord(subKey) - 1) + " OR " + tempList[j])
                    subKey = chr(ord(subKey) + 1)

                # e.g. insertList[2] : w1 = w1b OR x4
                insertList.append(temp1 + " = " + temp1 + chr(ord(subKey) - 1) + " OR " + tempList[length - 1])

                # replace subexpressions with 2 input gates
                subExpressions.pop(i)
                length = len(insertList)
                for j in range(length):
                    subExpressions.insert(i + j, insertList[j])

    # Step 2
    # Convert gates to equivalent CNF formula
    tempList.clear()
    insertList.clear()
    for i in range(len(subExpressions)):
        temp = subExpressions[i]

        (temp1, temp2) = temp.split(" = ")

        # w1 = w2 AND w3 transform to CNF
        # (-w2 v -w3 v w1) ^ (w2 v -w1) ^ (w3 v -w1)
        if " AND " in temp2:
            (temp2, temp3) = temp2.split(" AND ")
            notTemp1 = "NOT " + temp1
            notTemp2 = "NOT " + temp2
            notTemp3 = "NOT " + temp3
            if "NOT " in temp1:
                notTemp1 = temp1.replace("NOT ","")
            if "NOT " in temp2:
                notTemp2 = temp2.replace("NOT ","")
            if "NOT " in temp1:
                notTemp3 = temp2.replace("NOT ","")
            insertList.append("(" + notTemp2 + " OR " + notTemp3 + " OR " + temp1 + ") AND (" + temp2 + " OR " + notTemp1 + ") AND (" + temp3 + " OR " + notTemp1 + ")")

        # w1 = w2 OR w3 transform to CNF
        # (w2 v w3 v -w1) ^ (-w2 v w1) ^ (-w3 v w1)
        elif " OR " in temp2:
            (temp2, temp3) = temp2.split(" OR ")
            notTemp1 = "NOT " + temp1
            notTemp2 = "NOT " + temp2
            notTemp3 = "NOT " + temp3

            if "NOT " in temp1:
                notTemp1 = temp1.replace("NOT ","")
            if "NOT " in temp2:
                notTemp2 = temp2.replace("NOT ","")
            if "NOT " in temp1:
                notTemp3 = temp2.replace("NOT ","")

            insertList.append("(" + temp2 + " OR " + temp3 + " OR " + notTemp1 + ") AND (" + notTemp2 + " OR " + temp1 + ") AND (" + notTemp3 + " OR " + temp1 + ")")

        # w1 = NOT w2
        # (w1 v w2) ^ (-w1 v -w2)
        elif "NOT " in temp2:
            notTemp1 = "NOT " + temp1
            notTemp2 = temp2
            temp2 = notTemp2.replace("NOT ", "")

            insertList.append("(" + temp1 + " OR " + temp2 + ") AND (" + notTemp1 + " OR " + notTemp2 + ")")

    # Step 3
    # Combine all clauses and output with ANDs
    finalCNF = ""
    for i in range(len(insertList)):
        finalCNF += insertList[i] + " AND "
    finalCNF += "output"

    # DEBUG
    # print("Input for sat: " + finalCNF)

    # Step 4
    # Call sat to evaluate
    return sat(finalCNF)
