JSON_LAYER_SEPARATOR = '_'
FINDMY_FILES = [
    '~/Library/Caches/com.apple.findmy.fmipcore/Items.data',
    '~/Library/Caches/com.apple.findmy.fmipcore/Devices.data']
NAME_SEPARATOR = '_'
NULL_STR = 'NULL'
TIME_FORMAT = '%m/%d/%Y, %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
# API_ENDPOINT = 'http://localhost:8000/api/v1/devices-data/'
API_ENDPOINT = 'https://location-based-devices.spatialdynamicslab.xyz/api/v1/devices/'
KEYS_FOR_API =[
    "id",
    "identifier", 
    "name", 
    "location_latitude", 
    "location_longitude", 
    "location_timeStamp",
    "location_positionType", 
    "location_horizontalAccuracy",
    "location_verticalAccuracy", 
    "location_isInaccurate", 
    "location_isOld",
    "location_locationFinished", 
    "batteryLevel", 
    "batteryStatus"
]


# Here you need to add the names of the AirTags or SmartPhones to be tracked
DEVICE_NAMES_API_TRACKING = [
    'UCD-T1',
    # 'jpablogomezb-iPhone'
    'UCD-T2',
    'UCD-T3',
    'UCD-T4',
    'UCD-T5',
    'UCD-T6',
    'UCD-T7',
    'UCD-T8',
    'UCD-T9',
    'UCD-T10',
    'UCD-T11'
    'UCD-T12',
    'UCD-T13',
    'UCD-T14',
    'UCD-T15',
    'UCD-T16',
    'UCD-T17',
]
