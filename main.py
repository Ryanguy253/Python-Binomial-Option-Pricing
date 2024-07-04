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
N = 20 #change as needed
s0 = 200 #Original Stock price
K = 100 # Strike Price
T = 0.0000001 # Time to maturity
r = 0.05 # rf interest rate
v =0.20 # volatility
dt = T/N # delta t, change in time for a period

# Functions
# u is the percentage a stock rises by

U = np.exp(v*np.sqrt(dt));
print(f"Up Factor = {U}")

# d is the percentage a stock falls by

D = 1/(np.exp(v*np.sqrt(dt)));
print(f"Down Factor = {D}")

# q = ((1+r)-d)/(u-d) This is from the assumption that the stock is a martingale
q = (np.exp(r*dt)-D)/(U-D)
print(f"Q = {q}")

#Option Payoffs
def call_payoff(stock_price, strike_price):
    return max(stock_price - strike_price, 0)

def put_payoff(stock_price, strike_price):
    return max(strike_price - stock_price, 0)

# Example tree:
#         S0
#       /     \
#      S1     S2
#     /  \    / \
#    S3  S4  S5  S6

# Node
class BinomialTreeNode:
    def __init__(self, stock_price,option_value=None):
        self.stock_price = stock_price
        self.option_value = option_value
        self.left = None
        self.right = None

# Construct Binary Tree
def ConstructBinaryTree(volatility,dt):
    root = BinomialTreeNode(s0, None)
    current_level = [root]

    for i in range(N):
        next_level = []

        for node in current_level:
            stock_price_up = node.stock_price*U
            stock_price_down = node.stock_price*D

            node.left = BinomialTreeNode(stock_price_up,None)
            node.right = BinomialTreeNode(stock_price_down,None)

            next_level.extend([node.left, node.right])

        current_level = next_level

    return root

def CalculateOptionPrice(node,strike_price):
    if not node.left and not node.right: #leaves
        if option_type == 'call':
            node.option_value = call_payoff(node.stock_price,strike_price)
        else:
            node.option_value = put_payoff(node.stock_price,strike_price)
    else:
        if node.left.option_value is None:
            node.left.option_value = CalculateOptionPrice(node.left,strike_price)
        if node.right.option_value is None:
            node.right.option_value =CalculateOptionPrice(node.right,strike_price)
        node.option_value = (1 / (1 + r)) * (q * node.left.option_value + (1 - q) * node.right.option_value)

    return node.option_value

#Program
#Construct Binary Tree
root = ConstructBinaryTree(v,dt)

#Calculate Option Prices
C0 = CalculateOptionPrice(root,K)

print(f"The Option Price is {C0}")
C=root.left.stock_price
print(f"{C}")
