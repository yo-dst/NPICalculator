from queue import LifoQueue
from queue import Empty

def is_float(str: str) -> bool:
	try:
		float(str)
		return True
	except ValueError:
		return False

def is_operator(str: str) -> bool:
	if str == "+" \
		or str == "-" \
		or str == "*" \
		or str == "/":
		return True
	return False

def calculate(operator: str, left_operand: float, right_operand: float):
	if operator == "+":
		return left_operand + right_operand
	if operator == "-":
		return left_operand - right_operand
	if operator == "*":
		return left_operand * right_operand
	return left_operand / right_operand

def evaluate_NPI_expression(expression: str) -> int | float:
	# https://docs.python.org/3/library/queue.html#queue.LifoQueue
	stack = LifoQueue()

	# simple parsing technique
	tokens = expression.split()

	# loop through tokens and apply NPI algorithm
	for token in tokens:
		if is_float(token):
			# push number to the stack
			stack.put(float(token))
		elif is_operator(token):
			# pop two numbers from the stack
			try:
				right_operand = stack.get_nowait()
				left_operand = stack.get_nowait()
			except Empty:
				raise Exception("Tried to retrieve an operand but the stack is empty")
			
			# apply the operator on them and push the result on the stack
			result = calculate(token, left_operand, right_operand)
			stack.put(result)
		else:
			raise Exception("Got an invalid token")
		
	# last number in the stack is the final result
	try:
		result = stack.get_nowait()
	except Empty:
		raise Exception("Tried to retrieve the result but the stack is empty")
	
	# if it remains number(s) in the stack something went wrong
	if stack.empty() == False:
		raise Exception("Finished evaluating the expression but there isn't empty")
	
	return result if int(result) != result else int(result)

def main():
	return 0

if __name__ == "__main__":
	main()