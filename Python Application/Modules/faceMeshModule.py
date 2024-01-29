"""
Face Mesh Module
Original by: Computer Vision Zone
Check Website: https://www.computervision.zone/

Modified by: Gabriel Takeshi Miyake Batistella
"""

import cv2
import mediapipe as mp

class FaceMeshDetector:
    """
    Face Mesh Detector to find 468 Landmarks using the mediapipe library.
    Helps acquire the landmark points in pixel format
    """

    def __init__(self, staticMode=False, maxFaces=1, minDetectionCon=0.5, minTrackCon=0.5):
        """
        :param staticMode: In static mode, detection is done on each image: slower
        :param maxFaces: Maximum number of faces to detect
        :param minDetectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.staticMode, max_num_faces=self.maxFaces, min_detection_confidence=self.minDetectionCon, min_tracking_confidence=self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw=True):
        """
        Finds face landmarks in BGR Image.
        :param img: Image to find the face landmarks in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        h, w, c = img.shape
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    face.append([px, py, pz])
                faces.append(face)
                
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)

        if draw:
            return faces, img
        else:
            return faces