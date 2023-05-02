import numpy as np
import cv2 as cv
import glob
import re
from os import path


def pretty_matrix_print(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# Nota: PSIZE = PATTERN SIZE
images = glob.glob('./imagens/input/*.jpg')
for filepath in images:
    fname = path.basename(filepath)
    # extrair tamanho do tabuleiro do nome da imagem
    [x, y] = re.findall(r'\d+', fname)
    PSIZE = (int(x), int(y))
    # termination criteria
    # variaveis necessarias para funcoes
    objp = np.zeros((PSIZE[1]*PSIZE[0], 3), np.float32)
    objp[:, :2] = np.mgrid[0:PSIZE[0], 0:PSIZE[1]].T.reshape(-1, 2)
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    # pegar imagens do diretorio
    print(f'Processando imagem \'{fname}\'...')
    img = cv.imread(filepath)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, PSIZE, None)
    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, PSIZE, corners2, ret)
        print(f'> Salvando arquivo \'output_{fname}\'...')
        cv.imwrite(f'./imagens/output/cantos_{fname}', img)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        img = cv.imread(filepath)
        h,  w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        # desdistorcer
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # cortar a imagem
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite(f'./imagens/output/arrumada_{fname}', dst)
        print('matriz:')
        pretty_matrix_print(mtx)
        # gerar o experimento
        if fname == '5x7.jpg':
            img = cv.imread('./aha.jpg')
            h,  w = img.shape[:2]
            # newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            # desdistorcer
            dst = cv.undistort(img, mtx, dist, None, newcameramtx)
            # cortar a imagem
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv.imwrite(f'./exp.jpg', dst)
    else:
        print('>>> Falha procurando cantos :(')
