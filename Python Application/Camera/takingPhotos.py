import cv2 as cv

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

chessboardSize = (9,6)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

imagesSaved = 0
imageToSave = None
imageWithBoard = None

showingBoard = False

while True:
    if not showingBoard:
        check, frame = camera.read()
        inv = cv.flip(frame, 1)
        img = inv.copy()

        cv.imshow('img', img)
    else:
        cv.imshow('img', imageWithBoard)

    key = cv.waitKey(1)
    if key == ord(' ') and not showingBoard:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        if ret == True:
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            cv.drawChessboardCorners(img, chessboardSize, corners2, ret)

        imageToSave = frame.copy()
        imageWithBoard = img.copy()
        showingBoard = True

    elif key == ord('y') and showingBoard:
        imagesSaved += 1
        cv.imwrite(filename = "imagesForCalibration/calib_img{}.png".format(imagesSaved), img=imageToSave)
        print("Image {} saved!".format(imagesSaved))
        showingBoard = False

    elif key == ord('n') and showingBoard:
        showingBoard = False

    elif key == ord('q'):
        camera.release()
        cv.destroyAllWindows()
        break