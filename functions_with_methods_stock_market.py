## function to give min/max value in a confined range

stock_prices = [34.68, 36.09, 34.94, 33.97, 34.68, 35.82, 43.41, 44.29, 44.65, 53.56, 49.85, 48.71, 48.71, 49.94, 48.53, 47.03, 46.59, 48.62, 44.21, 47.21]

def price_at_day(day):
  return stock_prices[day-1]

def max_price(a,b):
  maximal = 0
  for i in range(a-1,b,1):
    if maximal <= stock_prices[i]:
      maximal = stock_prices[i]
  return maximal

def min_price(a,b):
  minimal = 10000
  for i in range(a-1,b,1):
    if minimal >= stock_prices[i]:
      minimal = stock_prices[i]
  return minimal


print(price_at_day(3))
print(price_at_day(4))

print(max_price(3,4))
print(min_price(3,4))

