# Ish Bot Central

A Flask-based web application that manages bot identities and URL processing with MongoDB integration.

## Features

- Bot identity management
- URL processing and tracking
- MongoDB database integration
- Configurable ad system with probability-based click behavior
- Proxy support for data collection

## Prerequisites

- Python 3.x
- MongoDB
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ish_bot_central
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
MONGO_HOST=your_mongo_host
MONGO_PORT=your_mongo_port
MONGO_USERNAME=your_mongo_username
MONGO_PASSWORD=your_mongo_password
AD_PROVIDER=your_ad_provider
SMARTPROXY_HOST=your_proxy_host
SMARTPROXY_PORT=your_proxy_port
DATAIMPULSE_HOST=your_dataimpulse_host
DATAIMPULSE_PORT=your_dataimpulse_port
```

## Configuration

The application uses a configuration system with the following main components:

### MongoDB Configuration
- Host, port, username, and password settings
- Connection management with Flask application context

### Ad System Configuration
- Configurable ad types (vignette and in-page)
- Click probability ranges
- Keyword-based ad targeting
- Smartphone-specific ad keywords

### Proxy Configuration
- SmartProxy integration
- DataImpulse integration

## Project Structure

```
ish_bot_central/
├── flaskr/
│   ├── blueprints/
│   │   ├── bot_identity.py
│   │   └── urls.py
│   ├── services/
│   ├── models/
│   ├── files/
│   ├── __init__.py
│   ├── config.py
│   └── db.py
├── requirements.txt
└── LICENSE
```

## Usage

1. Start the Flask application:
```bash
flask run
```

2. The application will be available at `http://localhost:5000`

## API Endpoints

### Bot Identity Endpoints

#### Get Identity
- **Endpoint**: `/api/bots/identity/<method>/[value]`
- **Method**: GET
- **Description**: Retrieves bot identity information based on the specified method
- **Parameters**:
  - `method`: The method to use for identity retrieval (e.g., "random")
  - `value`: Optional filter parameters (for random method) or required value for other methods
- **Response**: JSON object containing identity information
- **Example**:
  ```bash
  # Get random identity
  GET /api/bots/identity/random/
  
  # Get random identity with filters
  GET /api/bots/identity/random/filter1=value1&filter2=value2
  ```

#### Get Timezone
- **Endpoint**: `/api/bots/identity/<identity_id>/timezone/`
- **Method**: GET
- **Description**: Retrieves timezone information for a specific identity
- **Parameters**:
  - `identity_id`: The ID of the bot identity
- **Response**: JSON object containing timezone information
- **Example**:
  ```bash
  GET /api/bots/identity/123/timezone/
  ```

#### Get Timezone with IP
- **Endpoint**: `/api/bots/identity/<identity_id>/timezone/<ip_addr>/`
- **Method**: GET
- **Description**: Retrieves timezone information for a specific identity using a custom IP address
- **Parameters**:
  - `identity_id`: The ID of the bot identity
  - `ip_addr`: The IP address to use for timezone lookup
- **Response**: JSON object containing timezone information
- **Example**:
  ```bash
  GET /api/bots/identity/123/timezone/192.168.1.1/
  ```

#### Update Cookies
- **Endpoint**: `/api/bots/identity/<identity_id>/cookies/`
- **Method**: PUT
- **Description**: Updates cookies for a specific identity
- **Parameters**:
  - `identity_id`: The ID of the bot identity
  - Request Body: JSON object containing cookie data
- **Response**: JSON object containing updated cookie information
- **Example**:
  ```bash
  PUT /api/bots/identity/123/cookies/
  {
    "cookie1": "value1",
    "cookie2": "value2"
  }
  ```

#### Update Local Storage
- **Endpoint**: `/api/bots/identity/<identity_id>/local-storage/`
- **Method**: PUT
- **Description**: Updates local storage data for a specific identity
- **Parameters**:
  - `identity_id`: The ID of the bot identity
  - Request Body: JSON object containing local storage data
- **Response**: JSON object containing updated local storage information
- **Example**:
  ```bash
  PUT /api/bots/identity/123/local-storage/
  {
    "key1": "value1",
    "key2": "value2"
  }
  ```

### URL Processing Endpoints

#### Get URL
- **Endpoint**: `/api/url/<index>/`
- **Method**: GET
- **Description**: Retrieves URL information based on the specified index
- **Parameters**:
  - `index`: The index type (currently supports "random")
- **Response**: JSON object containing URL information
- **Example**:
  ```bash
  GET /api/url/random/
  ```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

Error responses include a JSON object with an "error" field containing the error message.

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 