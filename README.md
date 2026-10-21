
## Запуск тестов  
1. Установите зависимости:  
   ```sh
   pip install -r requirements.txt
    ```
2. Запустите тесты:  
   ```sh
    pytest tests --alluredir=allure_results
    ```
3. Сгенерируйте отчёт Allure::  
   ```sh
   allure serve allure_results  
    ```
