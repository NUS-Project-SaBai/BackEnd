# API Documentation: Village Management

---

- **Frontend Location**:  
  Village management pages, useVillages Hook, DynamicVillageDropdown
  Indirectly: PatientSearchbar, SideMenu, PatientSearchbarByReferral, the various pages.

- **Purpose on Frontend**:  
  To manage village data including creating new villages, updating existing ones, retrieving village lists for dropdowns, and managing village visibility (hiding/showing villages).

---

## API Endpoint: `/api/v1/villages/`

### Overview

- **Description**:  
  Manages village data including retrieval, creation, and updates. Supports filtering by visibility status and individual village operations.
- **HTTP Method**:  
  GET, POST, PATCH

---

### Request Details

#### Query Parameters (GET requests)

- **include_hidden**: Optional boolean parameter to include hidden villages in the response.
  - Type: String ("true" or any value)
  - Example: `/api/v1/villages/?include_hidden=true`
  - Default behavior: Only returns visible villages (is_hidden=false)

#### URL Parameters

- **pk**: Village ID for specific village operations (GET, PATCH)
  - Type: Integer
  - Example: `/api/v1/villages/1/`

#### Request Body (POST - Create Village)

- **Structure**:
  ```json
  {
    "village_name": "Sample Village",
    "colour_code": "#FF5733",
    "is_hidden": false
  }
  ```

#### Request Body (PATCH - Update Village)

- **Structure**:
  ```json
  {
    "village_name": "Updated Village Name",
    "colour_code": "#33FF57",
    "is_hidden": true
  }
  ```
  - **Note**: Only include fields you want to update. Empty string values are filtered out.

---

### Response Details

#### Response Structure

- **Status Codes**:
  - 200: Successful GET or PATCH operation
  - 201: Successful POST operation (village created)
  - 400: Bad Request (validation errors)
  - 404: Village not found (for specific pk operations)
  - 500: Internal Server Error

#### Sample Responses

**GET `/api/v1/villages/` (List all visible villages)**:

```json
[
  {
    "id": 1,
    "village_name": "Village A",
    "colour_code": "#FF5733",
    "is_hidden": false
  },
  {
    "id": 2,
    "village_name": "Village B",
    "colour_code": "#33FF57",
    "is_hidden": false
  }
]
```

**GET `/api/v1/villages/1/` (Get specific village)**:

```json
{
  "id": 1,
  "village_name": "Village A",
  "colour_code": "#FF5733",
  "is_hidden": false
}
```

**POST `/api/v1/villages/` (Create village)**:

```json
{
  "id": 3,
  "village_name": "New Village",
  "colour_code": "#3357FF",
  "is_hidden": false
}
```

**PATCH `/api/v1/villages/1/` (Update village)**:

```json
{
  "id": 1,
  "village_name": "Updated Village Name",
  "colour_code": "#FF5733",
  "is_hidden": false
}
```

#### Data Fetched by the Frontend

- **Complete Data Set**:  
  All fields from the Village model are sent over the API:
  - **id**: Unique identifier for the village (auto-generated)
  - **village_name**: Name of the village (max 20 characters, unique)
  - **colour_code**: Color code for visual representation (max 20 characters)
  - **is_hidden**: Boolean flag indicating if the village is hidden/deleted

#### Data Used by the Frontend

- **Relevant Data Subset**:  
  Typically, the frontend uses:
  - **id**: For identification and API calls
  - **village_name**: For display in dropdowns and forms
  - **colour_code**: For visual representation/styling
  - **is_hidden**: For filtering logic (when include_hidden is used)

---

### Data Processing Details

#### Processing on the Backend

- **Where**:  
  Processing is handled in the VillageView (api/views/village_view.py) and VillageService (api/services/village_service.py).
- **How**:
  - **GET requests**: Filters villages by is_hidden status based on query parameters
  - **POST requests**: Validates data using VillageSerializer and creates new village instances
  - **PATCH requests**: Filters out empty string values and applies partial updates to existing villages
  - **Data validation**: Ensures village_name uniqueness and field length constraints
- **Example**:  
  When `include_hidden=true` is passed, the service retrieves all villages regardless of is_hidden status. Otherwise, it defaults to only visible villages (is_hidden=false).

---

### API Endpoints Summary

| Method | Endpoint                                | Description                                |
| ------ | --------------------------------------- | ------------------------------------------ |
| GET    | `/api/v1/villages/`                     | Get all villages (visible only by default) |
| GET    | `/api/v1/villages/?include_hidden=true` | Get all villages including hidden ones     |
| GET    | `/api/v1/villages/{id}/`                | Get specific village by ID                 |
| POST   | `/api/v1/villages/`                     | Create a new village                       |
| PATCH  | `/api/v1/villages/{id}/`                | Update an existing village                 |

### Additional Notes

- **Uniqueness Constraint**: Village names must be unique across all villages (including hidden ones).
- **Soft Delete**: Villages use the `is_hidden` flag for soft deletion rather than actual deletion.
- **Color Codes**: The colour_code field is intended for frontend visual representation and should follow tailwind colour format. For eg. `text-blue-400` and `text-purple-400`
- **Filtering**: The `include_hidden` query parameter allows admin interfaces to manage hidden villages while keeping them out of regular user interfaces.
- **Partial Updates**: PATCH requests support partial updates - only send the fields you want to change.

_End of Village API Documentation_
