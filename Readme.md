# Endpoints
1. `auth/register/`: details in DocAuth.md
2. `auth/login/`: details in DocAuth.md
3. `regularplan/`: details in DocRegularPlan.md
4. `regularplan/:pk`: details in DocRegularPlan.md
5. `schema/swagger/`: Shows the Swagger documentation version's  


# HOW TO

1. Create a new docker machine with command `docker-machine create your_machine_name`,  where `your_machine_name` is the name of machine that will be created.
2. Create a .env file to define the enviroments variables of project, based in .env.example file.
3. This are the needed enviroment variables:
- DJANGO_SECRET_KEY: The Django secret key
- DJANGO_DEBUG: The Django variable debug. If is debug mode it is true else false.
- DJANGO_PORT: The port with the server django will be running.
- POSTGRES_DB: The Postgres DB name.
- POSTGRES_USER: The postgres username.
- POSTGRES_PASSWORD: The postgres password.
- POSTGRES_HOST: The Postgres host. If running a container define as postgres.
- POSTGRES_PORT: The Postgres port.
- REDIS_HOST: The Redis host. If running a container define as redis.
- REDIS_PORT: The Redis  port.
- REDIS_DB: The Redis DB name.
- MONGODB_HOST: The Mongo host. If running a container define as mongo.
- MONGODB_PORT: The Mongodb port.
- MONGODB_USER: The Mongodb username.
- MONGODB_PASSWORD: The Mongodb password.
- MONGODB_DB: The Mongodb DB name.
- SENDGRID_API_KEY: The Sendgrid API Key.
4. Execute the command `docker-machine start your_machine_name` to start the machine created.
5. Execute the command `docker-compose up --build` to up and build the images.
6. Done! The project is running.
7. To run the tests, execute the command `coverage run manage.py test --settings miio_challenge.settings.test`. This is needed cause defines a variable TEST with `true` in `test.py` file.
