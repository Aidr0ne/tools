class X: pass
class Y: pass

data = {
    1: ['Air', 2, '/home/aiden/Engine/engine/General/Air.png', 0, True, False],
    2: ['Ground', 3, 'dirt.png', 3, True, False, X, Y],
    3: ['Door', 4, 'Door.png', X, Y, 10, 10, False, 1000000000, 'testtp.pkl', """save_dict = {
    "Player": eng.objects.Player,
    "Ground": eng.objects.Ground,
    "Air": eng.objects.Air,
    "Door": eng.objects.Door,
}"""],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    0: []
}

meta = {
    1: ['Name', 'Save Id', 'Sprite Path', 'Hp', 'Transparent', 'Solid'],
    2: ['Name', 'Save Id', 'Sprite Path', 'Hp', 'Solid', 'Transparent', 'X', 'Y'],
    3: ['Name', 'Save Id', 'Sprite Path', 'X', 'Y', 'Target X', 'Target Y', 'Locked', 'Hp', 'Target File', "Save Dict"],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    0: []
}