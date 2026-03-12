from djitellopy import Tello
import time
import cv2
from ultralytics import YOLO


def go_to_height(target_height):
    time.sleep(1)
    distance_to_ground = tello.get_distance_tof()
    difference = target_height - distance_to_ground
    if difference < 0:
        tello.move_down(abs(difference))
    else:
        tello.move_up(difference)


def align_to_mission_pad():
    try:
        # move by x, y, z amount
        tello.go_xyz_speed(
            -tello.get_mission_pad_distance_x(),  # x
            -tello.get_mission_pad_distance_y(),  # y
            0,  # z
            10,  # speed (10-100)
        )
    except Exception:
        pass


def measure_hdb_height(drone_height):
    time.sleep(1)
    distance_to_hdb = tello.get_distance_tof()
    hdb_height = drone_height - distance_to_hdb
    return hdb_height


def construction_challenge():
    tello.takeoff()
    time.sleep(1)
    drone_height = 200
    go_to_height(drone_height)
    # todo: move to first hdb
    height = measure_hdb_height(drone_height)
    print("First HDB: ", height)
    # todo: move to second hdb
    height = measure_hdb_height(drone_height)
    print("Second HDB: ", height)
    # todo: move to third hdb
    height = measure_hdb_height(drone_height)
    print("Third HDB: ", height)
    # todo: move to fourth hdb
    height = measure_hdb_height(drone_height)
    print("Fourth HDB: ", height)
    # todo: instead of printing out, might want to write to a file


def read_qr(out_file):
    tello.set_video_direction(Tello.CAMERA_FORWARD)
    if not tello.stream_on:
        tello.streamon()
        time.sleep(1)
    tello.get_frame_read()
    time.sleep(1)
    # try to read frames until valid frame received
    while True:
        frame = tello.get_frame_read().frame
        if not (frame is None or frame.size == 0):
            break
    # cv2.imwrite(out_file, frame)
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(frame)
    # print(points)
    if points is not None and data.isdigit():
        return int(data)
    else:
        return None


def ai_challenge():
    tello.takeoff()
    time.sleep(1)
    # todo: measure qr height and update the value below
    qr_height = 200
    go_to_height(qr_height)
    sum_of_qr = 0
    # todo: move to qr code 1
    sum_of_qr += read_qr("D:\qr1.jpg")
    # todo: move to qr code 2
    sum_of_qr += read_qr("D:\qr2.jpg")
    # todo: move to qr code 3
    sum_of_qr += read_qr("D:\qr3.jpg")
    # todo: move to qr code 4
    sum_of_qr += read_qr("D:\qr4.jpg")
    if sum_of_qr > 10:
        pass
        # todo: land at a1
    else:
        pass
        # todo: land at a2


def detect_mission_pad():
    tello.enable_mission_pads()
    tello.set_mission_pad_detection_direction(0)
    align_to_mission_pad()
    for i in range(3):
        mission_pad = tello.get_mission_pad_id()
        if mission_pad is not None:
            break
        time.sleep(1)
    tello.disable_mission_pads()
    if mission_pad >= 1:
        return mission_pad
    else:
        return None


def land_if_5(value):
    if value == 5:
        raise Exception()  # jumps to cleanup codes in the 'finally' block


def delivery_challenge():
    tello.takeoff()
    time.sleep(1)
    go_to_height(120)
    # todo: move to mission pad 1
    mp = detect_mission_pad()
    land_if_5(mp)
    # todo: move to mission pad 2
    mp = detect_mission_pad()
    land_if_5(mp)
    # todo: move to mission pad 3
    mp = detect_mission_pad()
    land_if_5(mp)
    # todo: move to mission pad 4
    mp = detect_mission_pad()
    land_if_5(mp)


try:
    tello = Tello()
    tello.connect()
    battery_level = tello.get_battery()
    if battery_level < 20:
        raise Exception("Battery too low!")
    print("Battery Level: ", tello.get_battery())

    # construction_challenge()
finally:
    tello.end()
