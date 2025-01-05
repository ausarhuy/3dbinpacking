from py3dbp.packer import Packer
from py3dbp.item import Item
from py3dbp.bin import Bin
from py3dbp.visualizer import Visualizer
import time

start = time.time()

'''

This case is used to demonstrate an example of a packing complex situation.

'''

# init packing function
packer = Packer()
#  init bin
box = Bin('example2', (30, 10, 15), 99, 0, 1)
packer.add_bin(box)
#  add item
packer.add_item(Item('test1', 'test', 'cube', (9, 8, 7), 1, 1, 100, True, 'red'))
packer.add_item(Item('test2', 'test', 'cube', (4, 25, 1), 1, 1, 100, True, 'blue'))
packer.add_item(Item('test3', 'test', 'cube', (2, 13, 5), 1, 1, 100, True, 'gray'))
packer.add_item(Item('test4', 'test', 'cube', (7, 5, 4), 1, 1, 100, True, 'orange'))
packer.add_item(Item('test5', 'test', 'cube', (10, 5, 2), 1, 1, 100, True, 'lawngreen'))
packer.add_item(Item('test6', 'test', 'cube', (6, 5, 2), 1, 1, 100, True, 'purple'))
packer.add_item(Item('test7', 'test', 'cube', (5, 2, 9), 1, 1, 100, True, 'yellow'))
packer.add_item(Item('test8', 'test', 'cube', (10, 8, 5), 1, 1, 100, True, 'pink'))
packer.add_item(Item('test9', 'test', 'cube', (1, 3, 5), 1, 1, 100, True, 'brown'))
packer.add_item(Item('test10', 'test', 'cube', (8, 4, 7), 1, 1, 100, True, 'cyan'))
packer.add_item(Item('test11', 'test', 'cube', (2, 5, 3), 1, 1, 100, True, 'olive'))
packer.add_item(Item('test12', 'test', 'cube', (1, 9, 2), 1, 1, 100, True, 'darkgreen'))
packer.add_item(Item('test13', 'test', 'cube', (7, 5, 4), 1, 1, 100, True, 'orange'))
packer.add_item(Item('test14', 'test', 'cube', (10, 2, 1), 1, 1, 100, True, 'lawngreen'))
packer.add_item(Item('test15', 'test', 'cube', (3, 2, 4), 1, 1, 100, True, 'purple'))
packer.add_item(Item('test16', 'test', 'cube', (5, 7, 8), 1, 1, 100, True, 'yellow'))
packer.add_item(Item('test17', 'test', 'cube', (4, 8, 3), 1, 1, 100, True, 'white'))
packer.add_item(Item('test18', 'test', 'cube', (2, 11, 5), 1, 1, 100, True, 'brown'))
packer.add_item(Item('test19', 'test', 'cube', (8, 3, 5), 1, 1, 100, True, 'cyan'))
packer.add_item(Item('test20', 'test', 'cube', (7, 4, 5), 1, 1, 100, True, 'olive'))
packer.add_item(Item('test21', 'test', 'cube', (2, 4, 11), 1, 1, 100, True, 'darkgreen'))
packer.add_item(Item('test22', 'test', 'cube', (1, 3, 4), 1, 1, 100, True, 'orange'))
packer.add_item(Item('test23', 'test', 'cube', (10, 5, 2), 1, 1, 100, True, 'lawngreen'))
packer.add_item(Item('test24', 'test', 'cube', (7, 4, 5), 1, 1, 100, True, 'purple'))
packer.add_item(Item('test25', 'test', 'cube', (2, 10, 3), 1, 1, 100, True, 'yellow'))
packer.add_item(Item('test26', 'test', 'cube', (3, 8, 1), 1, 1, 100, True, 'pink'))
packer.add_item(Item('test27', 'test', 'cube', (7, 2, 5), 1, 1, 100, True, 'brown'))
packer.add_item(Item('test28', 'test', 'cube', (8, 9, 5), 1, 1, 100, True, 'cyan'))
packer.add_item(Item('test29', 'test', 'cube', (4, 5, 10), 1, 1, 100, True, 'olive'))
packer.add_item(Item('test30', 'test', 'cube', (10, 10, 2), 1, 1, 100, True, 'darkgreen'))

# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=100,
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
