freq = {}
while True:
  try:
    num = input("Enter a number (q to quit): ")
    if num == "q":
      break
    num = int(num)
  except ValueError:
    print("Not a valid number! Enter to continue...")
    input()
    continue
  while num > 0:
    digit = num % 10
    freq[digit] = freq.get(digit, 0) + 1
    num //= 10
  print("Frequency of each digit: " + str(freq))
  freq.clear()
