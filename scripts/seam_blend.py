import re
import os
import copy
import math

current_location = os.getcwd()
file_name = r'/blend_test_weave_sr.gcode'
file_location = current_location + r'/../gcode' + file_name


with open(file_location, 'r') as f:
    data = f.read()

seam_blend_start_layer = 4

command_layer_list = [x.split("\n") for x in data.split(';LAYER_CHANGE')]

for i in range(5, len(command_layer_list)-1):

    layer = copy.deepcopy(command_layer_list[i])
    next_layer = copy.deepcopy(command_layer_list[i+1])

    next_z = re.match(r';Z:(.*)', next_layer[1])
    if next_z is None:
        print(i)
    next_z = [float(z_) for z_ in next_z.groups()]
    next_z = 'Z' + str(next_z[0]) + ' '

    last_command = (layer[::-1])[1]
    second_to_last_command = (layer[::-1][2])

    if type(last_command) is not str:
        continue

    if re.match(r'M106', last_command):
        last_command = (layer[::-1])[2]
        second_to_last_command = (layer[::-1][3])

    match = re.match(r'G1 (X.*) (Y.*) (E.*)', last_command)
    prev_match = re.match(r'G1 (X.*) (Y.*) (E.*)', second_to_last_command)

    dx = float(match.groups()[0][1:]) - float(prev_match.groups()[0][1:])
    dy = float(match.groups()[1][1:]) - float(prev_match.groups()[1][1:])
    de = float(match.groups()[2][1:]) - float(prev_match.groups()[2][1:])
    
    total_dist = math.sqrt(dx**2 + dy**2)
    flow_rate = de/total_dist

    dz = 0.5
    new_dist = math.sqrt(dx**2 + dy**2 + dz**2)
    new_flow = flow_rate * new_dist

    print(de, new_flow)
    print(total_dist, new_dist)

    if match is None or prev_match is None:
        print(i)
        continue
    
    out_command = ''
    for group in match.groups():
        if re.match(r'E', group):
            out_command += next_z
        out_command += group
        out_command += ' '
    out_command += '; modified command'


    command_layer_list[i][len(layer)-2] = out_command

out_data = 'LAYER_CHANGE'.join(["\n".join(x) for x in command_layer_list])

#with open('test_output.gcode', 'w') as f:
#    f.write(out_data)
