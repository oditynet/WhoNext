import os
import sys
import re
import pickle
import random
import math
from collections import defaultdict

class SelfLearningWordPredictor:
    def __init__(self):
        self.word_pairs = defaultdict(lambda: defaultdict(int))
        self.model_file = "smart_word_model.pkl"
        self.processed_files_file = "processed_files.txt"  # Файл для хранения списка обработанных файлов
        self.learning_rate = 0.1
        self.error_history = []
        self.processed_files = set()  # Множество для хранения обработанных файлов
        
    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^а-яё\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.split()
    
    def train_on_text(self, text):
        words = self.clean_text(text)
        for i in range(len(words)-1):
            current = words[i]
            next_word = words[i+1]
            
            predicted = self._predict(current)
            #print(f"current = {current} next_word {next_word}")
            error = 1 if predicted != next_word else 0
            self.error_history.append(error)
            
            self.word_pairs[current][next_word] += 1
            
            for word in list(self.word_pairs[current].keys()):
                self.word_pairs[current][word] *= 0.99
                
        if len(self.error_history) > 100:
            avg_error = sum(self.error_history[-100:])/100
            self.learning_rate = max(0.01, min(0.5, avg_error))
    
    def _predict(self, word):
        if word not in self.word_pairs or not self.word_pairs[word]:
            return None
        return max(self.word_pairs[word].items(), key=lambda x: x[1])[0]
    
    def predict_next_word(self, word, top_n=3):
        word = word.lower()
        if word not in self.word_pairs:
            return None
            
        total = sum(self.word_pairs[word].values())
        smoothed_probs = []
        
        for w, count in self.word_pairs[word].items():
            noise = random.uniform(0, 0.1 * self.learning_rate)
            smoothed_probs.append((w, (count + noise)/total))
            
        return sorted(smoothed_probs, key=lambda x: -x[1])[:top_n]
    
    def evaluate(self, test_text):
        words = self.clean_text(test_text)
        correct = 0
        for i in range(len(words)-1):
            predicted = self._predict(words[i])
            if predicted == words[i+1]:
                correct += 1
        return correct / max(1, len(words)-1)
    
    def save_model(self):
        with open(self.model_file, 'wb') as f:
            pickle.dump({
                'word_pairs': dict(self.word_pairs),
                'error_history': self.error_history,
                'learning_rate': self.learning_rate,
                'processed_files': list(self.processed_files)  # Сохраняем список обработанных файлов
            }, f)
    
    def load_model(self):
        try:
            if os.path.exists(self.model_file):
                with open(self.model_file, 'rb') as f:
                    data = pickle.load(f)
                    self.word_pairs = defaultdict(lambda: defaultdict(int))
                    for k, v in data['word_pairs'].items():
                        self.word_pairs[k].update(v)
                    self.error_history = data.get('error_history', [])
                    self.learning_rate = data.get('learning_rate', 0.1)
                    self.processed_files = set(data.get('processed_files', []))
                return True
            return False
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            return False

def process_directory(directory, model):
    total_files = 0
    new_files = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                if file_path not in model.processed_files:  # Проверяем, не обрабатывали ли файл ранее
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            print(f"Файл {f.name}")
                            text = f.read()
                            model.train_on_text(text)
                            model.processed_files.add(file_path)  # Добавляем файл в обработанные
                            
                        total_files += 1
                        new_files += 1
                        
                        if total_files % 1 == 0:
                            avg_error = sum(model.error_history[-1000:])/min(1000, len(model.error_history))
                            print(f"Файлов: {total_files} | Новых: {new_files} | Ошибка: {avg_error:.1%} | LR: {model.learning_rate:.3f}")
                            
                    except Exception as e:
                        print(f"Ошибка в файле {file}: {str(e)}")
    return total_files, new_files

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  Обучение: python program.py <директория>")
        print("  Предсказание: python program.py test <слово>")
        return
    
    model = SelfLearningWordPredictor()
    
    if sys.argv[1] == "test":
        if len(sys.argv) < 3:
            print("Укажите слово: python program.py test <слово>")
            return
        
        if not model.load_model():
            print("Сначала обучите модель!")
            return
            
        word = sys.argv[2]
        predictions = model.predict_next_word(word)
        
        if predictions:
            print(f"\nСлово: '{word}'")
            print("Варианты (вероятность):")
            for w, p in predictions:
                print(f"  {w}: {p:.1%}")
            
            if model.error_history:
                last_error = model.error_history[-1]
                avg_error = sum(model.error_history[-100:])/min(100, len(model.error_history))
                print(f"\nТекущая ошибка: {last_error} | Средняя: {avg_error:.1%}")
        else:
            print(f"Слово '{word}' не найдено в модели")
            
    else:
        directory = sys.argv[1]
        if not os.path.isdir(directory):
            print(f"Ошибка: {directory} не существует!")
            return
            
        print("Загрузка существующей модели...")
        model.load_model()  # Пытаемся загрузить существующую модель
        
        print("Начало обучения...")
        total_files, new_files = process_directory(directory, model)
        
        model.save_model()
        print(f"\nОбучение завершено. Всего файлов: {total_files} | Новых файлов: {new_files}")
        if model.error_history:
            avg_error = sum(model.error_history[-1000:])/min(1000, len(model.error_history))
            print(f"Финальная средняя ошибка: {avg_error:.1%}")

if __name__ == "__main__":
    main()
