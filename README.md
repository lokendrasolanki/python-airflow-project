# Astronomer Project: Reading Data from an API and Writing to PostgreSQL

Welcome to the **Astronomer Project**, which reads data from an external API and writes the data into a PostgreSQL database using Astronomer and Airflow.

---

## 🚀 Prerequisites

Before getting started, ensure you have **Docker** installed on your system.

### 🛠️ Check if Docker is Installed
You can verify if Docker is installed by running:

```bash
docker --version
```

If Docker isn't installed, download and install it from the official website: [Docker Installation Guide](https://docs.docker.com/get-docker/).

---

## 🧭 Astronomer Installation & Setup Steps

Follow the steps below to install and run the Astronomer environment for this project.

---

### 1️⃣ **Install Astronomer CLI**

You need the Astronomer CLI to initialize and interact with the project. Follow the instructions based on your OS from the [Astronomer Installation Documentation](https://www.astronomer.io/docs/).

To verify the installation:

```bash
astro --version
```

---

### 2️⃣ **Clone the Repository**

First, clone the project repository to your local machine:

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
```

Replace `<REPOSITORY_URL>` with the URL of your repository and `<REPOSITORY_DIRECTORY>` with the name of your project directory.

---

### 3️⃣ **Start the Local Environment**

Start the Astronomer environment using:

```bash
astro dev start
```

This will bring up Airflow and other dependencies needed for execution.

---

## 🔗 Setting Up Connections in Airflow

Airflow uses **connections** to communicate with external systems. You need to set up two connections:

1. **PostgreSQL Connection**
2. **HTTP Connection (for accessing the external API)**

Follow these steps:

### 1️⃣ **Add PostgreSQL Connection**

You need to set up the PostgreSQL connection in the Airflow UI:

1. Log in to the Airflow UI at:  
   ```
   http://localhost:8080
   ```
2. Navigate to **Admin → Connections**.
3. Click **+ Add Connection** and configure the following fields:
   - **Connection ID:** `postgres_conn`
   - **Connection Type:** `Postgres`
   - **Host:** `localhost`
   - **Schema:** `<your_database_name>`
   - **Login:** `<your_user>`
   - **Password:** `<your_password>`
   - **Port:** `5432`

Click **Save** after entering the details.

---

### 2️⃣ **Add HTTP Connection**

You need to configure the connection for the external API:

1. Log in to the Airflow UI at:  
   ```
   http://localhost:8080
   ```
2. Navigate to **Admin → Connections**.
3. Click **+ Add Connection** and configure the following fields:
   - **Connection ID:** `api_conn`
   - **Connection Type:** `HTTP`
   - **Host:** `<API_BASE_URL>` (e.g., `https://api.example.com`)

Click **Save** after entering the details.

---

## 🛡️ Troubleshooting

### If `astro dev start` fails:
- Ensure Docker is running.
- Restart the Docker Daemon if necessary.
  
```bash
docker restart
```

### PostgreSQL issues:
- Verify if PostgreSQL is running at port `5432`.
- Recheck the database configuration in `dags/configuration.py`.

---

## 🧑‍💻 Contribution

We welcome contributions to improve this project! If you have ideas, fixes, or enhancements, feel free to fork the repository, make changes, and submit a pull request.

---

Thank you for setting up the **Astronomer Project**! 🚀 If you have any questions, feel free to reach out.