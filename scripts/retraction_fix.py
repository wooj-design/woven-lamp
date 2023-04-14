

file_name = ""

retraction = ""

deretraction = ""

with open(file_name) as f:
    layers = f.read.split(';START_LAYER')

output = []

for layer in layers:
    layer += retraction
    lines = layer.split('\n')
    if lines[:-1] != ";END_LAYER":
        output += '\n'.join(lines)
    else:
        lines.insert(1, deretraction)
        output += '\n'.join(lines)

output = ';START_LAYER'.join(output)
