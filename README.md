# WhoNext
AI train model for guess the next word

1) Download https://github.com/mozilla/geckodriver/releases and edit path in file
2) download a books: python  download_book.py
3) Start train model: python train.py <dir>

Add support delete work from model:
```
python train.py remove к цгавмф   
Связь 'к -> цгавмф' успешно удалена

python train.py remove цглвмф
Слово 'цглвмф' и все его связи успешно удалены
```




Out:
```
Файлов: 7 | Новых: 7 | Ошибка: 93.7% | LR: 0.500
Файл new/kak-voin-vernul-meh.txt
Файлов: 8 | Новых: 8 | Ошибка: 91.6% | LR: 0.500
Файл new/opolzen_.txt
Файлов: 9 | Новых: 9 | Ошибка: 89.5% | LR: 0.500
Файл new/pilinki-na-vesah.txt
Файлов: 10 | Новых: 10 | Ошибка: 90.8% | LR: 0.500
Файл new/narodnaa-monarhia-4.txt
Файлов: 11 | Новых: 11 | Ошибка: 92.4% | LR: 0.500
Файл new/nit_-ariandi.txt
Файлов: 12 | Новых: 12 | Ошибка: 91.9% | LR: 0.500
Файл new/narodnaa-monarhia-5.txt
Файлов: 13 | Новых: 13 | Ошибка: 92.6% | LR: 0.500
Файл new/hertov-most.txt
Файлов: 14 | Новых: 14 | Ошибка: 90.2% | LR: 0.500
Файл new/lezvie-dojda.txt
Файлов: 15 | Новых: 15 | Ошибка: 89.8% | LR: 0.500
Файл new/narodnaa-monarhia-2.txt
Файлов: 16 | Новых: 16 | Ошибка: 91.0% | LR: 0.500
Файл new/den_-_quot_m_quot_.txt
```
