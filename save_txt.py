def data_time(a, b, c, d):
    if d == '':
        d = '.'
    file = f'{a}\t\t{b}\n'
    with open(f'{d}/ptc历史{c}.txt', 'a', encoding='utf-8')as f:
        f.write(file)
