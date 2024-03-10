import logging


def check_Ki(package):
    path = package.get_path()
    # print(path)
    s = path[0]
    d = path[-1]
    other = path[1:-1]

    for i in other:
        if s.Ki[package][i] == i.Ki[package][s] and d.Ki[package][i] == i.Ki[package][s]:
            ...
        else:
            logging.error('false')
            exit(0)