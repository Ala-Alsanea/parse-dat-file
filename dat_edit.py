

def dat_edit(fileDat):
    lines = fileDat.readlines()
    lines.pop(0)

    with open("DatEdited/"+fileDat.name, "w") as f:
        for line in lines:
            # st.write(line)
            # if line.strip("\n") != delLine:
            f.write(line.decode('utf-8'))
    fileDat.close()
