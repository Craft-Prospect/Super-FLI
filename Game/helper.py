import constants

#helper sort function (returns number stripped of money symbol)
def get_number(line):
    return line.split(constants.SYMBOL)[1]

#When game closes, get player high score and store it in file.
def add_highscore(name, score):

    #Ignore invalid data
    if score == None or len(name) == 0:
        return

    #Name is a list of chars from keyboards.py that needs to be joined
    name = ''.join(name)

    #Add name and score to file
    with open('scores.txt', 'a') as f:
        store = (name + " : " + constants.SYMBOL+ str(score))
        f.write("%s\n" % store )

    sorted_lines = ''

    #Resort file
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        sorted_lines = sorted(lines, key=get_number, reverse = True)
    #Stored sorted file
    with open('scores.txt', 'w') as f:
       f.writelines(sorted_lines)
