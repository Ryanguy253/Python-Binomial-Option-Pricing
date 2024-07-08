import math

import numpy as np

# Martingale - Future expected value = current value, therefore stock is as likely to move up as it is likely to move down, therefore not arbitrage
# pg 119 slides

'''
Define Parameters
n -  Number of periods (number of times the stock can change price)

s0 - current value of stock
K - Option Strike Price
T - Time to maturity

q - Probability that stock goes up
r - Risk free interest rate

u - Up Factor
d - Down Factor 

v - Volatility

C(n) - price of call option based on martingale assumption and working backwards from the discounted call price in the future
'''

option_type = 'call'
N = 20  # change as needed
s0 = 100  # Original Stock price
K = 100  # Strike Price
T = 1  # Time to maturity
r = 0.05  # rf interest rate
v = 0.20  # volatility
dt = T / N  # delta t, change in time for a period

# Functions
# u is the percentage a stock rises by
U = np.exp(v * np.sqrt(dt))
print(f"Up Factor = {U}")

# d is the percentage a stock falls by
D = 1 / (np.exp(v * np.sqrt(dt)))
print(f"Down Factor = {D}")

# q = ((1+r)-d)/(u-d) This is from the assumption that the stock is a martingale
q = (np.exp(r * dt) - D) / (U - D)
print(f"Q = {q}")


# Option Payoffs
# def call_payoff(stock_price, strike_price):
    #return max(stock_price - strike_price, 0)


#def put_payoff(stock_price, strike_price):
    #return max(strike_price - stock_price, 0)


# Example tree:
#         S0
#       /     \
#      S1     S2
#     /  \    / \
#    S3  S4  S5  S6

# Node
class BinomialTreeNode:
    def __init__(self, stock_price, option_value=None):
        self.stock_price = stock_price
        self.option_value = option_value
        self.left = None
        self.right = None


# Construct Binary Tree
def ConstructBinaryTree(volatility, dt):
    global U, D

    root = BinomialTreeNode(s0, None)
    current_level = [root]

    for i in range(N):
        next_level = []

        for node in current_level:
            stock_price_up = node.stock_price * U
            stock_price_down = node.stock_price * D

            node.left = BinomialTreeNode(stock_price_up, None)
            node.right = BinomialTreeNode(stock_price_down, None)

            next_level.extend([node.left, node.right])

        current_level = next_level

    return root


def CalculateOptionPrice(node, strike_price):
    global r, q
    if not node.left and not node.right:  # leaves
        if option_type == 'call':
            node.option_value = max(node.stock_price - strike_price, 0)
        else:
            node.option_value = max(strike_price - node.stock_price, 0)
    else:
        if node.left.option_value is None:
            node.left.option_value = CalculateOptionPrice(node.left, strike_price)
        if node.right.option_value is None:
            node.right.option_value = CalculateOptionPrice(node.right, strike_price)
        node.option_value = np.exp(-r * dt) * (q * node.left.option_value + (1 - q) * node.right.option_value)

    return node.option_value


# Program
# Construct Binary Tree

root = ConstructBinaryTree(v, dt)

# Calculate Option Prices
C0 = CalculateOptionPrice(root, K)

print(f"The Option Price is {C0}")


# different approach (using combination formula)
def combination(n, i):
    return math.factorial(n) / (math.factorial(n - i) * math.factorial(i))


call_price_combination = 0

for k in range(N + 1):
    # Probability of each node
    _P = combination(N, k) * q ** k * (1 - q) ** (N - k)

    # Possible Stock Prices and Payoff
    ST = s0 * U ** k * D ** (N - k)

    # call price is probability of all outcomes multiplied by payoff price - it is the fair price
    if option_type == 'call':
        call_price_combination += _P * max(ST - K, 0)  # call payoff
    else:
        call_price_combination += _P * max(K - ST, 0)  # put payoff

call_price_combination * (np.exp(-r * T))

print(f"Call Price = {call_price_combination}")
