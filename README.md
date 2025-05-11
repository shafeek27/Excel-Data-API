# Excel Data API

## Overview
This FastAPI application processes Excel data from a file and exposes API endpoints for interaction with the data. The application reads from the Excel file `capbudg.xls` and provides endpoints to list tables, get table details, and calculate row sums.

## Features
- Excel file processing with pandas
- REST API with FastAPI
- Error handling for robust operation
- Automatic API documentation with Swagger UI

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure the Excel file exists at `capbudg.xls`

## Usage

### Starting the Server
Run the application with:

```bash
uvicorn main:app --host 0.0.0.0 --port 9090 --reload
```

The API will be available at `http://localhost:9090`.

### API Endpoints

#### GET /
Root endpoint with welcome message and basic information.

#### GET /list_tables
Lists all table names (sheet names) present in the Excel file.

**Response Example:**
```json
{
  "tables": ["Initial Investment", "Revenue Projections", "Operating Expenses"]
}
```

#### GET /get_table_details
Returns the names of the rows for the specified table.

**Parameters:**
- `table_name` (query): Name of the table/sheet to get details for

**Response Example:**
```json
{
  "table_name": "Initial Investment",
  "row_names": [
    "Initial Investment=",
    "Opportunity cost (if any)=",
    "Lifetime of the investment",
    "Salvage Value at end of project=",
    "Deprec.method(1:St.line;2:DDB)=",
    "Tax Credit (if any )=",
    "Other invest.(non-depreciable)="
  ]
}
```

#### GET /row_sum
Calculates and returns the sum of all numerical data points in the specified row.

**Parameters:**
- `table_name` (query): Name of the table/sheet
- `row_name` (query): Name of the row to calculate sum for

**Response Example:**
```json
{
  "table_name": "Initial Investment",
  "row_name": "Tax Credit (if any )=",
  "sum": 10
}
```

### Swagger Documentation
FastAPI provides automatic Swagger documentation for the API. 
Access the documentation at `http://localhost:9090/docs`.

## Error Handling

The API handles various error scenarios:
- 404: Excel file not found, table not found, or row not found
- 500: Error reading Excel file or calculating row sum

## Project Structure

```
.
├── capbudg.xls              # Excel file with data
├── main.py                  # Main FastAPI application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Testing

A Postman collection for testing the API is provided in `postman_collection.json`. 
Import this file into Postman to easily test the API endpoints.

## Potential Improvements

1. **Authentication & Authorization**: Implement user authentication for secure API access
2. **Caching**: Add caching mechanisms for frequently accessed data
3. **Database Integration**: Store processed Excel data in a database for improved performance
4. **Data Validation**: Add more sophisticated data validation and sanitization
5. **File Upload**: Allow users to upload Excel files through the API
6. **Dashboard**: Develop a web-based dashboard for data visualization
7. **Excel Format Support**: Support additional Excel formats beyond .xls
8. **Complex Calculations**: Implement more advanced data analysis operations
9. **Logging**: Add comprehensive logging for better debugging and monitoring
10. **Containerization**: Docker support for easier deployment

## Edge Cases Handling

The application addresses several edge cases:
- Non-existent Excel file
- Missing table (sheet) in the Excel file
- Missing row in a table
- Non-numerical data in rows
- Empty rows or tables
- Special characters in table or row names

## License

[MIT License](LICENSE)
