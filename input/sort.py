import json
import sys

def sort(input):
    return sorted(input)

if __name__ == '__main__':
    j = sys.argv[1]
    input = json.loads(j)
    output = sort(input)
    print(json.dumps(output))