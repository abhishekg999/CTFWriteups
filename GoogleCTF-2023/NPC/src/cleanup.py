with open('hint.dot', 'r') as f:
    lines = f.read().split('\n')

print(lines)

with open('actualgraph.dot', 'w+') as f:
    for line in lines:
        if '--' in line:   
            new_line = '    ' + ' -> '.join(line.replace(';', '').replace(' ', '').split('--')[::-1]) + ';'

            f.write(new_line + '\n')
        else:
            f.write(line + '\n')
