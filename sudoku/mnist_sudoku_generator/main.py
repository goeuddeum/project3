from Generator import *
import sudoku, mnist, datetime
import numpy as np
import matplotlib.pyplot as plt

start_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

# get number image from MNIST dataset
# mnist.py로 부터 가져오는 것 
test_images = mnist.test_images()
test_labels = mnist.test_labels()

# 값을 이미지로 만드는 함수 
# num에 1이라는 숫자를 넣으면 mnist에서 랜덤하게 1을 찾는데 매번 다르게 찾는다. 
def get_number_img(num, background=240):
  # 조건에 맞는 배열의 인덱스를 반환 여기서는 num과 똑같은 레이블의 인덱스를 반환 
  idxs = np.where(test_labels==num)[0]
  # 배열값중에 랜덤한 위치의 값을 반환 
  idx = np.random.choice(idxs, 1)
  # 이미지 형태를 img변수로 넘겨준다.
  img = test_images[idx].reshape((28, 28)).astype(np.int)
  # 글씨는 원래는 검정색인데, 흰색으로 하기위해 240에서 이미지를 빼기로 해서 흰색으로 만들어 준다.
  img = background - img # make background white
  return img

# 수도쿠 게임 보드를 만드는 함수 
def create_board(s):
  # 28*9 , 28*9의 배열을 만든다. mnist 숫자 이미지 한개의 가로 사이즈는 28, 스토쿠의 가로는 숫자가 9개이므로
  board_img = np.empty((28*9, 28*9))
  # 배열을 흰색으로 채워준다. 
  board_img.fill(255)

  for i in range(9):
    for j in range(9):
      num = s[9 * i + j]
      
      if num is not None:
        # get_number_img는 배열에 해당하는 숫자 이미를 넣는 함수 
        num_img = get_number_img(num)
        rows = slice(28*(i%10), 28*((i+1)%10))
        cols = slice(28*(j%10), 28*((j+1)%10))
        board_img[rows, cols] = num_img
  # board의 이미지를 반환한다. 
  return board_img

# visualize and save images
# 위에서 board_imgs를 받으면 실제로 그래주는 함수 
def visualize(board_imgs):
  for key, img in board_imgs.items():
    fig = plt.figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)

    # matplotlib로 수도쿠를 그리는 부분
    major_ticks = np.arange(0, 28*9, 28*3)
    minor_ticks = np.arange(0, 28*9, 28)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    ax.grid(True, which='both', color='k', linestyle='-')
    ax.grid(which='major', alpha=0.6, linewidth=1.5)
    ax.grid(which='minor', alpha=0.2)

    plt.xlim(0, 28*9)
    plt.ylim(28*9, 0)
    plt.imshow(img)
    plt.gray()
    # 이미지를 저장하는 부분
    plt.savefig('result/%s_%s.png' % (key, start_time))
  plt.show()

# main
# generate
gen = Generator()
# Generator를 generate 해주면 quiz와 answer를 반환하고 레벨을 지정할 수 있다.
quiz, answer = gen.generate(0) # 0-1-2-3
quiz = gen.get(quiz)
answer = gen.get(answer)

# another solver (sometimes not working properly)
# grid = sudoku.Grid(quiz)
# print("%s\n\n" % grid)
# grid.solve()
# print("\n%s\n" % grid)

quiz_img = create_board(quiz)
answer_img = create_board(answer)

visualize({
  'quiz': quiz_img,
  'answer': answer_img
})
