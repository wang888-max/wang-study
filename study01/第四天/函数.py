# def out_line():
#     print('--------------')
# out_line()
# # 函数说明文档 """      """
# #
# def triangle_area(base, height):
#     area = base * height/2
#     return area
# print("三角形的面积：", triangle_area(100, 10))

# 不定长参数 位置传参*args  封装到元组中
# def calc_data(*args):
#     min_data=min(args)
#     max_data=max(args)
#     avg_data=sum(args)/len(args)
#     return min_data, max_data,avg_data
#
# print(calc_data(14, 22, 34,32))


# 关键字传参 **kwargs  封装到字典中



# 函数参数类型 数字 布尔 字符串 列表 元组 集合 字典
# 特殊参数  函数


# 匿名函数lambda
# out_line= lambda : print("-----------------------")
# add=lambda x,y: x+y
# out_line()
# print(add(100,200))

# 计算n的阶乘
# def jc(n):
#     if n == 1:
#         return 1
#     else:
#         return n * jc(n - 1)
# resault=jc(10)
# print(resault)

# def calc_order_cost(*args,coupon,score,express):


# 函数类型注解