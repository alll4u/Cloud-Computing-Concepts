from hashlib import md5
from struct import unpack_from
from bisect import bisect_left

ITEMS = 100000
NODES = 100
VNODES = 10000
node_stat = [0 for i in range(NODES)]


def _hash(value):
    k = md5(str(value)).digest()
    ha = unpack_from(">I", k)[0]
    return ha

ring = []
hash2node = {}

for n in range(NODES):
    for v in range(VNODES):
        h = _hash(str(n) + str(v))
        ring.append(h)
        hash2node[h] = n
ring.sort()

# ring[] 
# key:   0-NODES*VNODES 
# value: idx的 hash code   

# hash2node
# key:   idx的 hash code
# value: 外层节点编号，非虚节点

# node_stat
# key:   外层节点编号
# value: 每个外层节点的对应数
for item in range(ITEMS):
    h = _hash(str(item))
    # 下面这个取余其实没什么意义啊
    n = bisect_left(ring, h) % (NODES*VNODES)
    node_stat[hash2node[ring[n]]] += 1

print sum(node_stat), node_stat

_ave = ITEMS / NODES
_max = max(node_stat)
_min = min(node_stat)

print("Ave: %d" % _ave)
print("Max: %d\t(%0.2f%%)" % (_max, (_max - _ave) * 100.0 / _ave))
print("Min: %d\t(%0.2f%%)" % (_min, (_ave - _min) * 100.0 / _ave))