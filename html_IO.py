def write_html(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()


def read_html(file_name):
    f = open(file_name, "r")
    content = f.read()
    f.close()
    return content
