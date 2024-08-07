import math
import numpy as np
import cv2 as cv
import glob

####################### OBJETO QUE GUARDA INFORMAÇÃO DA CALIBRAÇÃO ###########################

class CalibrationInfo:
    def __init__(self, calib_source):
        calib_data = np.load(calib_source)

        self.camMatrix = calib_data["camMatrix"]
        self.distCof = calib_data["distCoef"]
        self.rVector = calib_data["rVector"]
        self.tVector = calib_data["tVector"]

        self.w = 2*self.camMatrix[0][2]
        self.h = 2*self.camMatrix[1][2]

        self.fovX = 2*math.atan2(self.w, 2*self.camMatrix[0][0])
        self.fovY = 2*math.atan2(self.h, 2*self.camMatrix[1][1])



def main():

############################## ENCONTRAR PONTOS DO TABULEIRO #################################

    chessboardSize = (9,6)
    frameSize = (1280,720)

    # Termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    size_of_chessboard_squares_mm = 25.5
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob("imagesForCalibration/*.png")

    for image in images:
        img = cv.imread(image)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret == True:

            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
            cv.imshow("img", img)
            cv.waitKey(400)

    cv.destroyAllWindows()



####################################### CALIBRAÇÃO ###########################################

    ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

    print(cameraMatrix)
    print(dist)



################################### ERRO DE CALIBRAÇÃO #######################################

    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error

    print("Total Error: ", mean_error/len(objpoints))

    print("Calibration finished")



################################# SALVANDO EM UM ARQUIVO #####################################

    print("Saving the data into one files using numpy")
    np.savez(
        "calib_results/calculatedValues.npz",
        camMatrix = cameraMatrix,
        distCoef = dist,
        rVector = rvecs,
        tVector = tvecs,
    )



if __name__ == '__main__' : main()