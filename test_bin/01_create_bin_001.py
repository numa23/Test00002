# 0       1       2       3       4       5       6       7       
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# aaaaaaaabccddeefgggggggghhhhhhhhyyyyyyyyyyyymmmmdddddhhhhhmmmmmm

# aaaaaaaa(8):0x96
# b(1):0 or 1
# cc(2):0～3
# dd(2):0～3
# ee(2):0～3
# f(1):0
# gggggggg(8):'N'
# hhhhhhhh(8):'U'
# yyyyyyyyyyyy(12):2025
# mmmm(4):6
# ddddd(5):23
# hhhhh(5):15
# mmmmmm(6):54


data_type = 0x96
bit = 1
cc = 1
dd = 2
ee = 3
reserved1 = 'N'
reserved2 = 'U'
year = 2025
month = 6
day = 23
hour = 15
min = 54

data = b'\x00\x00\x00\x00\x00\x00\x00\x00'
data_ = bytearray(data)

#------
# 圧縮
#------
# 0       1       2       3       4       5       6       7       
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# aaaaaaaabccddeefgggggggghhhhhhhhyyyyyyyyyyyymmmmdddddhhhhhmmmmmm
data_[0] |= data_type
data_[1] |= bit << 7
data_[1] |= cc << 5
data_[1] |= dd << 3
data_[1] |= ee << 1
data_[2] = ord(reserved1)
data_[3] = ord(reserved2)
data_[4] |= (year >> 4) & 0b11111111
data_[5] |= (year << 4) & 0b11110000
data_[5] |= (month >> 0) & 0b00001111
data_[6] |= (day << 3) & 0b11111000
data_[6] |= (hour >> 2) & 0b00000111
data_[7] |= (hour << 6) & 0b11000000
data_[7] |= (min >> 0) & 0b00111111

# print((year >> 4) & 0xFF)
# print((year << 4) & 0xFF)
# print(hex((year >> 4) & 0xFF))
# print(hex((year << 4) & 0xFF))

print(type(data_))
print(data_)


# with open('test001.bin', '+bw') as f:
#     f.write()

#------
# 解凍
#------
# 0       1       2       3       4       5       6       7       
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# aaaaaaaabccddeefgggggggghhhhhhhhyyyyyyyyyyyymmmmdddddhhhhhmmmmmm
type_ = hex(data_[0])
bit_ = (data_[1] >> 7) & 0b00000001
cc_ = (data_[1] >> 5) & 0b00000011
dd_ = (data_[1] >> 3) & 0b00000011
ee_ = (data_[1] >> 1) & 0b00000011

reserved1_ = (data_[2] & 0b11111111) << 0
reserved2_ = (data_[3] & 0b11111111) << 0

year_ = (data_[4] & 0b11111111) << 4
year_ += (data_[5] & 0b11110000) >> 4
month_ = (data_[5] & 0b00001111) << 0
day_ = (data_[6] & 0b11111000) >> 3
hour_ = (data_[6] & 0b00000111) << 2
hour_ += (data_[7] & 0b11000000) >> 6
min_ = (data_[7] & 0b00111111) << 0



print(f'type:{type_}')
print(f'bit:{bit_}')
print(f'cc:{cc_}')
print(f'dd:{dd_}')
print(f'ee:{ee_}')

print(f'reserved1:{chr(reserved1_)}')
print(f'reserved2:{chr(reserved2_)}')

print(f'year:{year_}')
print(f'month:{month_}')
print(f'day:{day_}')
print(f'hour:{hour_}')
print(f'min:{min_}')

# <class 'bytearray'>
# bytearray(b'\x96\xb6NU~\x96\xbb\xf6')
# type:0x96
# bit:1
# cc:1
# dd:2
# ee:3
# reserved1:N
# reserved2:U
# year:2025
# month:6
# day:23
# hour:15
# min:54
