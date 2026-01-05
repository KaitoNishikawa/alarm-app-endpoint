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
        user_id = json_data.get('userID', None)
        is_last = json_data.get('isLast', False)


        print(f"x length: {len(accelData['x'])}")
        print(f"y length: {len(accelData['y'])}")
        print(f"z length: {len(accelData['z'])}")
        print(f"time length: {len(accelData['timestamp'])}")
        print(f"hr length: {len(HRData['HR'])}")
        print(f"hr time length: {len(HRData['timestamp'])}")

        return accelData, HRData, absolute_start_time, package_start_time, user_id, is_last
    
    def parse_prediction_json(json_data):
        user_id = json_data.get('userID', None)
        absolute_start_time = json_data.get('absoluteStartTime', None)

        session_id = datetime.datetime.fromtimestamp(round(absolute_start_time)).strftime('%Y%m%d_%H%M%S')

        return user_id, session_id
    
    def write_data_to_numpy_array(accelData, HRData, absolute_start_time, package_start_time):
        print(f'timestamp absolute: {datetime.datetime.fromtimestamp(package_start_time)}')
        print(f"timestamp relative: {accelData['timestamp'][0]}")

        accel_timestamp = np.array(accelData['timestamp'])
        x = np.array(accelData['x'])
        y = np.array(accelData['y'])
        z = np.array(accelData['z'])
        accel_data_array = np.column_stack([accel_timestamp, x, y, z])
        print(f'accel array shape: {accel_data_array.shape}')

        hr_timestamp = np.array(HRData['timestamp'])
        hr = np.array(HRData['HR'])
        hr_data_array = np.column_stack([hr_timestamp, hr])
        print(f'hr array shape: {hr_data_array.shape}')

        if abs(absolute_start_time - package_start_time) < 1:
            start_time = np.array([absolute_start_time])
            return [accel_data_array, hr_data_array, start_time], absolute_start_time, package_start_time, ['acceleration.npy', 'heartrate.npy', 'start_time.npy']
        return [accel_data_array, hr_data_array], absolute_start_time, package_start_time, ['acceleration.npy', 'heartrate.npy']
    
    def write_apple_sleep_data_to_json(json_data):
        sleep_data = json_data['sleepSegments']
        user_id = json_data['userID']
        session_start_date = json_data['sessionStartTime']

        sleep_data_bytes = json.dumps(sleep_data).encode('utf-8')
        return sleep_data_bytes, user_id, session_start_date
