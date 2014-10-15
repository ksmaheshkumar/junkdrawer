def fizzbuzz(n):
  for i in xrange(1, n+1):
    s = ''
    if i % 3 and i % 5:
      s = str(i)
    else:
      if i % 3 == 0:
        s += 'fizz'
      if i % 5 == 0:
        s += 'buzz'
    print s

fizzbuzz(100)
