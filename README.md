# Library Management System v1.0

The Library Management System is a multi-user application designed to efficiently manage the process of issuing e-books to users. It serves both librarians and general users, allowing them to request, read, and return e-books. Librarians have additional privileges to manage sections and e-books, and to approve or revoke access to books.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [ER Diagram](#er-diagram)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

### Frontend
- HTML
- CSS
- Bootstrap

### Backend
- Flask

### Templating Engine
- Jinja

### Data Storage
- SQLite

### Libraries
- Flask: A micro web framework for Python.
- SQL Alchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library.
- Flask-SQL Alchemy: An extension for Flask that adds support for SQL Alchemy.
- Flask-RESTful: An extension for Flask that adds support for quickly building REST APIs.
- Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python.
- Seaborn: A data visualization library based on Matplotlib that provides a high-level interface for drawing attractive and informative statistical graphics.

### IDE
- Visual Studio Code (VS Code)

## Features

1. **User Authentication**: Users and librarians can log in to access the system.
2. **Section Management**: Librarians can add new sections with details like name, date created, and description.
3. **Book Management**: Librarians can add new books with attributes such as title, content, author(s), etc.
4. **Book Issuing**: Users can request books, and librarians can approve or reject these requests.
5. **Book Return**: Users can return books after reading.
6. **Data Visualization**: Graphical representation of data such as user roles distribution, book request status, and section-wise book count.
7. **File Handling**: Functionality for uploading and downloading e-books.
8. **Search Options**: Users can search for books.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Akashkunwar/Library_Management_System.git
    ```

2. Navigate to the project directory:
    ```sh
    cd Library_Management_System
    ```

3. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Set up the database:
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. Run the application:
    ```sh
    flask run
    ```

## Usage

1. Access the application in your web browser at `http://127.0.0.1:5000`.
2. Use the provided credentials to log in:
    - Admin: `admin` / `admin`
    - Super User: `super` / `user`
    - User: `user` / `user`
    - Demo User: `demo` / `user`
    - Dummy User: `dummy` / `dummy`
3. Explore the functionalities of the system such as adding sections, managing books, issuing and returning books, and visualizing data.

## ER Diagram
![ER Diagram](https://raw.githubusercontent.com/Akashkunwar/Library_Management_System/main/ERD.png)

## Wireframe
![Wireframe](https://raw.githubusercontent.com/Akashkunwar/Library_Management_System/main/LMS.jpeg)

## Future Enhancements

In version 2.0, we plan to introduce the following major changes:

### Technologies
- **Frontend**: Vue.js
- **Backend Enhancements**: API-driven operations, Redis for caching, and Celery for batch jobs.

### Functionality
- **General User Signup and Login**: Using RBAC (Role-Based Access Control)
- **Mandatory Librarian Login**: Using RBAC
- **Advanced Security**: User and admin authentication using username or email and password with Flask Security or JWT-based Token Authentication

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---

Feel free to contact me if you have any questions or suggestions. Thank you for checking out my project!
