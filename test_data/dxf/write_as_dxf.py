if __name__ == "__main__":
    with open("an_output", 'r', encoding='utf8') as a_file:
        with open("an_output.dxf", 'w') as a_dxf:
            a_dxf.write(''.join([line.replace('\\n', '\n').replace('\\', '') for line in a_file.readlines()])[2:-1])