import pandas as pd
import numpy as np

# Загрузка данных с правильными заголовками
file_path = "Data_set_avarage_vol1.csv"

# Чтение данных с пропуском ненужных строк и столбцов
df = pd.read_csv(file_path, header=None, skiprows=[0])

# Извлечение метаданных
metadata = {
    'Device': df.iloc[0, 2:].values,
    'Folder': df.iloc[1, 2:].values,
    'Temp': df.iloc[2, 2:].values,
    'Sample': df.iloc[3, 2:].values
}

# Извлечение спектральных данных (начиная с строки 4)
spectral_data = df.iloc[4:, 1:].astype(float)
wavelengths = df.iloc[4:, 1].astype(float).values
intensities = df.iloc[4:, 2:].astype(float).values.T  # Транспонируем

# Создаем итоговый DataFrame
result_df = pd.DataFrame(intensities, columns=wavelengths)

# Добавляем метаданные
result_df.insert(0, 'Device', metadata['Device'])
result_df.insert(1, 'Material', metadata['Folder'])  # Folder -> Material для понятности
result_df.insert(2, 'Temperature', [int(t[1:]) if str(t).startswith('T') else np.nan for t in metadata['Temp']])
result_df.insert(3, 'Sample', metadata['Sample'])

# Очистка данных
result_df = result_df.dropna(subset=['Temperature'])
result_df['Temperature'] = result_df['Temperature'].astype(int)

# Сохранение результата
output_path = "processed_spectra_clean.csv"
result_df.to_csv(output_path, index=False)

print(f"Данные успешно обработаны и сохранены в {output_path}")
print("\nСтруктура обработанных данных:")
print(result_df.iloc[:, :10].head())  # Показываем первые 10 столбцов

# Дополнительная информация
print("\nСтатистика:")
print(f"Количество образцов: {len(result_df)}")
print(f"Диапазон температур: {result_df['Temperature'].min()}K - {result_df['Temperature'].max()}K")
print(f"Уникальные материалы: {result_df['Material'].unique()}")
