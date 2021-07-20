import argparse
import os

def words_gen(s):
    words = set()
    words.add(s)

    words.add(s.lower())
    #words.add(s.upper())
    
    s = s.lower()
    
    s_new = s[0].upper() + s[1:]
    words.add(s_new)
    
    #s_new = s[:-1] + s[-1].upper()
    #words.add(s_new)
    
    s_new = s[0].upper() + s[1:-1] + s[-1].upper()
    words.add(s_new)
    
    #words.add(s[::-1])
    
    return words


def pass_gen(words, cur_s='', lvl=0, max_lvl=2, sep=''):
    for i in words:
        if i != '' and i.lower() in cur_s.lower():
            continue
        for wv in words[i]:
            if lvl < max_lvl:
                yield from pass_gen(words, cur_s + sep * min(lvl, 1) + wv, lvl + 1, max_lvl)
            else:
                yield cur_s + sep * min(lvl, 1) + wv
                    


def main():
    parser = argparse.ArgumentParser(description='argparse')
    parser.add_argument('-pf', '--passfile', metavar='', type=str, help='Pass file to add')
    args = parser.parse_args()
    
    words = {}
    q = input()
    while q:
        words[q] = words_gen(q)
        q = input()
    words[''] = set([''])
    
    password_list = set()
    for i, password in enumerate(pass_gen(words)):
        password_list.add(password)
    if args.passfile and os.path.exists('Passwords/' + args.passfile):
        with open('Passwords/' + args.passfile, 'r') as f:
            print('Adding passfile...')
            for password in f:
                password_list.add(password.strip())
    
    with open('my_words.txt', 'w') as f:
        for i, password in enumerate(password_list):
            print(f'\rIter\t{i}', end='') 
            print(password, file=f)
            
        


if __name__ == '__main__':
    main()
