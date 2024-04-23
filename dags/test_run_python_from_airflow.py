import pandas as pd
def test_func1():
    print("this is test_func-1")
    return("This is test_func1!")


def test_func2():
    print("this is test_func-2")
    return("This is test_func2!")
def panda_processing():
   
# List1 
    lst = [['tom', 'reacher', 25], ['krish', 'pete', 30],
       ['nick', 'wilson', 26], ['juli', 'williams', 22]]
   
    df = pd.DataFrame(lst, columns =['FName', 'LName', 'Age'])
    print(df)
    df.to_csv('/tmp/output_result.csv',index=False)

print(test_func1())
print(test_func2())
panda_processing()
