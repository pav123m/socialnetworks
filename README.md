# socialnetworks
# Social Network API

## Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/pav123m/socialnetworks.git
    cd socialnetwork
    ```

2. **Build and run the Docker containers:**

    Make sure Docker is installed and running on your system.

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images specified in `docker-compose.yml` and start the containers.

3. **Run migrations:**

    Open a new terminal window/tab, navigate to the `socialnetwork` directory, and run:

    ```bash
    docker-compose run web python manage.py migrate
    ```

    This will apply any database migrations needed for the project.

4. **Create a superuser:**

    Still in the `socialnetwork` directory, run:

    ```bash
    docker-compose run web python manage.py createsuperuser
    ```

    Follow the prompts to create a superuser account. This account can be used to access the Django admin interface.

5. **Access the API:**

    Once the containers are up and running, you can access the API at:

    ```
    http://localhost:8000/api/
    ```

    The API endpoints can be explored using tools like Postman or by integrating with your frontend application.

6. **Postman Collection:**

    - Create a Postman collection with the endpoints described in the API.
    - Export the collection as a JSON file and include it in your repository.

7. **Additional Notes:**

    - Ensure Docker and Docker Compose are properly configured and running on your system.
    - Update any environment-specific settings (like `DATABASE_HOST` in `docker-compose.yml`) as per your setup.

