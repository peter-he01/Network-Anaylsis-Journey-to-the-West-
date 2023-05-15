import networkx as nx
import re
import matplotlib.pyplot as plt
import pinyin


# Opening raw text file
with open('west_text.txt', 'r', encoding='utf8') as file:
    west_text = file.read()

west_text = west_text.replace("\n","")
                              
with open('char_place.txt', 'r', encoding='utf8') as file:
    character = file.read().split("\n")

# Create a dictionary to map character names to unique IDs
name_to_id = {}
for i, char in enumerate(character):
    name_to_id[char] = i

character_regex = "|".join(character)

# Define the distance of the text window for co-occurrence
distance_in_text = 100

network_dictionary = {}

# Iterate over the first two characters ([:2]) from the character list
for character_name in character:
    # Find the starting indices of character occurrences in the text
    results = re.finditer(character_name, west_text)
    results = [r.start() for r in results]
    for result in results:
        text_window = west_text[result - distance_in_text:result + distance_in_text]
        co_occuring_char = re.findall(character_regex, text_window)
        co_occuring_char = [side_char for side_char in co_occuring_char if side_char != character_name]

        if character_name not in network_dictionary:
            network_dictionary[character_name] = {}

        for side_char in co_occuring_char:
            if side_char not in network_dictionary[character_name]:
                network_dictionary[character_name][side_char] = 1
            else:
                network_dictionary[character_name][side_char] += 1

G = nx.Graph()

edges_string = []

# Create nodes and edges in the graph
for character_name in character:
    character_id = name_to_id[character_name]
    G.add_node(character_id, name=character_name)

    if character_name in network_dictionary:
        character_edges = network_dictionary[character_name]

        for side_char, edge_weight in character_edges.items():
            side_character_id = name_to_id[side_char]
            G.add_edge(character_id, side_character_id, weight=edge_weight)
            edges_string.append(f"{character_id}\t{side_character_id}\t{edge_weight}\tUndirected")

# node spreadsheet (ID, name of character)

with open('westnodes_place.tsv', 'w', encoding='utf8') as wf:
    wf.write('ID\tName\tPinyin\n')
    wf.write("\n".join([f"{i}\t{character_name}\t{pinyin.get(character_name)}" for i, character_name in enumerate(character)]))

# edge spreadsheet (source targer weight)

with open('westedges_place.tsv', 'w', encoding='utf8') as wf:
    wf.write('Source\tTarget\tWeight\tType\n')
    wf.write("\n".join(edges_string))

