import re
from testa.tokens import TOKENS


s = "Happy Nice Alphanumeric String 123456789"

partitions = {}

for k, t in TOKENS.items():

    res = ''.join(re.findall(t, s))
    print('t: ' + t + ' res: ' + res)

    if partitions.get(res) is not None:  # old partition
        partitions[res] += t
    else:  # new partition.
        partitions[res] = [t]

print(partitions)
