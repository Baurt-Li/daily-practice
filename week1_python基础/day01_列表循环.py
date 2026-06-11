scores = [60,70,80,90,100,95,94,85,75,85]
# pingjun = sum(scores)/len(scores)
# count = 0
# for i in scores:
#     if i > pingjun:
#         count += 1
# print(pingjun,count)
fenshu = 0
for i in scores:
    if i >= 0 :
        fenshu += i
pingjun = fenshu/len(scores)
print(pingjun)


