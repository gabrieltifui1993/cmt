
class Coin():

    def __init__(self, id, code, name, sortOrder):
        self.id = id
        self.code = code
        self.name = name
        self.sortOrder = sortOrder

    def __str__(self):
        representation = "id: {} code: {} name: {} sortOrder: {}" \
            .format(self.id, self.code, self.name, self.sortOrder)
        return representation

    def __repr__(self):
        representation = "id: {} code: {} name: {} sortOrder: {}"\
                        .format(self.id, self.code, self.name, self.sortOrder)
        return representation

class CoinPropertyConstants:
    ID = "Id"
    NAME = "Name"
    FULL_NAME = "CoinName"
    SORT_ORDER = "SortOrder"