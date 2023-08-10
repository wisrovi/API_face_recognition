import json
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from matplotlib.patches import Polygon as mpl_polygon


def find_relations(persons_polygons, heads_polygons, cars_polygons, licenses_plates_polygons):    

    # evaluar si la persona tiene cabeza
    for i, person in enumerate(persons_polygons):
        for head in heads_polygons:
            if person.intersects(head):
                union = person.union(head)
                persons_polygons[i] = union
                break
        else:
            break


    persons_cars = []
    for i, person in enumerate(persons_polygons):
        for j, car in enumerate(cars_polygons):
            itersection = person.intersection(car)
            area_porcent = person.area / itersection.area if itersection.area > 0 else 0
            if itersection.area > 0.5 * person.area:
                persons_cars.append({
                    "person": i,
                    "car": j,
                    "area_person_car": round(area_porcent, 2)
                })
            
    for i, person_car in enumerate(persons_cars):
        car = cars_polygons[person_car["car"]]
        person = persons_polygons[person_car["person"]]

        # evaluar cual licencia tiene mas del 50% de su area intercepada por el carro
        min_distance = 1000000
        license_plate_find = None
        for j, license_plate in enumerate(licenses_plates_polygons):
            itersection = license_plate.intersection(car)
            area_porcent = license_plate.area / itersection.area if itersection.area > 0 else 0
            if area_porcent > 0.5:
                distance = car.distance(license_plate)
                if distance < min_distance:
                    min_distance = distance
                    license_plate_find = j
        persons_cars[i]["license_plate"] = license_plate_find

        # evaluar cual cabeza esta mas cerca 
        head_find = None
        min_distance = 1000000
        for j, head in enumerate(heads_polygons):
            distance = car.distance(head)
            if distance < min_distance:
                min_distance = distance
                head_find = j
        persons_cars[i]["head"] = head_find

    return persons_cars



summary = {}
with open("summary.json", "r") as f:
    summary = json.load(f)

w, h = summary["size"]["width"], summary["size"]["height"]
# Crear una imagen de fondo en blanco
fondo = np.zeros((h, w, 3), dtype=np.uint8)

fig, ax = plt.subplots()
ax.imshow(fondo)

for frame in summary["frames"][:]:
    id_frame = frame["frame"]
    persons = frame["person"]
    heads = frame["head"]
    licenses_plates = frame["license_plate"]
    cars = frame["car"]

    cars_polygons = []
    for bbox, conf in cars:
        obj = Polygon([
            (bbox[0], bbox[1]), 
            (bbox[2], bbox[1]), 
            (bbox[2], bbox[3]), 
            (bbox[0], bbox[3])])
        cars_polygons.append(obj)

    licenses_plates_polygons = []
    for bbox, conf in licenses_plates:
        obj = Polygon([
            (bbox[0], bbox[1]), 
            (bbox[2], bbox[1]), 
            (bbox[2], bbox[3]), 
            (bbox[0], bbox[3])])
        licenses_plates_polygons.append(obj)

    persons_polygons = []
    for bbox, conf in persons:
        obj = Polygon([
            (bbox[0], bbox[1]), 
            (bbox[2], bbox[1]), 
            (bbox[2], bbox[3]), 
            (bbox[0], bbox[3])])
        persons_polygons.append(obj)

    heads_polygons = []
    for bbox, conf in heads:
        obj = Polygon([
            (bbox[0], bbox[1]), 
            (bbox[2], bbox[1]), 
            (bbox[2], bbox[3]), 
            (bbox[0], bbox[3])])
        heads_polygons.append(obj)

    
    # evaluar si la persona tiene mas de la mitad del cuerpo en un carro
    persons_cars = find_relations(persons_polygons, heads_polygons, cars_polygons, licenses_plates_polygons)

    if len(persons_cars) > 0:
        print(id_frame, persons_cars)

    # draw persons_cars
    
    for person_car in persons_cars:
        if person_car["person"] is not None:
            print(f'person: {person_car["person"]}')
            person = persons_polygons[person_car["person"]]
            ax.add_patch(mpl_polygon(list(person.exterior.coords), edgecolor='yellow',
                                                linewidth=2, fill=False))

        if person_car["head"] is not None:
            print(f'head: {person_car["head"]}')
            head = heads_polygons[person_car["head"]]
            ax.add_patch(mpl_polygon(list(head.exterior.coords), edgecolor='red',
                                                linewidth=2, fill=False))

        if person_car["car"] is not None:
            print(f'car: {person_car["car"]}')
            car = cars_polygons[person_car["car"]]
            ax.add_patch(mpl_polygon(list(car.exterior.coords), edgecolor='green',
                                                linewidth=2, fill=False))
        
        if person_car["license_plate"] is not None:
            print(f'license_plate: {person_car["license_plate"]}')
            license_plate = licenses_plates_polygons[person_car["license_plate"]]
            ax.add_patch(mpl_polygon(list(license_plate.exterior.coords), edgecolor='blue',
                                                    linewidth=2, fill=False))
    
        print("*"*50)
    #break

ax.set_xlim(0, w)
ax.set_ylim(h, 0)
ax.axis('off')  # No mostrar ejes

plt.show()

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=4)
