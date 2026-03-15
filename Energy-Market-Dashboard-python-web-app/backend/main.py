import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List



app = FastAPI(title="RUS Energy Market API")

DATA_FILE = "data.csv"

class RecordCreate(BaseModel):
    """Модель для создания записи."""
    timestep: datetime
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float

    @classmethod
    @field_validator('consumption_eur', 'consumption_sib', 'price_eur', 'price_sib')
    def validate_non_negative(cls, v: float) -> float:
        """Проверка неотрицательности значений."""
        if v < 0:
            raise ValueError('Value cannot be negative')
        return v

class Record(RecordCreate):
    """Модель для ответа."""
    id: int

def load_data() -> pd.DataFrame:
    """Загрузка данных из CSV с добавлением id.""" 
    df = pd.read_csv(DATA_FILE)
    if 'id' not in df.columns:
        df.insert(0, 'id', range(1, len(df) + 1))
        df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df: pd.DataFrame) -> None:
    """Сохранение данных в CSV."""
    df.to_csv(DATA_FILE, index=False)

# Эндпоинты
@app.get("/records", response_model=List[Record])
async def get_records():
    """Получение всех записей."""
    try:
        df = load_data()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/records", response_model=Record, status_code=201)
async def create_record(record: RecordCreate):
    """Создание новой записи."""
    try:
        df = load_data()
        
        new_id = df['id'].max() + 1 if not df.empty else 1
        new_record = {
            'id': new_id,
            'timestep': record.timestep,
            'consumption_eur': record.consumption_eur,
            'consumption_sib': record.consumption_sib,
            'price_eur': record.price_eur,
            'price_sib': record.price_sib
        }
        
        new_row = pd.DataFrame([new_record])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        return new_record
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/records/{record_id}", status_code=status.HTTP_200_OK)
async def delete_record(record_id: int):
    """Удаление записи по id."""
    try:
        df = load_data()
        if record_id not in df['id'].values:
            raise HTTPException(status_code=404, detail=f"Record with id {record_id} not found"
            )
        
        df = df[df['id'] != record_id]
        save_data(df)
        return {"message": f"Record {record_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса."""
    return {"status": "healthy"}