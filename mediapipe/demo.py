import math
import cv2
import mediapipe as mp
import numpy as np

face_lr_threshold = 10
face_ud_threshold = 8
eye_threshold = 0.2
speaking_threshold = 0.08
yawn_threshold = 0.55
near_threshold = 9
far_threshold = 1.65

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def get_facing_directions(img_h, img_w, landmark):
    face_3d = []
    face_2d = []
    for idx, lm in enumerate(landmark):
        if idx in [33, 263, 1, 61, 291, 199]:
            x, y = int(lm.x * img_w), int(lm.y * img_h)
            face_2d.append([x, y])
            face_3d.append([x, y, lm.z])
    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)
    focal_length = 1 * img_w
    cam_matrix = np.array([[focal_length, 0, img_h / 2],
                           [0, focal_length, img_w / 2],
                           [0, 0, 1]])
    dist_matrix = np.zeros((4, 1), dtype=np.float64)
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
    rmat, jac = cv2.Rodrigues(rot_vec)
    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
    x, y, z = angles[0] * 360, angles[1] * 360, angles[2] * 360
    up, left, right, down, forward = False, False, False, False, False
    if abs(x) < face_ud_threshold and abs(y) < face_lr_threshold:
        forward = True
    else:
        up = x > face_ud_threshold
        down = x < -face_ud_threshold
        left = y > face_lr_threshold
        right = y < -face_lr_threshold
    return x, y, z, forward, up, down, left, right


def get_eye_ratio(img_h, img_w, mesh_coords):
    rh_right, rh_left, rv_top, rv_bottom = mesh_coords[33], mesh_coords[133], mesh_coords[159], mesh_coords[145]
    lh_right, lh_left, lv_top, lv_bottom = mesh_coords[362], mesh_coords[263], mesh_coords[386], mesh_coords[
        374]
    rhd = math.sqrt((rh_right[0] - rh_left[0]) ** 2 + (rh_right[1] - rh_left[1]) ** 2)
    rvd = math.sqrt((rv_top[0] - rv_bottom[0]) ** 2 + (rv_top[1] - rv_bottom[1]) ** 2)
    lhd = math.sqrt((lh_right[0] - lh_left[0]) ** 2 + (lh_right[1] - lh_left[1]) ** 2)
    lvd = math.sqrt((lv_top[0] - lv_bottom[0]) ** 2 + (lv_top[1] - lv_bottom[1]) ** 2)
    return max(lvd / lhd, rvd / rhd)


def get_mouth_ratio(img_h, img_w, mesh_coords):
    mh_right, mh_left, mv_top, mv_bottom = mesh_coords[308], mesh_coords[78], mesh_coords[13], mesh_coords[14]
    mhd = math.sqrt((mh_right[0] - mh_left[0]) ** 2 + (mh_right[1] - mh_left[1]) ** 2)
    mvd = math.sqrt((mv_top[0] - mv_bottom[0]) ** 2 + (mv_top[1] - mv_bottom[1]) ** 2)
    return mvd / mhd


def get_face_size(img_h, img_w, mesh_coords):
    fh_right, fh_left, fv_top, fv_bottom = mesh_coords[454], mesh_coords[234], mesh_coords[10], mesh_coords[152]
    fhd = math.sqrt((fh_right[0] - fh_left[0]) ** 2 + (fh_right[1] - fh_left[1]) ** 2)
    fvd = math.sqrt((fv_top[0] - fv_bottom[0]) ** 2 + (fv_top[1] - fv_bottom[1]) ** 2)
    return fhd * fvd / 10000


drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())

                mesh_coords = [(int(point.x * img_w), int(point.y * img_h)) for point in face_landmarks.landmark]
                x, y, z, forward, up, down, left, right = get_facing_directions(img_h, img_w, face_landmarks.landmark)
                eye_ratio = get_eye_ratio(img_h, img_w, mesh_coords)
                mouth_ratio = get_mouth_ratio(img_h, img_w, mesh_coords)
                face_size = get_face_size(img_h, img_w, mesh_coords)

                cv2.putText(image, f'{"Left" if left else ""}{"Right" if right else ""}{"Up" if up else ""}{"Down" if down else ""}{"Forward" if forward else ""}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'{"Eye Closed" if eye_ratio < eye_threshold else "Eye Open"}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, 'Closed' if mouth_ratio < speaking_threshold else ('Speaking' if mouth_ratio < yawn_threshold else 'Yawn'), (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'{"Near" if face_size > near_threshold else ("OK" if face_size > far_threshold else "Far")}', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'x: {np.round(x, 2)}', (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'y: {np.round(y, 2)}', (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'z: {np.round(z, 2)}', (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'i: {np.round(eye_ratio, 2)}', (500, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'm: {np.round(mouth_ratio, 2)}', (500, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)
                cv2.putText(image, f'f: {np.round(face_size, 2)}', (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 127, 127), 2)

        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
