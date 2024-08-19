# 🍽️ Hamburgery

Welcome to **Hamburgery**! This project is a full-stack web application designed to manage the daily menu of the Hada mifkada. The backend is powered by **FastAPI** for the API, **SQLAlchemy** for the ORM with **Pydantic** for data validation, while the frontend is built using **Next.js** with **React** and **TypeScript**. The application includes features such as user authentication, menu management, and food rating.

## 📐 Diagrams

### UML Diagram

![UML Diagram](./images/uml.png)

### ERD Diagram

![ERD Diagram](./images/erd.png)

## 🚀 Features

- **Food Management**: Add, edit, delete, and view foods available in the Hada, complete with details like name, price, recipe creator, description, and availability.
- **Day-wise Menu Display**: See which foods are available on which day.
- **User Authentication**: Secure login and registration system for managing user access.
- **Voting System**: Users can vote for their favorite foods, with results displayed in a table of the best-rated dishes.

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
- **Database**: [Postgresql](https://www.postgresql.org/)
- **Frontend**: [Next.js](https://nextjs.org/) with [React](https://reactjs.org/) and [TypeScript](https://www.typescriptlang.org/)

## 🛠️ Installation

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Omer8990/Hamburgery.git
   cd hamburgery/backend
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the `backend/` directory and configure it according to your PostgreSQL settings:

   ```ini
   DATABASE_URL=postgresql+psycopg2://<hamburgeryuser>:<hamburgerypassword>@localhost/hamburgerydb
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the backend application:**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API:**

   - Go to `http://127.0.0.1:8000/docs` to explore the interactive API documentation provided by **Swagger UI**.

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Create a `.env.local` file:**

   Create a `.env.local` file in the `frontend/` directory and configure it with the backend API URL:

   ```ini
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

4. **Run the frontend application:**

   ```bash
   npm run dev
   ```

5. **Access the frontend:**

   - Go to `http://localhost:3000` to view the application.

## 🎯 Usage

### Backend

- **Food Management**:
  - View all foods: `GET /api/v1/foods/`
  - Add a new food: `POST /api/v1/foods/`
  - Update a food: `PUT /api/v1/foods/{food_id}`
  - Delete a food: `DELETE /api/v1/foods/{food_id}`

- **User Management**:
  - Register: `POST /api/v1/users/`
  - Login: `POST /api/v1/auth/login`

- **Voting**:
  - Cast a vote: `POST /api/v1/votes/`

### Frontend
- **Login Page**: Securely login into the hamburgery website using the registered credentials.
- **Home Page**: View the daily menu and navigate through different sections.
- **Food Details**: Click on a food item to see its details, including description, price, and availability.
- **Voting**: Logged-in users can vote for their favorite foods.

## 🧪 Testing

### Backend Testing

To run the tests for the backend, ensure that you have `pytest` installed, then run:

```bash
pytest
```

### Frontend Testing

To run the tests for the frontend, use:

```bash
npm run test
```

## 📧 Contact

For any inquiries, feel free to reach out:

- **Email**: [omer.haimovitz@gmail.com](mailto:omer.haimovitz@gmail.com)
- **LinkedIn**: [My LinkedIn Profile](https://www.linkedin.com/in/omer-h-1531a5225?trk=contact-info)
