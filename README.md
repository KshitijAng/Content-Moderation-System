# Content Moderation System

## Overview

This project is a **scalable AI-powered content moderation system** built using **FastAPI, Celery, PostgreSQL, Redis, and OpenAI’s Moderation API**. It can process text content asynchronously and store moderation results in a database while ensuring high throughput and fault tolerance.

## Why is This Needed?

In modern applications, user-generated content (UGC) can contain harmful or inappropriate text. A content moderation system helps:

- **Filter out harmful content** before it reaches users.
- **Ensure compliance** with platform policies.
- **Automate moderation** using AI instead of manual review.
- **Handle large-scale moderation requests asynchronously.**

## Features

✅ **FastAPI for API endpoints**
✅ **OpenAI Moderation API integration**
✅ **Asynchronous processing with Celery & Redis**
✅ **PostgreSQL for persistent storage**
✅ **Docker & Docker Compose setup for easy deployment**
✅ **Automatic retries with exponential backoff** for failed tasks
✅ **REST API endpoints for moderation and task status tracking**

---

## 🚀 How to Use

### **1️⃣ Prerequisites**

Ensure you have the following installed:

- **Docker & Docker Compose**
- **Python 3.12**
- **An OpenAI API Key**

### **2️⃣ Clone the Repository**

```sh
git clone https://github.com/your-repo/content-moderation.git
cd content-moderation
```

### **3️⃣ Set Up Environment Variables**

Create a `.env` file and add:

```ini
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://postgres:mysecretpassword@db:5432/postgres
REDIS_URL=redis://redis:6379/0
```

### **4️⃣ Run the Application with Docker**

```sh
docker-compose up --build
```

This will start:
✅ **PostgreSQL** on `localhost:5432`
✅ **Redis** on `localhost:6379`
✅ **FastAPI** on `localhost:8000`
✅ **Celery Worker** for async processing

### **5️⃣ Test the API**

#### **Submit a Text for Moderation**

Access FastAPI's Swagger UI using **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**, enter the text in the **moderate/text** section, and click **Execute**. The response will look like this:

```json
{
  "id": "c8c1d6f3-44b3-4d39-b04d-dcb0d5a1eb21",
  "flagged": false,
  "categories": {},
  "category_scores": {}
}
```

#### **Check Task Status**

Copy the `id` from the response and paste it into the **task/{task\_id}** section to get more details about the moderation results:

```json
{
  "status": "Completed",
  "result": {
    "flagged": false,
    "categories": {
      "sexual": false,
      "hate": false,
      "harassment": false,
      "self-harm": false,
      "sexual/minors": false,
      "hate/threatening": false,
      "violence/graphic": false,
      "self-harm/intent": false,
      "self-harm/instructions": false,
      "harassment/threatening": false,
      "violence": false
    },
    "category_scores": {
      "sexual": 0.0006504094344563782,
      "hate": 0.000025428740627830848,
      "harassment": 0.00003054423359571956,
      "self-harm": 0.000032383639336330816,
      "sexual/minors": 0.00005876993964193389,
      "hate/threatening": 2.25505047524166e-7,
      "violence/graphic": 0.00003652232771855779,
      "self-harm/intent": 0.000029279632144607604,
      "self-harm/instructions": 0.000056661148846615106,
      "harassment/threatening": 0.0000012931146784467273,
      "violence": 0.000026649413484847173
    }
  }
}
```

#### **Get Moderation Stats**

```json
{
  "total_requests": 4,
  "flagged_count": 0
}
```

### **7️⃣ Open Swagger UI**

Go to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** for interactive API documentation.

---

## 🛠️ Technologies Used

- **FastAPI** - High-performance backend framework
- **Celery** - Task queue for async processing
- **Redis** - Message broker for Celery
- **PostgreSQL** - Database for storing moderation results
- **Alembic** - Database migration tool
- **Docker & Docker Compose** - Containerized deployment
- **OpenAI API** - AI-powered content moderation

---

## 📌 Why Do We Need Redis, Celery, and Alembic?

### **🔹 Redis**

Redis is used as a **message broker** for Celery. It allows tasks to be queued and processed asynchronously. Without Redis, Celery wouldn’t be able to efficiently distribute and handle tasks in a scalable way.

### **🔹 Celery**

Celery is responsible for **asynchronous task execution**. When a moderation request is submitted, Celery processes it in the background, ensuring that the API remains fast and responsive.

---

## 🎯 Future Improvements

- Add **rate limiting** to prevent API abuse
- Implement **Redis caching** for faster responses
- Set up **Prometheus & Grafana** for monitoring
- Improve **unit tests & CI/CD deployment**

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve this project!

## 📜 License

This project is licensed under the MIT License.

