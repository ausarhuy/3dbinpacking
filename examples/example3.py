from py3dbp.packer import Packer
from py3dbp.item import Item
from py3dbp.bin import Bin
from py3dbp.visualizer import Visualizer
import time

start = time.time()

'''

This example is used to demonstrate that the algorithm does not optimize.

'''

# init packing function
packer = Packer()
#  init bin 
box = Bin('example3', (6, 1, 5), 100, 0, put_type=1)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority, load bear, Upside down or not , 'item color')
packer.add_bin(box)
# If all item (2, 1, 3) , item can be fully packed into box, but if choose one item and modify (3, 1, 2) , item can't be fully packed into box.
packer.add_item(Item('Box-1', 'test', 'cube', (2, 1, 3), 1, 1, 100, True, 'yellow'))
packer.add_item(Item('Box-2', 'test', 'cube', (3, 1, 2), 1, 1, 100, True, 'pink'))  # Try switching (3, 1, 2) and (2, 1, 3) to compare the results
packer.add_item(Item('Box-3', 'test', 'cube', (2, 1, 3), 1, 1, 100, True, 'brown'))
packer.add_item(Item('Box-4', 'test', 'cube', (2, 1, 3), 1, 1, 100, True, 'cyan'))
packer.add_item(Item('Box-5', 'test', 'cube', (2, 1, 3), 1, 1, 100, True,'olive'))

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
        alpha=0.2,
        write_num=True,
        fontsize=10
    )
    fig.show()
