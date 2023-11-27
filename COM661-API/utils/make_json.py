import random, json


def generate_dummy_data():
    productType = ['Room Spray', 'Body Spray', 'Pillow Spray',
                   'Essential Oil', 'Face Oil']
    ingredientType = ['Patchouli', 'Geranium', 'Rosehip']

    product_list = []

    for i in range(100):
        randProductType = productType[random.randint(0, len(productType) - 1)]
        randIngredientType = ingredientType[random.randint(0, len(ingredientType) - 1)]
        name = str(randIngredientType) + ' ' + str(randProductType)
        price = round(random.uniform(10.99, 20.99), 2)
        productDescription = write_descriptions(randIngredientType)
        productSize = calculate_size(randProductType)
        product_list.append(
            {"name": name,
             "price": price,
             "type": randProductType,
             "size": productSize,
             "description": productDescription,
             "reviews": []})
    return product_list


def write_descriptions(ingredientType):
    if ingredientType == 'Patchouli':
        description = 'Patchouli essential oil has been noted to have anti-inflammatory, antibacterial and stress-relieving properties. In China, patchouli has historically been considered a therapeutic herb, and its use has been documented in Traditional Chinese Medicine  for over 1000 years. It has been used to treat fatigue, fever, indigestion and headaches.'
    elif ingredientType == 'Geranium':
        description = 'Geranium essential oil is believed to have antibacterial, antimicrobial, and antiseptic properties making it beneficial for reducing acne breakouts, skin irritation, and skin infections, it is also anecdotally proven to relieve depression and anxiety, making this a calming room or home spray. It has also been known to help women with hormonal changes. It can also be used everyday as a perfume or for masking strong odours.'
    else:
        description = "Organic Rosehip Face Oil has been known for centuries for it's valuable healing benefits. It is loaded with skin nourishing vitamins and essential fatty acids. It also contains phenols that have been shown to have antibacterial, anti-fungal and anti-viral properties."

    return description

def calculate_size(productType):
    if 'oil' in productType.lower():
        size = '30ml'
    else:
        size = '100ml'
    return size


products = generate_dummy_data()
fout = open("products.json", "w")
fout.write(json.dumps(products))
fout.close()