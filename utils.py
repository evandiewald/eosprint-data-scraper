def parse_data(hatch_data):
    parsed = []
    lines = hatch_data.splitlines()
    for i in range(len(lines)):
        if len(lines[i]) > 0:
            label = ''
            myval = None
            word_list = lines[i].split()
            for j in range(len(word_list)):
                if myval is None:
                    try:
                        myval = float(word_list[j])
                    except ValueError:
                        label += word_list[j]
                else:
                    continue
            if myval is not None:
                parsed.append([label, myval])
    return dict(parsed)

