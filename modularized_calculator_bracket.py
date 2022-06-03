#! /usr/bin/python3

def read_number(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def read_multiply(line, index):
  token = {'type': 'MULTIPLY'}
  return token, index + 1

def read_divide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

def read_left_bracket(line, index):
  token = {'type': 'LEFT'}
  return token, index + 1

def read_right_bracket(line, index):
  token = {'type': 'RIGHT'}
  return token, index + 1



def find_left_bracket(line, index):
  while index < len(line):
    #print(index, line[index])
    if line[index] == '(':
      left_index = index
      right_index = find_left_bracket(line, index + 1)
      index = right_index
      print("left, right", left_index, right_index)
      #answer = evaluate(tokens[left])
      #print(answer)

    elif line[index] == ')':
      index += 1
      return index

    else:
      index += 1

def find_bracket(tokens, index):
  new_tokens = []
  while index < len(tokens):
    if tokens[index]['type'] == 'LEFT':
      left_index = index
      right_index = find_bracket(tokens, index + 1)
      index = right_index
      #print("left, right", left_index, right_index)

      answer = evaluate(tokens[left_index + 1:right_index - 1])
      #print(answer)
      token = {'type': 'NUMBER', 'number': answer}

      #'(1+2)'みたいな式の結果が出たら'3    'にしたいのでtoken_skipで入れ替える
      token_skip = {'type': 'SKIP'}

      tokens[left_index] = token
      for i in range(left_index + 1, right_index):
        tokens[i] = token_skip

    elif tokens[index]['type'] == 'RIGHT':
      index += 1
      return index

    else:
      new_tokens.append(tokens[index])
      index += 1

  return answer




def tokenize(line):
  tokens = []
  #括弧がないと結果が出ないから人工的に最初と最後に括弧を挿入する
  tokens.append({'type': 'LEFT'})

  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '*':
      (token, index) = read_multiply(line, index)
    elif line[index] == '/':
      (token, index) = read_divide(line, index)
    elif line[index] == '(':
      (token, index) = read_left_bracket(line, index)
    elif line[index] == ')':
      (token,index) = read_right_bracket(line, index)
    elif line[index] == ' ':
      index += 1
      continue
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)

  #最後の位置に括弧を挿入する
  tokens.append({'type': 'RIGHT'})
  return tokens


def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  tokens_plus_minus = []  #足し算と引き算を保存して後に処理する

  #まず掛け算と割り算を処理する
  while index < len(tokens):
    #print(index, tokens[index - 1])
    if tokens[index]['type'] == 'NUMBER':
      #もしPLUSとMINUSなら、符号と数字両方ともtokens_plus_minusに保存する
      if tokens[index - 1]['type'] == 'PLUS':
        tokens_plus_minus.append(tokens[index - 1])
        tokens_plus_minus.append(tokens[index])
        #answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        tokens_plus_minus.append(tokens[index - 1])
        tokens_plus_minus.append(tokens[index])

      #もしMULTIPLYとDIVIDEの場合、tokens_plus_minusから最後の数字を取り出して一時的な結果(res_temp)を計算する
      #計算が終わったら、この符号がいらなくなり、res_tempだけを保存すればいい
      elif tokens[index - 1]['type'] == 'MULTIPLY':
        if len(tokens_plus_minus) == 0:
          print('Insufficient Parameters')
          exit(1)
        previous_token = tokens_plus_minus.pop()
        res_temp = previous_token['number'] * tokens[index]['number']
        tokens_plus_minus.append({'type': 'NUMBER', 'number': res_temp})
      elif tokens[index - 1]['type'] == 'DIVIDE':
        if tokens[index]['number'] == 0:
          print('Division by zero is not allowed!!')
          exit(1)
        if len(tokens_plus_minus) == 0:
          print('Insufficient Parameters')
          exit(1)
        previous_token = tokens_plus_minus.pop()
        res_temp = previous_token['number'] / tokens[index]['number']
        tokens_plus_minus.append({'type': 'NUMBER', 'number': res_temp})

      #多分これの判定結果ずっとFalse、NUMBERの後だけ出るから
      #elif tokens[index - 1]['type'] == 'SKIP':
      #  continue

      else:
        print('Invalid syntax')
        exit(1)
    index += 1

  #足し算と引き算を処理する
  index = 1
  while index < len(tokens_plus_minus):
    if tokens_plus_minus[index]['type'] == 'NUMBER':
      if tokens_plus_minus[index - 1]['type'] == 'PLUS':
        answer += tokens_plus_minus[index]['number']
      elif tokens_plus_minus[index - 1]['type'] == 'MINUS':
        answer -= tokens_plus_minus[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1

  #print(tokens_plus_minus)
  return answer


def test(line):
  tokens = tokenize(line)
  actual_answer = find_bracket(tokens, index=0)
  #actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")

  #単一の数字
  test("1")
  test("1.5")
  test("-1.5")

  #足し算と引き算だけ
  test("1+2")
  test("1-5")
  test("1.0+2.1")
  test("1.3-2.1")
  test("1+2-3")
  test("1.5+34.6-100.5")
  test("-90.11-0.89+5.3")

  #掛け算と割り算だけ
  test("2*3")
  test("2/3")
  test("2.5*6")
  test("0.7*2.8")
  test("-2.5*6")
  test("2*3/7")
  test("2/5*3")
  test("2.5*3.6/8.0")

  #+-*/全部ある
  test("3.0+2*4-1/5")
  test("3.0+2*4*4-1/5/0.8")
  test("2.0-3.5*2.6/2/3*5")
  test("4-3/1*0/5")

  #除数は0
  #test("1/0")

  #パラメーター不足
  test('9')
  #test('9*')  #SyntaxError: unexpected EOF while parsing
  #test('/9')
  #test('*9')

  #空白がある
  test("1 ")
  test(" 1")
  test("1 + 2")
  test("1 * 2")
  test("3.0+2 *4*4 - 1/ 5 /0.8")


  #二重以上の括弧がない場合
  test("(1)")
  test("(1+2)")
  test("(1.0+2.3)+4")
  test("3*(4-2)")
  test("4+5*(3-1.2)*(4+2)")

  #二重以上の括弧がある場合
  test("((1))")
  test("((1+2)*(3+4))")
  test("4-3*((5-2)/(3-1.8))")
  test('1+3.5*((2+80/6)-(6-20.7))*3')
  test("(3.0+4*(2-1))/5")
  test("(((1)))")
  test("4*(1+2/(3*(4.5-2.7)))")

  print("==== Test finished! ====\n")


run_test()

#line = '(1+3.5*((2+80/6)-(6-20.7))*3)'
#find_left_bracket(line, index=0)
#tokens = tokenize(line)


#answer = find_bracket(tokens, index=0)
#print("answer", answer)
#answer = evaluate(tokens)
#print(answer)
#print("expected answer", eval(line))

#while True:
#  print('> ', end="")
#  line = input()
#  find_left_bracket(line, index=0)
#  tokens = tokenize(line)
#  answer = find_bracket(tokens, index=0)
#  print("answer = %f\n" % answer)