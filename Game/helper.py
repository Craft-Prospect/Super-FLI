
#helper sort function
def get_number(line):
    return line.split('£')[1]

#When game closes, get player high score and store it in file. Will be included in states with Ibrahim's program
def add_high_score(name, score):
    #Add name to file

    if score == None or len(name) == 0:
        return

    name = ''.join(name)

    with open('scores.txt', 'a') as f:
        store = (name + " : £" + str(score))
        f.write("%s\n" % store )

    sorted_lines = ''

    #Sort file
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        sorted_lines = sorted(lines, key=get_number, reverse = True)
    #Stored sorted file
    with open('scores.txt', 'w') as f:
       f.writelines(sorted_lines)
