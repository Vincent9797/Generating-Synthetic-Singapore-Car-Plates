import random

def gen_numbers():
    gen_nums = []
    csnums = []

    while len(gen_nums) < 4:
        gen_nums.append(random.randint(0, 9))

    for index, num in enumerate(gen_nums):
        csnums.append(num * (5 - index))

    return gen_nums, csnums

def car_plate():
    a1 = "S"
    a2 = ["F", "G", "H", "J", "K", "L"]
    a3 = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
          "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ]
    gen_a1 = random.choice(a1)
    gen_a2 = random.choice(a2)
    gen_a3 = random.choice(a3)
    prefix = gen_a1 + gen_a2 + gen_a3

    gen_nums, csnums = gen_numbers()
    csalp2 = (ord(gen_a2.lower()) - 96) * 9
    csalp3 = (ord(gen_a3.lower()) - 96) * 4
    compute = csalp2 + csalp3 + sum(csnums)
    number = ''.join(str(num) for num in gen_nums)

    # TODO: Handle Value Error 
    suffix = get_suffix(compute)
    compete = prefix + number + suffix

    return compete


def goods_plate():
    a1 = "G"
    a2 = ["T", "U", "V", "W", "X", "Y", "Z", "BA", "BB", "BC", "BD", "BE"]
    gen_a1 = random.choice(a1)
    gen_a2 = random.choice(a2)
    prefix = gen_a1 + gen_a2

    if len(prefix) == 2:
        csalp2 = (ord(prefix[0].lower()) - 96) * 9
        csalp3 = (ord(prefix[1].lower()) - 96) * 4
    else:
        csalp2 = (ord(prefix[1].lower()) - 96) * 9
        csalp3 = (ord(prefix[2].lower()) - 96) * 4

    gen_nums, csnums = gen_numbers()
    compute = csalp2 + csalp3 + sum(csnums)
    number = ''.join(str(num) for num in gen_nums)

    # TODO: Handle Value Error 
    suffix = get_suffix(compute)

    compete = prefix + number + suffix
    return compete

def get_suffix(num):
    compute_dict = {   
        0  : 'A',
        1  : 'Z',
        2  : 'Y',
        3  : 'X',
        4  : 'U',
        5  : 'T',
        6  : 'S',
        7  : 'R',
        8  : 'P',
        9  : 'M',
        10 : 'L',
        11 : 'K',
        12 : 'J',
        13 : 'H',
        14 : 'G',
        15 : 'E',
        16 : 'D',
        17 : 'C',
        18 : 'B'
    }

    if num % 19 in compute_dict:
        return compute_dict[num % 19]
    else:
        raise ValueError

def generate(number, typeof=None):
    list_of_cars = []

    if typeof is None:
        plate_generators = [car_plate, goods_plate]
        random_int = random.randint(0, len(plate_generators)-1)
        generate_type = plate_generators[random_int]
    elif typeof == "cars":
        generate_type = car_plate
    else:
        generate_type = goods_plate
    for _ in range(number):
        new_license_plate = generate_type()
        list_of_cars.append(new_license_plate)

    return list_of_cars

def generate_random_plate():
    if random.randint(0, 1) == 0:
        return car_plate()
    else:
        return goods_plate()

if __name__ == '__main__':
    for i in range(100):
        if random.randint(0,1) == 0:
            print(car_plate())
        else:
            print(goods_plate())
