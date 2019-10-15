
i = -1
j = 0
while j < 400:
  i = (i + 1) % 181
  j += 1
  print("j: {0} i: {1}".format(j,i))