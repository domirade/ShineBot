# hardcoded IDs? in MY bot? it's more likely than you think

import enum

Guilds = {
    'Shine': 637859341193445377,
    'MabiPro': 280414320595304448
    }
    
Users = {
    'Domirade': 146191479746854913,
    'rice': 192862829362020352
}

Roles = {
    'Developer' : 733732703295504474,
    'Friend' : 638092428070354949,
    'Member' : 637860859212988417,
    'Senior' : 637906599448674305,
    'Officer' : 637860109187284993,
    'Leader' : 637860034956754957
    }

CosmeticRoles = {
    'Archer' : 638738870308962314,
    'Mage' : 638738866618105894,
    'Warrior' : 638738872066375711,
    'Alchemist' : 638738829645316096,
    'Basic' : 738507198296096788,
    'Intermediate' : 738507262192123995,
    'Advanced' : 738507373571997696,
    'Hardmode' : 738507484641230989,
    'Elite' : 738507573468069959,
    'Shinecraft' : 732421163703205960,
    'Winemaking' : 742591841492402216,
    'Venting' : 760907349174386709,
    'Maplestory' : 770037023854690345
    }

Channels = {
    'Development' : 700852121150554133, # bot-spam
    'Public-Info' : 760915117306150994, #information
    'General' : 637861464774017044, # guild-general
    'Market' : 639289350722551819, # wishlist-bazaar
    'Bosses': 737258991603679233, # field-bosses
    'LFG': 637953663930859521, # events-lfg
    'QNA' : 637976439299506186,
    'Suggestions' : 637976383389433887,
    'MabiPro_Market' : 280895499383603211
}

@enum.unique
class Emoji(enum.Enum):
    unknown = "❓"
    sunny = "☀"
    cloudy = "☁"
    rainy = "🌧"
    thunder = "🌩"
    def get(i:int) -> str:
        """ Gets the emoji corresponding to the integer argument. """
        if i == -9:
            return Emoji.unknown.value
        elif i == -8:
            return Emoji.sunny.value
        elif i in range(-7,0):
            return Emoji.cloudy.value
        elif i in range(0,20):
            return Emoji.rainy.value
        elif i == 20:
            return Emoji.thunder.value