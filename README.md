# Cloud Image Resizer

A simple web service that allows users to upload images and resize them on the fly. The application consists of a **FastAPI** backend and a **React** frontend, and it is deployed on Render.

---

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Architecture](#architecture)
- [Backend (FastAPI)](#backend-fastapi)
- [Frontend (React)](#frontend-react)
- [Setup & Installation](#setup--installation)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Upload images via the UI or via API endpoint.
- Specify width and height (or one dimension) to resize while maintaining aspect ratio.
- Supports common image formats: JPEG, PNG, WEBP, GIF.
- Returns the resized image as a downloadable file.
- Simple authentication token for API usage (optional).

---

## Demo
You can try the live demo here: **[Live Backend URL](https://cloud-image-resizer-backend.onrender.com)**

The frontend is available at **[Live Frontend URL]** (replace with actual URL if deployed).

---

## Architecture
```
CloudImageResizer/
├── Backend/            # FastAPI app (Python)
│   ├── app/
│   │   ├── main.py     # entry point
│   │   ├── routes.py   # API routes
│   │   └── utils.py    # image processing helpers
│   └── requirements.txt
├── Frontend/           # React app (JavaScript/TypeScript)
│   ├── src/
│   │   ├── components/
│   │   └── App.tsx
│   └── package.json
└── README.md           # This document
```

---

## Backend (FastAPI)
- **Endpoint**: `POST /resize`
  - **Request**: multipart/form-data with fields `file`, `width` (optional), `height` (optional).
  - **Response**: `image/*` with the resized picture.
- **Dependencies**: `fastapi`, `uvicorn`, `pillow`, `python-multipart`.
- **Run locally**:
  ```bash
  cd Backend
  uvicorn app.main:app --reload
  ```

---

## Frontend (React)
- Built with **Create React App** and **TypeScript**.
- Uses **Axios** to call the backend API.
- Simple UI to select an image, input dimensions, and download the result.
- Run locally:
  ```bash
  cd Frontend
  npm install
  npm start
  ```

---

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cloud-image-resizer.git
   cd cloud-image-resizer
   ```
2. Set up the backend virtual environment:
   ```bash
   cd Backend
   python -m venv .venv
   source .venv/bin/activate   # on Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. (Optional) Set environment variables:
   - `API_TOKEN` – token required for protected endpoints.
4. Install frontend dependencies:
   ```bash
   cd ../Frontend
   npm install
   ```

---

## Running Locally
- **Backend**: `uvicorn app.main:app --reload`
- **Frontend**: `npm start` (will proxy API requests to `http://localhost:8000`)

Visit `http://localhost:3000` in your browser to use the app.

---

## Deployment
The project is configured for **Render**:
- Backend service (Python) – uses the `render.yaml` file.
- Frontend service (Node) – can be deployed as a static site.
- Ensure the environment variable `API_TOKEN` (if used) is set in Render dashboard.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes.
4. Open a Pull Request describing the changes.

---

## License
This project is licensed under the MIT License – see the `LICENSE` file for details.
