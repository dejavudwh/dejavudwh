import utils
import string


CONFIG = {}

def update_readme(template):
    lines = []
    rows = 0
    flag = False
    is_old = False
    with open('README.md', 'r', encoding='UTF-8') as f:
        for line in f:
            if not is_old:
                lines.append(line)
            if not flag:
                rows = rows + 1
            if 'COMMITS-LIST:START' in line:
                flag = True
                is_old = True
            elif 'COMMITS-LIST:END' in line:
                lines.append('\n' + line)
                is_old = False
    lines.insert(rows, template)      
    content = ''.join(lines)
    file = open('README.md', 'w', encoding='UTF-8')
    file.write(content)
    file.close()


if __name__ == '__main__':
    global CONIFG
    CONFIG = utils.read_config()