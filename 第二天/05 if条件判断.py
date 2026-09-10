# a = int(input("请输入第一个边长"))
# b = int(input("请输入第二个边长"))
# c = int(input("请输入第三个边长"))
# if a + b > c and a + c > b and b + c > a:
#     if a == b and b == c:
#         print(f"{a}{b}{c}这三个边长构成等边三角形")
#     elif a == b or a == c or b == c:
#         print(f"{a}{b}{c}这三个边长构成等腰三角形")
#     else:
#         print(f"{a}{b}{c}这三个边长构成普通三角形")
# else:
#     print(f"{a}{b}{c}这三个边长不构成三角形")

# elc = float(input("请输入用电度数"))
# if elc <= 2800:
#     print(f"电费{0.4883 * elc}")
# if elc < 4800 and elc> 2800:
#     print(f"电费{2800*0.4883+(elc-2800)*0.5383}")
# if elc >=4800:
#     print(f"电费{2800*0.4883+2000*0.5383+(elc-4800)*0.7883}")
usage_elec = int(input("请输入用电度数: "))

# 定义阶梯电价
first_max = 2880  # 第一档上限
second_max = 4800  # 第二档上限

first_price = 0.4883  # 第一档单价
second_price = 0.5383  # 第二档单价
third_price = 0.7883  # 第三档单价

total_cost = 0.0  # 总电费

# 使用if语句进行阶梯电价计算
if usage_elec <= first_max:
    # 全部在第一档
    total_cost = usage_elec * first_price
elif usage_elec <= second_max:
    # 第一档部分
    first_cost = first_max * first_price

    # 第二档部分
    second_usage = usage_elec - first_max
    second_tier_cost = second_usage * second_price
    total_cost = first_cost + second_tier_cost
else:
    # 第一档部分
    first_cost = first_max * first_price

    # 第二档部分
    second_usage = second_max - first_max
    second_cost = second_usage * second_price

    # 第三档部分
    third_usage = usage_elec - second_max
    third_cost = third_usage * third_price
    total_cost = first_cost + second_cost + third_cost

print(f"{usage_elec} 度的电费是: {total_cost} 元")