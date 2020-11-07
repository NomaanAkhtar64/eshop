def get_ext(filename):
    out = ""
    len_ = len(filename)
    for i in range(len_):
        char = filename[len_ - (i + 1) :]

        if char == ".":
            out[filename[len_ - i :]]
            break
    return out


print(get_ext("Test.test"))