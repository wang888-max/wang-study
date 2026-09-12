
# # 定义类--->不推荐为对象动态定义属性
# class Car:
#     pass
# c1 = Car()
# c1.color = 'red'
# c1.brand = '奥运'
# c1.maker = '中国'
# c1.price = 100000
#
# print(c1.__dict__)

#
# class Car:
#     def __init__(self, make, model, year, price):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.price = price
#         print("---------------")
# c1=Car("Ford","Mustang",1999,20000)
# print(c1.make)
# print(c1.model)
# print(c1.year)
# print(c1.price)
# print(c1.__dict__)



# 2.实例方法
# 3.魔法方法
# 4.实例属性类属性所有实例对象共享的先是例后对象