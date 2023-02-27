#!/usr/bin/env python
import re
import sys

variables = []
command_identifier = ['이메일인증.+', '팔테', '두*둣교', '둣-교.+!', '둣~교.+!', '교둣', '영구정지', '엔이', '댓', '엔이꺼라', '리메이크']
param_identifier = ['둣\.+교', '\.+', ',+', '\?', '무름표', '물음표']


class Define:
  def __init__(self, n, *codes):
    self.__name = n
    self.__codes = codes
  def call(self, __codes):
    for r in self.__codes:
      run(r)

class Class:
  def __init__(self, n, fields):
    self.__name = n
    self.__fields = fields
  def make_instance():
    print()
    
  


def setVar(index, value):
  if len(variables) > index:
    variables[index] = value
  else:
    variables.append(value)


def run(code):
  global variables
  global command_identifier
  global param_identifier
  global f

  if code == '':
    quit(print('인터프리터를 종료합니다!'))
  
  #명령어 추출
  for r in range(len(command_identifier)):
    if re.match(command_identifier[r], code):
      command = re.findall(command_identifier[r], code)[0]
      break
  else:
    if code != '':
      raise Exception('정의되지 않은 함수입니다.({} 번째줄)'.format(r - 1))

  #인수 추출
  params = []
  code2 = code
  
  if command == '리메이크':
    params.append(code[4:])
  
  if code2.find(':') != -1:
    for r in param_identifier:
      if re.search(r, code2[:code2.find(':')]):
        params += re.findall(r, code2[:code2.find(':')])
        code2 = re.sub(r, '', code2[:code2.find(':')])
  else:
    for r in param_identifier:
      if re.search(r, code2):
        params += re.findall(r, code2)
        code2 = re.sub(r, '', code2)

  params2 = params
  #인수 중 변수값 불러오기
  for r in params:
    if re.match('둣\.+교', r):
      try:
        params[params.index(r)] = variables[r.count('.') - 1]
      except IndexError:
        raise Exception('선언되지 않은 변수입니다.')
  #print(params)
  params_sum = 0
  for r in params:
    if re.match('\.+', str(r)):
      params_sum += len(r)
    elif re.match(',+', str(r)):
      params_sum -= len(r)
    elif re.match('-?[0-9]+', str(r)):
      params_sum += r
    elif re.match('\?', str(r)):
      try:
        params_sum += int(input(''))
      except ValueError:
        raise ValueError('입력된 값이 정수가 아닙니다.')
    elif re.match('물음표', str(r)) or re.match('무름표', str(r)):
      try:
        params_sum += ord(input(''))
      except TypeError:
        raise TypeError('문자가 아닌 문자열이 입력되었습니다.')
  #print(params_sum)

  #명령어 실행. 명령어 식별자 리스트에 추가했는지 확인!
  if re.match('두*둣교', command):
    variable_index = command.count('두')
    setVar(variable_index, params_sum)
    
  elif re.match('둣-교.+!', command):
    print(params_sum)
    
  elif re.match('둣~교.+!', command):
    print(chr(params_sum))
    
  elif re.match('이메일인증', command):
    if params_sum != 0:
      run(code[code.find(':') + 1:])
      
  elif re.match('교둣\.+', command):
    if mode == '외부 파일 실행':
      return params_sum
    else:
      sys.stdout.write('인터프리터에서는 실행할 수 없는 함수입니다.')
      
  elif re.match('팔테', command):
    try:
      if params_sum != 0:
        for i in range(params_sum):
          run(code[code.find(':') + 1:])
    except RecursionError:
      raise Exception('반복 처리할 내용이 없습니다.')
        
  elif re.match('영구정지', command):
    try:
      removeobj = params2[0]
      variables.pop(str(removeobj).count('.') - 1)
    except Exception:
      raise Exception('인수의 값이 변수가 아닙니다.')
    
  elif re.match('엔이', command):
    with open('./{}'.format(params2[0]), 'a') as f:
      f.write(params2[1])
      
  elif re.match('리메이크', command):
    directory = params[0]
    try:
      f = open('./{}'.format(directory), 'r', encoding='utf8')
      for r in f:
        if r != '소프트웨어 교육의 첫걸음,\n':
          run(r.strip('\n'))
    except FileNotFoundError:
      raise Exception('\'{}\' 파일이 없습니다.'.format(directory))
      
  else:
    raise Exception('정의되지 않은 함수입니다.')


mode = '인터프리터' if len(sys.argv) < 2 else '외부 파일 실행'
if mode == '외부 파일 실행':
  directory = sys.argv[1]
  try:
    f = open('./{}'.format(directory), 'r', encoding='utf8')
    for r in f:
      if r != '소프트웨어 교육의 첫걸음,\n':
        run(r.strip('\n'))
    quit()
  except FileNotFoundError:
    raise Exception('\'{}\' 파일이 없습니다.'.format(directory))

print('둣-랭 인터프리터 By 파이썬.')
print('박새 제작')
print('엔터를 눌러 종료')

code = input('> ')
if code != '소프트웨어 교육의 첫걸음,':
  if code == '':
    quit(print('인터프리터를 종료합니다!'))
  else:
    raise Exception('소프트웨어 교육의 첫걸음, 둣교')

code = None
while code != '':
  code = input('> ')
  run(code)
quit()
