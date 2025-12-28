import math
import json
import os
import datetime
import numpy as np

class LoadData:
    def parse_data_json(json_data):
        accelData = {
            'x': json_data['x'],
            'y': json_data['y'],
            'z': json_data['z'],
            'timestamp': json_data['accel_timestamp']
        }
        HRData = {
            'HR': json_data['heartRate'],
            'timestamp': json_data['heartRate_timestamp']
        }
        absolute_start_time = json_data.get('absoluteStartTime', None)
        package_start_time = json_data.get('packageStartTime', None)
        userID = json_data.get('userID', None)


        print(f"x length: {len(accelData['x'])}")
        print(f"y length: {len(accelData['y'])}")
        print(f"z length: {len(accelData['z'])}")
        print(f"time length: {len(accelData['timestamp'])}")
        print(f"hr length: {len(HRData['HR'])}")
        print(f"hr time length: {len(HRData['timestamp'])}")

        return accelData, HRData, absolute_start_time, package_start_time, userID

    def write_data_to_files(accelData, HRData, absolute_start_time, package_start_time, docker_root):
        data_dir = os.path.join(docker_root, 'data')

        file_number = datetime.datetime.fromtimestamp(absolute_start_time).strftime('%Y%m%d')

        file_mode = 'a'

        print(f'timestamp absolute: {datetime.datetime.fromtimestamp(package_start_time)}')
        print(f"timestamp relative: {accelData['timestamp'][0]}")
        # if new data session, reset files
        if accelData['timestamp'][0] < 10:
            file_mode = 'w'

        accel_path = os.path.join(data_dir, 'motion', file_number + '_' + str(round(package_start_time)) + '_acceleration.npy')
        # with open(accel_path, file_mode) as file:
        #     for index, i in enumerate(accelData['timestamp']):
        #         newLine = str(i) + ' ' + str(accelData['x'][index]) + ' ' + str(accelData['y'][index]) + ' ' + str(accelData['z'][index]) + '\n'
        #         file.write(newLine)
        accel_timestamp = np.array(accelData['timestamp'])
        x = np.array(accelData['x'])
        y = np.array(accelData['y'])
        z = np.array(accelData['z'])
        accel_data_array = np.vstack([accel_timestamp, x, y, z])
        print(f'accel array shape: {accel_data_array.shape}')
        np.save(accel_path, accel_data_array)

        hr_path = os.path.join(data_dir, 'heart_rate', file_number + '_' + str(round(package_start_time)) + '_heartrate.npy')
        # with open(hr_path, file_mode) as file:
        #     for index, i in enumerate(HRData['timestamp']):
        #         newLine = str(i) + ',' + str(HRData['HR'][index]) + '\n'
        #         file.write(newLine)
        hr_timestamp = np.array(HRData['timestamp'])
        hr = np.array(HRData['HR'])
        hr_data_array = np.vstack([hr_timestamp, hr])
        print(f'hr array shape: {hr_data_array.shape}')
        np.save(hr_path, hr_data_array)

        # labels_path = os.path.join(data_dir, 'labels', file_number + '_' + str(round(package_start_time)) + '_labeled_sleep.txt')
        # with open(labels_path, 'w') as file:
        #     iteration_amount = math.floor(accelData['timestamp'][-1] / 30) + 1

        #     for i in range(iteration_amount):
        #         newLine = str(i * 30) + ' ' + '0' + '\n'
        #         file.write(newLine)

        # if absolute_start_time and package_start_time are the same
        if abs(absolute_start_time - package_start_time) < 1:
            start_path = os.path.join(data_dir, 'start_time', file_number + '_' + str(round(package_start_time)) + '_start_time.json')
            with open(start_path, 'w') as f:
                    json.dump({"startTime": absolute_start_time}, f)

            return [accel_path, hr_path, start_path], absolute_start_time, package_start_time, ['acceleration.npy', 'heartrate.npy', 'start_time.json']
        return [accel_path, hr_path], absolute_start_time, package_start_time, ['acceleration.npy', 'heartrate.npy']
    
    def write_data_to_numpy_array(accelData, HRData, absolute_start_time, package_start_time):
        print(f'timestamp absolute: {datetime.datetime.fromtimestamp(package_start_time)}')
        print(f"timestamp relative: {accelData['timestamp'][0]}")

        accel_timestamp = np.array(accelData['timestamp'])
        x = np.array(accelData['x'])
        y = np.array(accelData['y'])
        z = np.array(accelData['z'])
        accel_data_array = np.vstack([accel_timestamp, x, y, z])
        print(f'accel array shape: {accel_data_array.shape}')

        hr_timestamp = np.array(HRData['timestamp'])
        hr = np.array(HRData['HR'])
        hr_data_array = np.vstack([hr_timestamp, hr])
        print(f'hr array shape: {hr_data_array.shape}')

        if abs(absolute_start_time - package_start_time) < 1:
            start_time = np.array([absolute_start_time])
            return [accel_data_array, hr_data_array, start_time], absolute_start_time, package_start_time, ['acceleration.npy', 'heartrate.npy', 'start_time.npy']
        return [accel_data_array, hr_data_array], absolute_start_time, package_start_time, ['acceleration.npy', 'heartrate.npy']

    def write_apple_sleep_data_to_file(json_data, docker_root):
        sleep_data = json_data['sleepSegments']
        userID = json_data['userID']
        session_start_date = json_data['sessionStartTime']

        timestamp = datetime.datetime.fromtimestamp(session_start_date)

        save_dir = os.path.join(docker_root, 'data', 'apple_sleep')

        sleep_path = os.path.join(save_dir, f"{timestamp.strftime('%Y%m%d')}_{round(session_start_date)}_apple_sleep.json")
        with open(sleep_path, 'w') as f:
            json.dump(sleep_data, f, indent=4)

        return userID, session_start_date, sleep_path
    
    def write_apple_sleep_data_to_json(json_data):
        sleep_data = json_data['sleepSegments']
        user_id = json_data['userID']
        session_start_date = json_data['sessionStartTime']

        sleep_data_bytes = json.dumps(sleep_data).encode('utf-8')
        return sleep_data_bytes, user_id, session_start_date
