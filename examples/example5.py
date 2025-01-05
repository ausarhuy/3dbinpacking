from py3dbp.packer import Packer
from py3dbp.item import Item
from py3dbp.bin import Bin
from py3dbp.visualizer import Visualizer
import time

start = time.time()

'''

Check stability on item - first rule
1. Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule. 

'''

# init packing function
packer = Packer()
#  init bin 
box = Bin('example5', (5, 4, 3), 100, 0, 0)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority, load bear, Upside down or not , 'item color')
packer.add_bin(box)
packer.add_item(Item('Box-3', 'test', 'cube', (2, 5, 2), 1, 1, 100, True, 'pink'))
packer.add_item(Item('Box-3', 'test', 'cube', (2, 3, 2), 1, 2, 100, True, 'pink'))  # Try switching (2, 2, 2) and (2, 3, 2) to compare the results
packer.add_item(Item('Box-4', 'test', 'cube', (5, 4, 1), 1, 3, 100, True, 'brown'))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75
)

# put order
packer.put_order()

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
        write_num=True,
        fontsize=10
    )
    fig.show()
