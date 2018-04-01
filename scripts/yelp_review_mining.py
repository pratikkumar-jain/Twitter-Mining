import json

# File Path : Change accordingly
filename = "/Users/pratik/Downloads/dataset/review.json"
output_text = []


# function to read a review and append it to the list
def filereader(line):
    gdfJson = json.loads(line)
    out = gdfJson['text'].replace('\n', '')
    output_text.append(out)


with open(filename, 'r') as f:
    for line in f:
        filereader(line)