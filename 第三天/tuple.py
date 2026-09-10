t1=(80,95,78,56,673,23,33)
print(t1)
print(tuple(t1))

print(t1[0])
print(t1[1])

print(t1.count(80))
print(t1.index(80))


# 组包解包
t1=(80,95,78,56,673,23,33)
t2=80,95,78,56,673,23,33
# 解包
a,b,c,d,e,f,g=t1
print(a)
print(b)

first,*other=t2
print(first)
print(*other)