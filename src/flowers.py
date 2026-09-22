import csv


def load_flowers(filepath="coordonnees.csv"):
    flowers = []

    with open(filepath, mode="r", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            if row:
                x = float(row[0])
                y = float(row[1])
                flowers.append((x, y))

    return flowers


print(load_flowers())
