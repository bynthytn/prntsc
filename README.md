# TODO
Получение расфасованных по цветам картинок в отдельных папках

## Получение картинки с сайта prnt.sc путем генерации случайной ссылки

- [x] генерация случайной ссылки
- [x] открытие оригинала картинки
- [x] скачивание картинки в общую папку
- [x] проверка картинки на удаленность/доступность
    - [x] ???ссылка ведет на imgur
    - [x] ???the screenshot was removed
    - [x] ???проверять размер - кривые картинки в папке весят 1 КБ(удалять сразу)
- [x] загружаем случайную картинку
- [x] находим средний цвет
- [ ] если дистанция больше 350 и персентедж больше 80 И
    - [ ] если дистанция топ-2 цветов к белому или черному меньше 150(например 50 50 50) И
        - [ ] первый цвет будет основным - первый цвет белый, тогда второй должен быть черным и тогда картинка отсортируется в папку с белыми картинками
    - [ ] если дистанция между р г б меньше 50(например 20 20 10)
- [ ] переносить загруж в папочко uploaded со структурой sorted
    - [ ] 
- [ ] отдельный для gif 9n1t0s
- [x] определение основного цвета картинки
- [x] если общий цвет картинки составляет менее 40-50% или картинка каша - не скачивать
- [x] перемещение картинки в папку определенного цвета

## Бесконечная загрузка картинок в группы по цветам

#### Выгрузка картинок из папок по цветам в группы по цветам
- [x] перемещение картинок в папки по цветам
- [ ] загрузка картинки в нужную группу с таймером на полчаса больше предыдущей картинки находящейся в очереди
- [ ] удаление картинки из папки на компьютере

#### Повторение

- [x] постоянная загрузка новых картинок
- [ ] при достигнутом количестве картинок превышающем 1000 шт. перестать загружать новые
- [ ] сделать инпут с запрашиваемым числом картинок на скачку

### Рефактор

- [ ] классы
- [ ] async(aiohttp вместо requests)

