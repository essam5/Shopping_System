# Shopping_System Project 
- run ---> docker-compose up 
and vist http://localhost:8000/
- run ---> docker-compose run shopping_system python manage.py migrate
# project content 
- Models (user, profile, address , cart, cart_item , product, category, order, order_item) with test cases 
- PostgreSQL database
- black linter 
# ERD for this project is 
https://dbdiagram.io/d/63f65988296d97641d82fd83

Project Name: Flink Kafka CSV Integration
This project is a data pipeline implemented in Java with Apache Flink. It reads JSON data from a Kafka topic, transforms it into CSV format, and then writes the CSV data into a file. It's specifically useful when you need to perform near real-time data transformation from JSON to CSV.

Features
Kafka consumer: Reads data from a specified Kafka topic.
Data Transformation: Converts the consumed JSON data to CSV format.
Data Sink: Writes the CSV data to a specified file system location.
How to Run the Project
This is a Gradle project. You can run it from the command line or an IDE that supports Gradle (like IntelliJ IDEA).

Clone the project with git clone <repository-url>
Navigate to the root directory of the project via cd <project-directory>
Run gradle clean build to build the project
To run the main class, execute gradle run
Prerequisites
Java 8 or higher
Apache Kafka Server (Bootstrap server is hard-coded as "159.203.24.108:9092" in the current version)
Access to the filesystem path "/root/Imsety/integration_kafka" to write the CSV file
Project Structure
The project's main class is Main, and it contains two important inner classes:

JsonToCsvMapper: Implements MapFunction and is responsible for converting the incoming JSON string to a CSV line.
CsvEncoder: An encoder class used to convert Tuple data into CSV format for the StreamingFileSink.
The main method sets up the Flink environment, initializes a Kafka consumer, creates a transformation pipeline to convert the JSON to CSV, and finally sets up a file sink to output the CSV data.

Dependencies
The project uses Apache Flink and Kafka libraries for streaming and data processing. It also uses the Jackson library for JSON processing. The Gradle build file has the following dependencies:

flink-java for Flink's core Java APIs
flink-streaming-java_2.11 for Flink's DataStream API
flink-clients_2.11 to interact with Flink cluster
flink-connector-kafka_2.11 to connect with Kafka
flink-csv to deal with CSV data format
kafka-clients to interact with Kafka broker
jackson-databind for JSON data binding
