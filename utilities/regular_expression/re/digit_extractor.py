import re

def find_digits_in_string(input_string):
  ### 文字列に含まれる最初の数字を抜き出す
  ### \d+ -> 1つ以上の数字
  match = re.search(r'\d+', input_string)

  if match:
    print(f"The first number found in '{input_string}':", match.group())
  else:
    print(f"No numbers were found in '{input_string}'.")

strings = ["test001.dat", "test002.dat", "foge.dat"]

for string in strings:
  find_digits_in_string(string)
