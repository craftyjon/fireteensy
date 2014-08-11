# with open('./teensy-strands.pckl', 'w') as teensy_file:
#     configuration = {}
#     teensy_config = {}
    
#     configuration['leds_per_strut'] = leds_per_strut
#     configuration['struts_per_strand'] = struts_per_strand
#     configuration['teensys'] = teensy_config
#     for teensy in self.teensy_nums:
#         teensy_config[teensy] = {}
#         for strand in self.strands[teensy]:
#             teensy_config[teensy][self.strand_count] = strand
#             self.strand_map[(teensy, strand)] = self.strand_count
#             self.strand_count = self.strand_count + 1
#     pickle.dump(configuration, teensy_file)
#     return True

import pickle
import json

# with open('./teensy-strands.pckl', 'r') as teensy_file:
#     with open ('./ts.json', 'w') as json_file:
#         data = pickle.load(teensy_file)
#         json_file.write(json.dumps(data))

with open('./ts.json', 'r') as json_file:
    with open ('./teensy-strands.pckl', 'w') as teensy_file:
        data = json.load(json_file)
        pickle.dump(data, teensy_file)