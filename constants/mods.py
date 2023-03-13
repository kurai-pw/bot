from enum import IntFlag

class Mods(IntFlag):
    NOMOD = 0
    NOFAIL = 1 << 0
    EASY = 1 << 1
    TOUCHSCREEN = 1 << 2  # old: 'NOVIDEO'
    HIDDEN = 1 << 3
    HARDROCK = 1 << 4
    SUDDENDEATH = 1 << 5
    DOUBLETIME = 1 << 6
    RELAX = 1 << 7
    HALFTIME = 1 << 8
    NIGHTCORE = 1 << 9
    FLASHLIGHT = 1 << 10
    AUTOPLAY = 1 << 11
    SPUNOUT = 1 << 12
    AUTOPILOT = 1 << 13
    PERFECT = 1 << 14
    KEY4 = 1 << 15
    KEY5 = 1 << 16
    KEY6 = 1 << 17
    KEY7 = 1 << 18
    KEY8 = 1 << 19
    FADEIN = 1 << 20
    RANDOM = 1 << 21
    CINEMA = 1 << 22
    TARGET = 1 << 23
    KEY9 = 1 << 24
    KEYCOOP = 1 << 25
    KEY1 = 1 << 26
    KEY3 = 1 << 27
    KEY2 = 1 << 28
    SCOREV2 = 1 << 29
    MIRROR = 1 << 30

    def split(self) -> list:
        return str(Mods(self.value)).split('Mods.')[1].split('|')

    def human_readable(self):
        mods = {
            'NOMOD': None,
            'NOFAIL': 'NF',
            'EASY': 'EZ',
            'TOUCHSCREEN': 'TS',
            'HIDDEN': 'HD',
            'HARDROCK': 'HR',
            'SUDDENDEATH': 'SD',
            'DOUBLETIME': 'DT',
            'NIGHTCORE': 'NC',
            'RELAX': 'RX',
            'HALFTIME': 'HF',
            'FLASHLIGHT': 'FL',
            'AUTOPLAY': '',
            'SPUNOUT': 'SO',
            'AUTOPILOT': 'AP',
            'PERFECT': 'PF',
            'KEY1': 'K1',
            'KEY2': 'K2',
            'KEY3': 'K3',
            'KEY4': 'K4',
            'KEY5': 'K5',
            'KEY6': 'K6',
            'KEY7': 'K7',
            'KEY8': 'K8',
            'KEY9': 'K9',
            'FADEIN': '',
            'RANDOM': '',
            'CINEMA': '',
            'TARGET': '',
            'KEYCOOP': '',
            'SCOREV2': 'V2',
            'MIRROR': '',
        }

        res = []

        for mode in self.split():
            res.append(mods[mode])

        if res:
            return ' +' + ''.join(res)
        return None
