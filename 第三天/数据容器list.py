# s=["a","b","c","d","e","f","g","h"]
# print(s[0:5:1])
# print(type(s[0:5:1]))
# print(s[0:5:2])
# print(s[0:5:3])
# print(s[:5:1])
# print(s[:5:])
# print(s[:5])
# print(s[:-2:1])


# # 列表list常用方法
#
# s=[56,90,88,65,90,100,209,72,145]
# print(s)
#
# s.append(200)
# print(s)
#
# s.insert(1,300)
# print(s)
#
# s.remove(90)
# print(s)
#
# e=s.pop(1)
# print(e)
#
# e=s.pop()
# print(e)
#
# s.sort()
# print(s)
#
# s.reverse()
# print(s)

# 案例一
# num_list=[]
#
# for i in range(10):
#     num=int(input("输入有效数字"))
#     num_list.append(num)
# print("数字列表：", num_list)
#
# num_list.sort()
# print("排序后的数字", num_list)
#
# print("最小值：", num_list[0])
# print("最大值", num_list[-1])
# print("平均值", sum(num_list)/len(num_list))



# 案例二

# num_list1=[19,23,54,64,875,20,109,132,232,54]
# num_list2=[55,80,72,35,60,123,54,29,91]
#
# # for num in num_list2:
# #     print(num)
# #     num_list1.append(num)
# # num_list =num_list1+num_list2
# num_list=[*num_list1,*num_list2]
# print(num_list)
#
# new_list=[]
# for num in num_list1:
#     if num not in new_list:
#         new_list.append(num)
# print(new_list)
# new_list.sort()
# print(new_list)


# 列表推导式
num_list=[i**2 for i in range(1, 21)]
print(num_list)

