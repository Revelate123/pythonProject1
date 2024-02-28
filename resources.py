def key_check(Dictionary, string):
    try:
        output = Dictionary[string]
    except KeyError:
        output = "BLANK"
    return output
