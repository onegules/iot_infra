from iot_infra.proto.sensors.v1.sensors.pb2 import Event, Sensors

from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import random
import numpy as np
from scipy.stats import skewnorm
from sklearn.preprocessing import MinMaxScaler

NUM_DATA_POINTS = 1000
NUM_UNITS = 3

class Data:
    datetime_range = ["2024-05-12", "2024-05-13"]
    
    def generate():
        pass

    def _scale(data):
        # possible to rescale 'by hand', details here
        # https://stackoverflow.com/questions/64535187/scaling-data-to-specific-range-in-python
        # instead use MinMaxScaler for simplicity
        scaler = MinMaxScaler(feature_range=(min(self.allowed_value_range), max(self.allowed_value_range)))
        data = scaler.fit(data)
        return data


    def _add_timestamps(data: list):
        timestamps = []
        start = self.datetime_range[0]
        start = datetime.strptime(start, "%Y-%m-%d")
        end = self.datetime_range[1]
        end = datetime.strptime(end, "%Y-%m-%d")
        for i in range(NUM_DATA_POINTS):
            timestamps.append(datetime.fromtimestamp(randrange(
            round(start.timestamp(), round(end.timestamp()))
            )
                                                     )
                              )
        return list(zip(timestamps, data))

    def serialize_events():
        events = []
        for item in self.data:
            value = item[0]
            timestamp = item[1]
            event = Event() 
            event.value = value
            event.event_timestamp = timestamp
            events.append(event)
        return events

class Temperature(Data):
    data: list
    allowed_value_range = [5, 25]

    def generate():
        # assume temperature is somewhat bimodal
        abs_value_range = max(allowed_value_range) - min(allowed_value_range)
        mean_1 = min(allowed_value_range) + (abs_value_range / 2)
        std = abs_value_range / 2
        size_1 = NUM_DATA_POINTS // 2
        modal_1 = np.random.normal(mean_1, std, size_1)
        mean_2 = max(allowed_value_range) - (abs_value_range / 2)
        size_2 = NUM_DATA_POINTS - size_1
        bi_modal_dist = np.random.normal(mean_2, std, size_2)
        bi_modal_dist.extend(modal_1)
        scaled_dist = self._scale(bi_modal_dist)
        self._add_timestamps(scaled_dist)
        self.data = scaled_dist

class Humidity(Data):
    data: list
    allowed_value_range = [65, 75]
    
    def generate():
        # real humidity depends on temp, ignore this for now
        # let's just pick a distribution for this
        # picking a left skewed distribution since SF is likely
        # more humid due to its proximity to the ocean
        # more negative is more left skewed
        # reference: 
        # https://stackoverflow.com/questions/24854965/create-random-numbers-with-left-skewed-probability-distribution
        dist = skewnorm.rvs(a=-5 ,loc=max(allowed_value_range), size=NUM_DATA_POINTS)
        scaled_dist = self._scale(dist)
        self._add_timestamps(scaled_dist)
        self.data = scaled_dist
        

class AirPressure(Data):
    data: list
    # https://wrcc.dri.edu/htmlfiles/westcomp.bp.html
    allowed_value_range = [29, 32]
    
    def generate():
        # lets just choose a normal distribution for this one
        abs_value_range = max(allowed_value_range) - min(allowed_value_range)
        mean = min(allowed_value_range) + (abs_value_range / 2)
        std = abs_value_range / 2
        dist = np.random.normal(mean_1, std, NUM_DATA_POINTS)
        scaled_dist = self._scale(dist)
        self._add_timestamps(scaled_dist)
        self.data = scaled_dist

def generate_serials():
    serials = []
    for i in range(NUM_DATA_POINTS):
        # generates a random number between 1 and 3
        # want to generate a hex thing at some point?
        # requires a schema change for protobuf
       serials.append(random.randrange(1, NUM_UNITS + 1))

def push_to_api(proto):
    pass

def main():
    temperature = Temperature()
    humidity = Humidity()
    air_pressure = AirPressure()
    temperature.generate()
    humidty.generate()
    air_pressure.generate()
    serials = generate_serials()
    t_events = temperature.serialize_events()
    h_events = humidity.serialize_events()
    ap_events = air_pressure.serialize_events()

    for i in range(NUM_DATA_POINTS):
        proto = Sensors()
        proto.temperature = t_events[i]
        proto.humidity = h_events[i]
        proto.air_pressure = ap_events[i]
        now = datetime.now()
        proto.ingress_time.FromDatetime(now)
        push_to_api(proto)

if __name__ == "__main__":
    main()
