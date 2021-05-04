from convertCircuitSatToSat import convertCircuitSatToSat

input = "w1 = x1 AND x2 AND x3\n" + "w2 = NOT x3\n" + "w3 = w2 OR x4\n" + "output = w1 AND w3"
# input = "output=x1ANDx2"
output = convertCircuitSatToSat(input)

print(output)
