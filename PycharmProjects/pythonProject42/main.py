# Gerekli kütüphaneleri içe aktarıyoruz
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# IRIS veri setini yüklüyoruz
iris = load_iris()
X = iris.data  # Özellikler (sepal ve petal ölçüleri)
y = iris.target  # Etiketler (setosa, versicolor, virginica)

# Veriyi eğitim ve test olarak ayırıyoruz (test seti %25)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

# Decision Tree modelini oluşturup eğitiyoruz
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Eğitim ve test setleri için tahmin yapıyoruz
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

# Eğitim ve test doğruluklarını hesaplıyoruz
train_accuracy = accuracy_score(y_train, train_predictions)
test_accuracy = accuracy_score(y_test, test_predictions)

print(f"Eğitim doğruluğu: {train_accuracy:.2f}")
print(f"Test doğruluğu: {test_accuracy:.2f}")

# Bu sonucun anlamı:
print("\nNot: Eğitim doğruluğu genelde yüksektir çünkü model kendi gördüğü veriyi tahmin ediyor. Ancak test doğruluğu genel başarıyı gösterir.")

# 10 farklı random_state değeri ile test yapıyoruz
random_accuracies = []
for seed in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=seed)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    random_accuracies.append(acc)

mean_acc = np.mean(random_accuracies)
std_acc = np.std(random_accuracies)

print("\n10 farklı random_state kullanarak elde edilen test doğrulukları:")
print(random_accuracies)
print(f"Ortalama: {mean_acc:.2f}")
print(f"Standart Sapma: {std_acc:.4f}")

# Farklı test seti oranları ile doğrulukları karşılaştırıyoruz
ratios = [0.1, 0.25, 0.5, 0.75, 0.9]
accuracies = []

for r in ratios:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=r, random_state=0)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    accuracies.append(acc)

# Grafikle gösteriyoruz
plt.figure(figsize=(8, 5))
plt.plot(ratios, accuracies, marker='o', color='blue')
plt.title("Doğruluk vs. Test Seti Oranı")
plt.xlabel("Test Seti Oranı")
plt.ylabel("Test Doğruluğu")
plt.grid(True)
plt.show()

# Modelin karar ağacını çiziyoruz
plt.figure(figsize=(12, 8))
plot_tree(model, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)
plt.title("Karar Ağacı Görselleştirmesi")
plt.show()

