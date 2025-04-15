import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Предположим, ваш DataFrame называется df
# Исключаем категориальные столбцы и оставляем только длины волн
X = df.drop(columns=['Device', 'Material', 'Temperature', 'Sample']).values

# Нормализуем данные (для PCA важно масштабирование)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Применяем PCA
pca = PCA()  # можно изменить количество компонент
principal_components = pca.fit_transform(X_scaled)

# Создаем DataFrame с главными компонентами
pca_df = pd.DataFrame(data=principal_components, 
                      columns=['PC1', 'PC2'])

# Добавляем метаданные для интерпретации
pca_df = pd.concat([df[['Device', 'Material', 'Temperature', 'Sample']], pca_df], axis=1)

# Посмотрим объясненную дисперсию
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
