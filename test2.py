# import time, os
#
#
# date = 1  #time.strftime('%Y%m%d')
# a = 'photo'
# if not a:
#     os.mkdir('photo')
# isExists = os.path.exists(f'./photo/{date}')
# if not isExists:
#     os.mkdir(f'./photo/{date}')
# else:
#     print(1)


# a = 1
# b = '1'
# if a == b:
#     print('等于')
# else:
#     print('不等于')

allHour = {1,2,3,4,11}
allMinute = {1,2,3,4,11}
browserHour = 11
browserMinute = 11
nowMinute = '5' + '7'
nowHour = '2' + '2'
# 开始时间
if int(nowMinute) >= 58:
    subscript1 = int(browserHour) + 1  # 下标
    print(subscript1)
else:
    subscript2 = int(browserMinute) + 4
    print(subscript2)