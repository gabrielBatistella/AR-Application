import numpy as np
import cv2 as cv

from Connection.handler import Handler

class Photor(Handler):

    chessboardSize = (9,6)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def __init__(self):
        super().__init__()

        self.imagesSaved = 0
        self.imageToSave = None
        self.imageWithBoard = None

        self.showingBoard = False

    def __del__(self):
        super().__del__()
        cv.destroyAllWindows()

    def operateOnData(self, data):
        frame_encoded = np.frombuffer(data, dtype=np.uint8)
        frame = cv.imdecode(frame_encoded, cv.IMREAD_COLOR)
        inv = cv.flip(frame, 1)
        img = inv.copy()

        if not self.showingBoard:
            cv.imshow('img', img)
        else:
            cv.imshow('img', self.imageWithBoard)

        key = cv.waitKey(1)
        if key == ord('s'):
            height, width, _ = frame.shape
            print(width," - ",height)

        if key == ord(' ') and not self.showingBoard:
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            ret, corners = cv.findChessboardCorners(gray, self.__class__.chessboardSize, None)
            if ret == True:
                corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), self.__class__.criteria)
                cv.drawChessboardCorners(img, self.__class__.chessboardSize, corners2, ret)

            self.imageToSave = frame.copy()
            self.imageWithBoard = img.copy()
            self.showingBoard = True

        elif key == ord('y') and self.showingBoard:
            self.imagesSaved += 1
            cv.imwrite(filename = "Camera/imagesForCalibration/calib_img{}.png".format(self.imagesSaved), img=self.imageToSave)
            print("Image {} saved!".format(self.imagesSaved))
            self.showingBoard = False

        elif key == ord('n') and self.showingBoard:
            self.showingBoard = False

        return ""