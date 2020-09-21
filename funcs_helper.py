from os import path


def remove_hash_sign(x):
    if type(x) == str:
        x = x.replace('#', '%23')
    else:
        x = [i.replace('#', '%23') for i in x]

    return x


def cookie_getter():
    # Goes up two directory levels
    parent_dir = path.dirname(path.dirname(__file__))

    # Append subfolder and file within to parent_dir
    cookie_path = path.join(parent_dir, 'cod_cookie/sso_cookie.txt')

    with open(cookie_path) as cookie_file:
        cookie_value = cookie_file.read()

    return cookie_value
