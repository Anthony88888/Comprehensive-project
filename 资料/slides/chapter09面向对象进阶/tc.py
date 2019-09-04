
import inspect

class TypeCheck:
    def __init__(self, name, typ):
        self.name = name
        self.type = typ

    def __get__(self, instance, owner):
        print('get~~~~~~~~~~')
        if instance:
            return instance.__dict__[self.name]
        return instance

    def __set__(self, instance, value):
        print('set+++++++++++++')
        if not isinstance(value, self.type): # 'tom'
            raise TypeCheck(value)
        instance.__dict__[self.name] = value



class Person:
    name = TypeCheck('name', str) # 硬编码 inspect
    age = TypeCheck('age', int) #写死了

    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age



p1 = Person('tom', 18)
print('-' * 30)
print(Person.name)
print(p1.name)
print(p1.__dict__)
print(p1.age)

#p2 = Person('jerry', '20')

p1.age = 100
p1.test = 1000
print(p1.__dict__)
Person.age = 2000
p1.age = 2
