import random
import xml.etree.ElementTree as ET

# 1. Настройки
NETWORK_FILE = r'C:\Users\Eldos\OneDrive\Рабочий стол\final\network_final_combined.xml'
OUTPUT_FILE  = r'C:\Users\Eldos\OneDrive\Рабочий стол\final\population_500.xml'
NUM_PEOPLE = 500

# districts in Almaty
districts = {
    'Arena':     {'x': (645094, 648258), 'y': (4789036, 4794375), 'links': []}, #places near the Almaty Arena
    'Almaly':    {'x': (652000, 657300), 'y': (4788700, 4791700), 'links': []}, 
    'Bostandyk': {'x': (652000, 656100), 'y': (4778000, 4789000), 'links': []}, 
    'work Bost': {'x': (652567, 659041), 'y': (4783151, 4790652), 'links': []}, #city center with most of the offices
    'Auezov':    {'x': (649100, 651300), 'y': (4786000, 4791200), 'links': []}, 
    'Alatau':    {'x': (644000, 654300), 'y': (4788000, 4799000), 'links': []}, 
    'Medeu':     {'x': (652500, 663100), 'y': (4777000, 4793500), 'links': []}, 
    'Turksib':   {'x': (654600, 670000), 'y': (4791000, 4800000), 'links': []}, 
    'Zhetysu':   {'x': (650600, 656700), 'y': (4790000, 4798600), 'links': []}, 
    'Nauryzbai': {'x': (647000, 649200), 'y': (4775000, 4790100), 'links': []}, 
    'Other':     {'x': (634200, 642210), 'y': (4775600, 4798000), 'links': []} #from countryside
}

node_coords = {} 

print("Step 1: finding nodes...")
for event, elem in ET.iterparse(NETWORK_FILE, events=('start',)):
    if elem.tag == 'node':
        n_id = elem.get('id')
        node_coords[n_id] = (float(elem.get('x')), float(elem.get('y')))
        elem.clear()

print(f"Step 2: distributing links...")
for event, elem in ET.iterparse(NETWORK_FILE, events=('start',)):
    if elem.tag == 'link':
        l_id = elem.get('id')
        from_node = elem.get('from')
        
        if from_node in node_coords:
            x, y = node_coords[from_node]
            # Сортируем линк в район
            for d_name, d_info in districts.items():
                if d_info['x'][0] <= x <= d_info['x'][1] and d_info['y'][0] <= y <= d_info['y'][1]:
                    d_info['links'].append(l_id)
                    break
        elem.clear()

for name in districts:
    print(f"District {name}: {len(districts[name]['links'])} links")

dist_names = [n for n in districts if districts[n]['links']]
h_weights = [0.047, 0.081, 0.129, 0.007, 0.123, 0.079, 0.102, 0.096, 0.017, 0.089, 0.23] 
w_weights = [0.066, 0.169, 0.09, 0.12, 0.075, 0.06, 0.143, 0.104, 0.039, 0.064, 0.07]

print(f"There are: {len(dist_names)} districts")


# --- ЗАПИСЬ ФАЙЛА (ВСТАВИТЬ ВМЕСТО СТАРОГО БЛОКА WITH OPEN) ---
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd">\n')
    f.write('<plans name="Plans_Test1">\n')

    for i in range(1, NUM_PEOPLE):
        role = random.random()
        h_dist = random.choices(dist_names, weights=h_weights)[0]
        h_link = random.choice(districts[h_dist]['links'])

        # 1. time to leave the house
        if role < 0.60: # workers and first shift students
            h_end = f"{random.randint(7, 8):02d}:{random.randint(0, 59):02d}:00"
        elif role < 0.9: # second shift students and workers
            h_end = f"{random.randint(12, 13):02d}:{random.randint(0, 59):02d}:00"
        else: # others
            h_end = f"{random.randint(6, 10):02d}:{random.randint(0, 59):02d}:00"

        f.write(f'  <person id="person_{i}">\n    <plan selected="yes">\n')
        f.write(f'      <act type="home" link="{h_link}" end_time="{h_end}" />\n')

        # --- ACTIVITIES LOGIC ---
        if role < 0.50: # workers
            w_dist = random.choices(dist_names, weights=w_weights)[0]
            w_link = random.choice(districts[w_dist]['links'])
            f.write('      <leg mode="car" />\n')
            # dinner time
            l_start = f"{random.randint(11, 12):02d}:{random.randint(0, 59):02d}:00"
            f.write(f'      <act type="work" link="{w_link}" end_time="{l_start}" />\n')
            f.write('      <leg mode="car" />\n')
            l_end = f"{random.randint(12, 13):02d}:{random.randint(0, 59):02d}:00"
            f.write(f'      <act type="leisure" link="{w_link}" end_time="{l_end}" />\n')
            f.write('      <leg mode="car" />\n')
            w_end = f"{random.randint(16, 17):02d}:{random.randint(0, 59):02d}:00"
            f.write(f'      <act type="work" link="{w_link}" end_time="{w_end}" />\n') #work end

        elif role < 0.80: # students
            e_dist = 'work Bost' if random.random() < 0.35 else random.choice(['Nauryzbai', 'Bostandyk', 'Alatau', 'Arena']) #most of the universities and schools
            e_link = random.choice(districts[e_dist]['links'])
            f.write('      <leg mode="car" />\n')
            u_end = f"{random.randint(15, 16):02d}:{random.randint(0, 59):02d}:00"
            f.write(f'      <act type="edu" link="{e_link}" end_time="{u_end}" />\n')
            
            # partying
            if random.random() < 0.6:
                f.write('      <leg mode="car" />\n')
                lei_dist = random.choice(['Bostandyk', 'work Bost', 'Arena', 'Medeu'])
                lei_link = random.choice(districts[lei_dist]['links'])
                lei_end = f"{random.randint(17, 18):02d}:{random.randint(0, 59):02d}:00"
                f.write(f'      <act type="leisure" link="{lei_link}" end_time="{lei_end}" />\n')

        else: # others
            h1_link = random.choice(districts[h_dist]['links'])
            f.write('      <leg mode="car" />\n')
            any_end = f"{random.randint(11, 12):02d}:{random.randint(0, 59):02d}:00"
            f.write(f'      <act type="hospital" link="{h1_link}" end_time="{any_end}" />\n')
            h2_link = random.choice(districts[h_dist]['links'])
            end = f"{random.randint(13, 14):02d}:{random.randint(0, 59):02d}:00"
            f.write(f'      <act type="leisure" link="{h2_link}" end_time="{any_end}" />\n')

        # way to home for all
        f.write('      <leg mode="car" />\n')
        f.write(f'      <act type="home" link="{h_link}" />\n')
        f.write('    </plan>\n  </person>\n')

    f.write('</plans>\n')



print("File is successfully created.")
