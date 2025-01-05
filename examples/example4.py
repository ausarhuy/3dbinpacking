from py3dbp.packer import Packer
from py3dbp.item import Item
from py3dbp.bin import Bin
from py3dbp.visualizer import Visualizer
import time

start = time.time()

'''

This example can be used to test large batch calculation time and binding functions.

'''

# init packing function
packer = Packer()

# Evergreen Real Container (20ft Steel Dry Cargo Container)
# Unit cm/kg
box = Bin(
    name='example4',
    whd=(589.8, 243.8, 259.1),
    max_weight=28080,
    corner=15,
    put_type=0
)

packer.add_bin(box)

# dyson DC34 (20.5 * 11.5 * 32.2 ,1.33kg)
# 64 pcs per case ,  82 * 46 * 170 (85.12)
for i in range(15):
    packer.add_item(Item(
        partno='Dyson DC34 Animal{}'.format(str(i + 1)),
        group='Dyson',
        type='cube',
        whd=(170, 82, 46),
        weight=85.12,
        priority=1,
        loadbear=100,
        upsidedown=True,
        color='#FF0000')
    )

# washing machine (85 * 60 *60 ,10 kG)
# 1 pcs per case, 85 * 60 *60 (10)
for i in range(18):
    packer.add_item(Item(
        partno='wash{}'.format(str(i + 1)),
        group='wash',
        type='cube',
        whd=(85, 60, 60),
        weight=10,
        priority=1,
        loadbear=100,
        upsidedown=True,
        color='#FFFF37'
    ))

# 42U standard cabinet (60 * 80 * 200 , 80 kg)
# one per box, 60 * 80 * 200 (80)
for i in range(15):
    packer.add_item(Item(
        partno='Cabinet{}'.format(str(i + 1)),
        group='cabinet',
        type='cube',
        whd=(60, 80, 200),
        weight=80,
        priority=1,
        loadbear=100,
        upsidedown=True,
        color='#842B00')
    )

# Server (70 * 100 * 30 , 20 kg) 
# one per box , 70 * 100 * 30 (20)
for i in range(42):
    packer.add_item(Item(
        partno='Server{}'.format(str(i + 1)),
        group='server',
        type='cube',
        whd=(70, 100, 30),
        weight=20,
        priority=1,
        loadbear=100,
        upsidedown=True,
        color='#0000E3')
    )

# calculate packing
packer.pack(
    bigger_first=True,
    distribute_items=False,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.75,
    binding=[('server', 'cabinet', 'wash')],
    # binding=['cabinet','wash','server']
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

