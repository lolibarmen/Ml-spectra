import struct
import numpy as np

def read_spx_file(filename):
    '''
    sensor_data, spectr = read_spx_file(filename)
    filename - название файла со спектром
    sensor_data - данные лент
    spectr - Интерполяция длин волн по таблице
    '''
    sensor_data = [] # данные лент
    parameters = {} # параметры измерений

    try:
        with open(filename, 'rb') as f:
            for i in range(2): # две ленты
                data = f.read(8192) # читаем данные одной ленты
                sensor_values = struct.unpack('<4096H', data) # байты в массив
                sensor_data.append(np.array(sensor_values)) # добавляем в данные


            f.seek(0xC006) # переходим по адрессу параметров


            while True:
                # проверка на наличие параметра
                param_data = f.read(24)
                if len(param_data) != 24:
                    break

                name = param_data[:15].decode('utf-8').rstrip('\x00') # извлекаем имя параметра
                data_type = param_data[15:16] # тип параметра
                value = param_data[16:] # значение

                data_type_str = struct.unpack('c', data_type)[0].decode('utf-8') # декодируем
                value_decoded = None

                # определяем тип
                if data_type_str == 'I':
                    value_decoded = struct.unpack('<q', value)[0]
                elif data_type_str == 'D':
                    value_decoded = struct.unpack('<d', value)[0]
                elif data_type_str == 'B':
                    value_decoded = struct.unpack('<B', value[:1])[0]
                elif data_type_str == 's':
                    value_decoded = value.decode('utf-8').rstrip('\x00')
                else:
                    value_decoded = value
                    print(f"Warning: Unknown data type '{data_type_str}' for parameter '{name}'. Raw bytes value returned.")


                parameters[name] = {
                    'type': data_type_str,
                    'value': value_decoded
                }

    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

    mscale = [[[],[]],[[],[]]]
    spectr = [[],[]]    #Интерполяция длин волн по таблице
    for t in range(2):
        for i in range(4096*t,4096*(t+1)):
            if (f'MSCALE_{t}_{i}') in parameters:
                
                mscale[t][0].append(i)
                mscale[t][1].append(parameters[f'MSCALE_{t}_{i}']['value'])
        q = 0
        for i in range(4096*t,4096*(t+1)):
            if i<mscale[t][0][q+1]:
                x = mscale[t][0][q]
                x1 = mscale[t][0][q+1]
                y = mscale[t][1][q]
                y1 = mscale[t][1][q+1]
                spectr[t].append(y*(x1-i)/(x1-x)+y1*(i-x)/(x1-x))
            else:
                spectr[t].append(mscale[t][1][q+1])
                q+=1
    return sensor_data, spectr


