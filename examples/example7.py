from py3dbp.packer import Packer
from py3dbp.item import Item
from py3dbp.bin import Bin
from py3dbp.visualizer import Visualizer
import time

start = time.time()

'''

If you have multiple boxes, you can change distribute_items to achieve different packaging purposes.
1. distribute_items=True , put the items into the box in order, if the box is full, the remaining items will continue to be loaded into the next box until all the boxes are full  or all the items are packed.
2. distribute_items=False, compare the packaging of all boxes, that is to say, each box packs all items, not the remaining items.

'''

# init packing function
packer = Packer()
#  init bin 
box = Bin('example7-Bin1', (5, 5, 5), 100, 0, 0)
box2 = Bin('example7-Bin2', (3, 3, 5), 100, 0, 0)
#  add item
# Item('item partno', (W,H,D), Weight, Packing Priority, load bear, Upside down or not , 'item color')
packer.add_bin(box)
packer.add_bin(box2)

packer.add_item(Item('Box-1', 'test1', 'cube', (5, 4, 1), 1, 1, 100, True, 'yellow'))
packer.add_item(Item('Box-2', 'test2', 'cube', (1, 2, 4), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-3', 'test3', 'cube', (1, 2, 3), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-4', 'test4', 'cube', (1, 2, 2), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-5', 'test5', 'cube', (1, 2, 3), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-6', 'test6', 'cube', (1, 2, 4), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-7', 'test7', 'cube', (1, 2, 2), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-8', 'test8', 'cube', (1, 2, 3), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-9', 'test9', 'cube', (1, 2, 4), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-10', 'test10', 'cube', (1, 2, 3), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-11', 'test11', 'cube', (1, 2, 2), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-12', 'test12', 'cube', (5, 4, 1), 1, 1, 100, True, 'pink'))
packer.add_item(Item('Box-13', 'test13', 'cube', (1, 1, 4), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-14', 'test14', 'cube', (1, 2, 1), 1, 1, 100, True, 'pink'))
packer.add_item(Item('Box-15', 'test15', 'cube', (1, 2, 1), 1, 1, 100, True, 'pink'))
packer.add_item(Item('Box-16', 'test16', 'cube', (1, 1, 4), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-17', 'test17', 'cube', (1, 1, 4), 1, 1, 100, True, 'olive'))
packer.add_item(Item('Box-18', 'test18', 'cube', (5, 4, 2), 1, 1, 100, True, 'brown'))

# calculate packing 
packer.pack(
    bigger_first=True,
    # Change distribute_items=False to compare the packing situation in multiple boxes of different capacities.
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
