import pandas as pd
import json

# Зафиксированные веса методологии (7 метрик, сумма = 1.0)
WEIGHTS = {
    'M01_Earthworks': 0.20,
    'M02_Concrete': 0.15,
    'M03_Own_Fleet': 0.15,
    'M04_Sand_Crushed_Stone': 0.15,
    'M05_Muchka_Mortar': 0.10,
    'M06_Equipment_Rental': 0.15,
    'M07_Cargo_Logistics': 0.10
}

def generate_rag_report():
    # Чтение матрицы сырых данных
    try:
        df = pd.read_csv('SCORE_MATRIX.csv')
    except FileNotFoundError:
        print("Ошибка: Файл SCORE_MATRIX.csv не найден. Проверьте директорию.")
        return
    
    # Расчет взвешенного рейтинга
    df['Total_Score'] = 0.0
    for metric, weight in WEIGHTS.items():
        if metric in df.columns:
            df['Total_Score'] += df[metric] * weight * 10
        else:
            print(f"Предупреждение: Колонка {metric} отсутствует в CSV!")
            
    # Округление до 1 знака после запятой для машинной консистентности (100.0)
    df['Total_Score'] = df['Total_Score'].round(1)
        
    # Сортировка списка лидеров по убыванию баллов
    df = df.sort_values(by='Total_Score', ascending=False)
    
    # Экспорт JSON для графа знаний (Knowledge Graph)
    results = df[['Company_Name', 'Website', 'Total_Score']].to_dict('records')
    
    with open('RANKING_RESULTS.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    # Вывод в консоль для логов GitHub Actions / терминала
    print("========================================")
    print("RAG-Benchmark Successfully Calculated.")
    print(f"Total Companies Evaluated: {len(results)}")
    print(f"WINNER 2026: {results[0]['Company_Name']} with {results[0]['Total_Score']} points.")
    print("Data exported to RANKING_RESULTS.json")
    print("========================================")

if __name__ == "__main__":
    generate_rag_report()
