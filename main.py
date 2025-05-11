"""
FastAPI Application for Excel Data Processing

This application reads data from an Excel file and exposes API endpoints
for interacting with the data.

Author: Claude
Date: May 10, 2025
"""

import os
from typing import Dict, List, Union, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Constants
EXCEL_PATH = "./Data/capbudg.xls"

# Models for API responses
class TablesResponse(BaseModel):
    tables: List[str]

class TableDetailsResponse(BaseModel):
    table_name: str
    row_names: List[str]

class RowSumResponse(BaseModel):
    table_name: str
    row_name: str
    sum: float

# Initialize FastAPI app
app = FastAPI(
    title="Excel Data API",
    description="API for interacting with Excel data from capbudg.xls",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def check_file_exists():
    """
    Check if the Excel file exists.
    
    Raises:
        HTTPException: If the file does not exist.
    """
    if not os.path.exists(EXCEL_PATH):
        raise HTTPException(
            status_code=404,
            detail=f"Excel file not found at {EXCEL_PATH}"
        )

def read_excel_sheets() -> Dict[str, pd.DataFrame]:
    """
    Read all sheets from the Excel file.
    
    Returns:
        Dict[str, pd.DataFrame]: A dictionary mapping sheet names to DataFrames.
        
    Raises:
        HTTPException: If there's an error reading the file.
    """
    try:
        check_file_exists()
        excel_data = pd.read_excel(EXCEL_PATH, sheet_name=None)
        return excel_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading Excel file: {str(e)}"
        )

def get_row_names(df: pd.DataFrame) -> List[str]:
    """
    Extract row names from a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to extract row names from.
        
    Returns:
        List[str]: List of row names.
    """
    # Assuming the first column contains row names
    if df.shape[0] > 0:
        return df.iloc[:, 0].dropna().tolist()
    return []

def calculate_row_sum(df: pd.DataFrame, row_name: str) -> float:
    """
    Calculate the sum of numerical values in a row.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        row_name (str): The name of the row to sum.
        
    Returns:
        float: The sum of numerical values in the row.
        
    Raises:
        HTTPException: If the row is not found or contains no numerical data.
    """
    # Find the row with the specified name
    row_mask = df.iloc[:, 0] == row_name
    if not any(row_mask):
        raise HTTPException(
            status_code=404,
            detail=f"Row '{row_name}' not found in table"
        )
    
    # Get the row and convert to numeric, coercing errors to NaN
    row_data = df.loc[row_mask].iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
    
    # Sum the numerical values, ignoring NaN
    row_sum = row_data.sum().sum()
    
    return float(row_sum)

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides basic API information.
    
    Returns:
        Dict: Welcome message and basic API information.
    """
    return {
        "message": "Welcome to the Excel Data API",
        "endpoints": [
            "GET /list_tables",
            "GET /get_table_details",
            "GET /row_sum"
        ]
    }

@app.get("/list_tables", response_model=TablesResponse, tags=["Tables"])
async def list_tables():
    """
    List all table names (sheet names) present in the Excel file.
    
    Returns:
        TablesResponse: Object containing a list of table names.
        
    Raises:
        HTTPException: If there's an error reading the Excel file.
    """
    excel_data = read_excel_sheets()
    return TablesResponse(tables=list(excel_data.keys()))

@app.get("/get_table_details", response_model=TableDetailsResponse, tags=["Tables"])
async def get_table_details(
    table_name: str = Query(..., description="Name of the table/sheet to get details for")
):
    """
    Return the names of the rows for the specified table.
    
    Args:
        table_name (str): Name of the table (sheet) to get details for.
        
    Returns:
        TableDetailsResponse: Object containing the table name and row names.
        
    Raises:
        HTTPException: If the table is not found or there's an error processing the data.
    """
    excel_data = read_excel_sheets()
    
    if table_name not in excel_data:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table_name}' not found in Excel file"
        )
    
    df = excel_data[table_name]
    row_names = get_row_names(df)
    
    return TableDetailsResponse(
        table_name=table_name,
        row_names=row_names
    )

@app.get("/row_sum", response_model=RowSumResponse, tags=["Calculations"])
async def row_sum(
    table_name: str = Query(..., description="Name of the table/sheet"),
    row_name: str = Query(..., description="Name of the row to calculate sum for")
):
    """
    Calculate and return the sum of all numerical data points in the specified row.
    
    Args:
        table_name (str): Name of the table (sheet).
        row_name (str): Name of the row to calculate sum for.
        
    Returns:
        RowSumResponse: Object containing the table name, row name, and calculated sum.
        
    Raises:
        HTTPException: If the table or row is not found, or there's an error in calculation.
    """
    excel_data = read_excel_sheets()
    
    if table_name not in excel_data:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table_name}' not found in Excel file"
        )
    
    df = excel_data[table_name]
    try:
        row_sum_value = calculate_row_sum(df, row_name)
        
        return RowSumResponse(
            table_name=table_name,
            row_name=row_name,
            sum=row_sum_value
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating row sum: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)
