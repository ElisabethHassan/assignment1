import csv


def main():
    with open('admissions_test1.csv', newline="") as f:
        csvreader = csv.reader(f)

        list_1_h = [0, 1, 2, 3, 8] # headers: ['SAT', 'GPA', 'Interest', 'High School Quality', 'in_out']
        list_2_h = [4, 5, 6, 7] # headers: ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4']
        list_1, list_2 = [], []
        student_names = []
        file_chosen_student = open("unsorted_chosen_students.txt", "w")
        file_outliers = open("outliers.txt", "w")
        file_improved = open("chosen_improved.txt", "w")
        file_extra_unsorted = open("unsorted_extra_improved_chosen.txt", "w")

        for line in csvreader:
            student_names.append(line[0])

            line.pop(0) # remove the student's name from list

            sliced_row = [line[h] for h in list_1_h]
            list_1.append(sliced_row)
            sliced_rows = [line[h] for h in list_2_h]
            list_2.append(sliced_rows)


        # encodes the in/out value
        for row in list_1:
            row[4] = encode_in_out(row[4])


        for i in range (2, len(list_1) - 1):
            float_rows = convert_row_type(list_1[i]) # convert row into floats
            student_score = calculate_score(float_rows[0], float_rows[1], float_rows[2], float_rows[3], float_rows[4]) # calculate score


            if student_score >= 6.0:
                # print(student_names[i], student_score)
                file_chosen_student.write(student_names[i] + " " + str(student_score) + "\n")

            if is_outlier(float_rows[0], float_rows[1], float_rows[2]) and student_score >= 5.0:
                file_outliers.write(student_names[i] + " " + str(student_score) + "\n")

            if student_score >= 6.0 or (is_outlier(float_rows[0], float_rows[1], float_rows[2]) and student_score >= 5.0):
                file_improved.write(student_names[i] + " " + str(student_score) + "\n")

            if student_score >= 6.0 or (student_score >= 5.0 and (is_outlier(float_rows[0], float_rows[1], float_rows[2]) or (gpa_checker(list_2[i]) == True) or (grade_improvement(list_2[i]) == True))):
                file_extra_unsorted.write(student_names[i] + " " + str(student_score) + "\n")

        file_chosen_student.close()
        sort_students_by_score("unsorted_chosen_students.txt", "chosen_students.txt")
        file_outliers.close()
        file_improved.close()
        file_extra_unsorted.close()
        sort_students_by_score("unsorted_extra_improved_chosen.txt", "extra_improved_chosen.txt" )


def convert_row_type(row):
    for i in range(0, len(row)):
        row[i] = float(row[i])
    return row

def encode_in_out(state):
    if state == "in":
        return 1
    elif state == "out":
        return 0

def calculate_score(sat, gpa, interest, quality, state):
    score = (.40 * (gpa * 2)) + ((sat // 160) * .30) + (quality * .20) + (interest * .05) + (state * .05)
    score = round(score, 2)
    return score

def is_outlier(sat, gpa, interest_score):
    return (interest_score == 0 or (gpa * 2) - (sat // 160) >= 2) if True else False

def gpa_checker(row):
    row.sort()  # sorts the semester from low to highest
    convert_row_type(row)

    if row[1] - row[0] > 20:
        # print("Student contains class score that is more than two letter grades lower than all other scores.")
        return True
    else:
        # print("Student is good")
        return False

def grade_improvement(row):
    convert_row_type(row)
    for i in range(len(row) - 1):
        if row[i] > row[i+1]:
            return False
    return True

# tells sorted to sort using the value in index one of array (student score)
def get_score(student):
    return student[1]

def sort_students_by_score(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    student_scores = []
    for line in lines:
        name, score = line.rsplit(' ', 1)  # splits from right to separate name and score
        student_scores.append((name, score.strip()))  # remove trailing whitespace

    # sort data by score from high to low
    sorted_student_scores = sorted(student_scores, key=get_score, reverse=True)

    # put sorted score in output file
    with open(output_file, 'w') as file:
        for name, score in sorted_student_scores:
            file.write(f'{name} {score}\n')

main()

