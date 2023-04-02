import os


def dat_edit(fileDat):
    """
    drop and return the first line of the file and write it to DatEdited dir 
    """
    lines = fileDat.readlines()
    first_line = lines.pop(0)

    try:
        os.mkdir('DatEdited')
    except OSError:
        pass

    with open("DatEdited/"+fileDat.name, "w") as f:
        for line in lines:
            # st.write(line)
            # if line.strip("\n") != delLine:
            f.write(line.decode('utf-8'))
    fileDat.close()
    return first_line
