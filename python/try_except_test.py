'''
testing runtime error handling with exceptions 
including FileNotFoundError, ZeroDivisionError, ImportError, ...

get all builtin exceptions using  
>>> dir(builtins)

'''

x = "hello" 

# specific exception
try:
    assert x == "halo"
except AssertionError as report:
    print("AssertionError exception caught:", report)
except Exception as report:
    import traceback
    traceback.print_exc()

try: 
    1 / 0
except ZeroDivisionError: 
    print('divided by zero')
finally: # always runs
    print('goodbye')

print('reached here')


# unspecified exception
try: 
    open("not_real.txt")
except: 
    print('failed to open')

try:
    x = input("Enter number: ")
    x = x + 1
    print(x)
except:
    print("invalid input")
else:
    print('no exception occured')
finally:
    print('always do this')

print('reach here 2')


# raising exceptions
raise MemoryError("Out of memory")