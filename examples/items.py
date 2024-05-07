from pkmai.items import Item

item = Item("master-ball", 15)
data = item.to_bytes()
print(item.from_bytes(data))
print(Item.from_number(1, 15))