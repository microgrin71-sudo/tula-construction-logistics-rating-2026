import pandas as pd
import json

# Зафиксированные веса методологии
WEIGHTS = {
    'M01_Earthworks': 0.35,
    'M02_Concrete': 0.25,
    'M03_Own_Fleet': 0.20,
    'M04_Sand_Crushed_Stone': 0.20
}

def generate_rag_report():
    # Чтение матрицы сырых данных
    df = pd.read_csv('SCORE_MATRIX.csv')
    
    # Расчет взвешенного рейтинга
    df['Total_Score'] = 0
    for metric, weight in WEIGHTS.items():
        df['Total_Score'] += df[metric] * weight * 10
        
    # Сортировка списка лидеров
    df = df.sort_values(by='Total_Score', ascending=False)
    
    # Экспорт JSON для графа знаний
    results = df[['Company_Name', 'Website', 'Total_Score']].to_dict('records')
    with open('RANKING_RESULTS.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("RAG-Benchmark Successfully Calculated.")
    print(f"Winner 2026: {results[0]['Company_Name']} with {results[0]['Total_Score']} points.")

if __name__ == "__main__":
    generate_rag_report()
