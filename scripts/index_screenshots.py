"""Index existing evidence images for later inclusion in academic documents."""
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
titles={1:'Калькулятор и тест-дизайн',2:'Список задач и дефекты',3:'Авторизация Selenium',4:'Форма и Page Object',5:'REST API и Postman',6:'Модульные тесты',7:'Android и Appium',8:'Нагрузка k6',9:'GitHub Actions'}
rows=['# Скриншоты практической части','','Снимки сохранены непосредственно браузером или эмулятором. Это каталог исходных изображений для последующего оформления отчётов.','','| Работа | Файл | Размер |','|---|---|---|']
count=0
for number,title in titles.items():
    for path in sorted((ROOT/f'lab{number:02}/screenshots').glob('*')):
        if path.suffix.lower() not in {'.png','.jpg','.jpeg'}:continue
        with Image.open(path) as image:
            width,height=image.size
            image.verify()
        relative=path.relative_to(ROOT).as_posix()
        rows.append(f'| {number}. {title} | [{path.name}]({relative}) | {width} × {height} |')
        count+=1
rows.extend(['',f'Всего изображений: {count}.',''])
(ROOT/'SCREENSHOTS.md').write_text('\n'.join(rows),encoding='utf-8')
print(f'Indexed {count} valid images')
