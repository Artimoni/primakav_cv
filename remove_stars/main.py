import numpy as np
import socket

server_ip = "84.237.21.36"
server_port = 5152

def get_neighbors(y, x):
    return [(y - 1, x), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x + 1), (y + 1, x), (y, x - 1), (y, x + 1),  (y + 1, x - 1)]

def check_neighbors(arr, y, x):
    for neighbor in get_neighbors(y, x):
        ny, nx = neighbor
        if 0 <= ny < arr.shape[0] and 0 <= nx < arr.shape[1]:
            if arr[y][x] <= arr[ny][nx]:
                return False
    return True

def receive_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data

def group_close_points(points, threshold=2):
    groups = []
    for p in points:
        added = False
        for group in groups:
            if any(np.hypot(p[0] - gp[0], p[1] - gp[1]) <= threshold for gp in group):
                group.append(p)
                added = True
                break
        if not added:
            groups.append([p])
    return [group[0] for group in groups]#взятие первой точки из каждой группы

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
    connection.connect((server_ip, server_port))
    for _ in range(10):
        connection.send(b"get")
        received_bytes = receive_all(connection, 40002)

        image = np.frombuffer(received_bytes[2:40002], dtype="uint8").reshape(received_bytes[0], received_bytes[1])

        max_coords = []
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                if check_neighbors(image, y, x):
                    max_coords.append((y, x))

        filtered_coords = group_close_points(max_coords)

        if len(filtered_coords) < 2:
            result = 0.0
        else:
            p1, p2 = filtered_coords[:2]
            result = np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

        connection.send(f"{round(result, 1)}".encode())
        print(connection.recv(20))

    connection.send(b"beat")
    print(connection.recv(20))
