#parsarea documentului
def parse_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    sections = {}
    current_section = None
    current_lines = []

#procesarea fiecarei linii din fisier
    for line in lines:
        line = line.strip()
#ignoram liniile goale si comentariile(ie liniile care incep cu #)
        if not line or line.startswith("#"):
            continue
#o sectiune incepe cu un nume urmat de ":"
        if line.endswith(":"):
            current_section = line[:-1]
            current_lines = []
#o sectiune se termina cu "end"
        elif line.lower() == "end":
            if current_section:
                sections[current_section] = current_lines.copy()
                current_section = None
                current_lines = []

        elif current_section:
            current_lines.append(line)

    return sections


