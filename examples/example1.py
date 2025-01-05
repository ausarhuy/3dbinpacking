import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from py3dbp.packer import Packer
from py3dbp.item import Item
from py3dbp.bin import Bin
from py3dbp.visualizer import Visualizer
import time

start = time.time()

'''

This example is used to demonstrate the mixed packing of cube and cylinder.

'''

# init packing function
packer = Packer()
#  init bin
box = Bin('example1', (5.6875, 10.75, 15.0), 70.0, 0, 0)
packer.add_bin(box)
#  add item
packer.add_item(Item('50g [powder 1]', 'test', 'cube', (2, 2, 4), 1, 1, 100, True, 'red'))
packer.add_item(Item('50g [powder 2]', 'test', 'cube', (2, 2, 4), 2, 1, 100, True, 'blue'))
packer.add_item(Item('50g [powder 3]', 'test', 'cube', (2, 2, 4), 3, 1, 100, True, 'gray'))
packer.add_item(Item('50g [powder 4]', 'test', 'cube', (2, 2, 4), 3, 1, 100, True, 'orange'))
packer.add_item(Item('50g [powder 5]', 'test', 'cylinder', (2, 2, 4), 3, 1, 100, True, 'lawngreen'))
packer.add_item(Item('50g [powder 6]', 'test', 'cylinder', (2, 2, 4), 3, 1, 100, True, 'purple'))
packer.add_item(Item('50g [powder 7]', 'test', 'cylinder', (1, 1, 5), 3, 1, 100, True, 'yellow'))
packer.add_item(Item('250g [powder 8]', 'test', 'cylinder', (4, 4, 2), 4, 1, 100, True, 'pink'))
packer.add_item(Item('250g [powder 9]', 'test', 'cylinder', (4, 4, 2), 5, 1, 100, True, 'brown'))
packer.add_item(Item('250g [powder 10]', 'test', 'cube', (4, 4, 2), 6, 1, 100, True, 'cyan'))
packer.add_item(Item('250g [powder 11]', 'test', 'cylinder', (4, 4, 2), 7, 1, 100, True, 'olive'))
packer.add_item(Item('250g [powder 12]', 'test', 'cylinder', (4, 4, 2), 8, 1, 100, True, 'darkgreen'))
packer.add_item(Item('250g [powder 13]', 'test', 'cube', (4, 4, 2), 9, 1, 100, True, 'orange'))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75
)

# print result
for box in packer.bins:
    volume = box.width * box.height * box.depth
    print(":::::::::::", box)

    print("FITTED ITEMS:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''

    # '''
    for item in box.items:
        print("partno : ", item.partno)
        print("group : ", item.group)
        print("color : ", item.color)
        print("position : ", item.position)
        print("rotation type : ", item.rotation)
        print("W*H*D : ", str(item.width) + '*' + str(item.height) + '*' + str(item.depth))
        print("volume : ", float(item.width) * float(item.height) * float(item.depth))
        print("weight : ", float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")
    print("***************************************************")
    # '''
    print("UNFITTED ITEMS:")
    for item in box.unfitted_items:
        print("partno : ", item.partno)
        print("group : ", item.group)
        print("color : ", item.color)
        print("W*H*D : ", str(item.width) + '*' + str(item.height) + '*' + str(item.depth))
        print("volume : ", float(item.width) * float(item.height) * float(item.depth))
        print("weight : ", float(item.weight))
        volume_f += float(item.width) * float(item.height) * float(item.depth)
        unfitted_name += '{},'.format(item.partno)
        print("***************************************************")
    print("***************************************************")
    print('space utilization : {}%'.format(round(volume_t / float(volume) * 100, 2)))
    print('residual volume : ', float(volume) - volume_t)
    print('unpack item : ', unfitted_name)
    print('unpack item volume : ', volume_f)
    print("gravity distribution : ", box.gravity)
    # '''
    stop = time.time()
    print('used time : ', stop - start)

    # draw results
    visualizer = Visualizer(box)
    fig = visualizer.plot_box_and_items(
        title=box.name,
        alpha=0.8,
        write_num=False,
        fontsize=10
    )
    fig.show()