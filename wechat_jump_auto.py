# coding: utf-8
import os
import time
import math
from PIL import Image


def pull_screenshot():
    os.system('~/platform-tools/adb shell screencap -p /sdcard/1.png')
    os.system('~/platform-tools/adb pull /sdcard/1.png .')


def backup_screenshot(ts):
    os.system('cp 1.png screenshot_backups/{}.png'.format(ts))


def jump(distance):
    press_time = distance * 1.39
    press_time = max(press_time, 200)
    press_time = int(press_time)
    # 500 1600
    cmd = '~/platform-tools/adb shell input swipe 500 1600 500 1601 ' + str(press_time)
    print cmd
    os.system(cmd)


def find_piece_and_board(im):
    w, h = im.size

    piece_x_sum = 0
    piece_x_c = 0
    piece_y_max = 0
    board_x = 0
    board_y = 0

    for i in range(h):
        for j in range(w):
            pixel = im.getpixel((j, i))
            if (50 < pixel[0] < 60) and (53 < pixel[1] < 63) and (95 < pixel[2] < 110):
                piece_x_sum += j
                piece_x_c += 1
                piece_y_max = max(i, piece_y_max)

    if not all((piece_x_sum, piece_x_c)):
        return 0, 0, 0, 0
    piece_x = piece_x_sum / piece_x_c
    piece_y = piece_y_max - 20

    for i in range(h):
        if i < 300:
            continue
        last_pixel = im.getpixel((0, i))
        if board_x or board_y:
            break
        board_x_sum = 0
        board_x_c = 0

        for j in range(w):
            pixel = im.getpixel((j, i))
            # 修掉脑袋比下一个小格子还高的情况的 bug in 1514552420.png
            if abs(j - piece_x) < 70:
                continue

            # 修掉圆顶的时候一条线导致的小 bug
            if abs(pixel[0] - last_pixel[0]) + abs(pixel[1] - last_pixel[1]) + abs(pixel[2] - last_pixel[2]) > 10:
                board_x_sum += j
                board_x_c += 1
        if board_x_sum:
            board_x = board_x_sum / board_x_c

    board_y = piece_y + abs(board_x - piece_x) * abs(1122 - 831) / abs(813 - 310)

    if not all((board_x, board_y)):
        return 0, 0, 0, 0

    return piece_x, piece_y, board_x, board_y


def main():
    while True:
        pull_screenshot()
        im = Image.open("./1.png")
        # 获取棋子和 board 的位置
        piece_x, piece_y, board_x, board_y = find_piece_and_board(im)
        ts = int(time.time())
        print(ts, piece_x, piece_y, board_x, board_y)
        jump(math.sqrt(abs(board_x - piece_x) ** 2 + abs(board_y - piece_y) ** 2))
        backup_screenshot(ts)
        time.sleep(3)


if __name__ == '__main__':
    main()
