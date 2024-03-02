import socket
import numpy as np
import cv2 as cv

from Connection.tcpServer import TCPServer

class PhotosServer(TCPServer):

    chessboardSize = (9,6)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def __init__(self, ip, port):
        super().__init__(ip, port)

        self.imagesSaved = 0
        self.imageToSave = None
        self.imageWithBoard = None

        self.showingBoard = False

    def _operateOnDataReceived(self, data):
        frame_encoded = np.frombuffer(data, dtype=np.uint8)
        frame = cv.imdecode(frame_encoded, cv.IMREAD_COLOR)
        #inv = cv.flip(frame, 1)
        img = frame.copy()

        if not self.showingBoard:
            cv.imshow('img', img)
        else:
            cv.imshow('img', self.imageWithBoard)

        key = cv.waitKey(1)
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
            cv.imwrite(filename = "imagesForCalibration/calib_img{}.png".format(self.imagesSaved), img=self.imageToSave)
            print("Image {} saved!".format(self.imagesSaved))
            self.showingBoard = False

        elif key == ord('n') and self.showingBoard:
            self.showingBoard = False

        return ""
    
    def close(self):
        super().close()
        cv.destroyAllWindows()
        

        
def main():
    HOSTNAME = socket.gethostname()
    HOST = socket.gethostbyname(HOSTNAME)

    server = PhotosServer(HOST, 5051)
    server.run()

if __name__ == '__main__' : main()