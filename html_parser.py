import sys, recog

def closetag(html, start):
    pos = start
    while pos < len(html):
        if html[pos] == ">":
            return pos
        pos += 1
    return -1

# Tokenize function
def tokenize(html_content):
    tokens = []
    pos = 0

    while pos < len(html_content):
        if html_content[pos] == "<":
            endpos = closetag(html_content, pos)
            if endpos == -1:
                return ["ERROR"]
            html_tag = html_content[pos:endpos+1].lower()
            if recog.recog(html_tag) == "ACCEPTED":
                tokens.append(html_tag)
            else:
                return ["ERROR"]
            pos = endpos + 1
        else:
            pos += 1

    return tokens

def parser(input,parse_table):
    stack = []
    stack.append('#')
    stack.append('S')
    input.append('EOS')
    i = 0
    while stack[-1]!='#': #looping hingga isi stack teratas adalah #    
        read = input[i] #LL(1)
        top = stack.pop()
        if top in parse_table: #jika top daripada stack berupa non terminal
            if read in parse_table[top]: #kalau 'read/symbol' ada di parse table 
                produksi = parse_table[top][read] # produksinya apa
                if produksi !='':
                    stack.extend(reversed(produksi.split())) #push hasil produksi ke stack secara terbalik
            else:
                return "REJECTED"
        else: #jika top daripada stack berupa terminal
            if top == read:
                i= i+1 #input maju
            else:
                return "REJECTED"
    top = stack.pop()
    if stack == [] and top == "#":
        return "ACCEPTED"
    else:
        return "REJECTED" 

#mendefinisikan grammar dan parser table
grammar = {
    'S': ['<html> A </html>'],
    'A': ['<head> D </head> B','B',''],
    'B': ['<body> C </body>', ''],
    'C': ['<h1> </h1> C', '<p> </p> C', ''],
    'D': ['<title> </title>', ''],
}
parse_table = {
    'S': {
        '<html>': '<html> A </html>',
    },
    'A': {
        '<head>': '<head> D </head> B',
        '<body>': 'B',
        '</html>': '',
    },
    'B': {
        '<body>': '<body> C </body>',
        '</html>': ''
    },
    'C': {
        '<h1>': '<h1> </h1> C', 
        '<p>': '<p> </p> C',
        '</body>': '',
    },
    'D': {
       '<title>': '<title> </title>',
       '</head>': ''
    }
}

def main():
    if len(sys.argv) != 2:
        print("Usage: python html_parser.py <filename>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return

    # Menampilkan isi tag yang ada pada file HTML
    print("Isi file tag pada file HTML:")
    print(html_content)
    print(tokenize(html_content))
    token_html = tokenize(html_content)
    print(parser(token_html,parse_table))

if __name__ == "__main__":
    main()