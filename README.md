## Proyecto Microservicios - Materia: Tópicos Avanzados de Desarrollo Web

### Alumnos: Ignacio Niveyro - Gonzalo Razuc

El proyecto consiste en la implementación de una página simple que recomienda películas en función de las peliculas que el usuario examina. La página simplemente muestra un mosaico de posters de peliculas en una grilla. Cuando el usuario clickea un poster puede ver el plot de la película. 
El sistema registra el historial de películas que el usuario viene examinando y recomienda una pelicula en función de las **últimas 3 examinadas**. La recomendación puede ubicarse como poster en un panel aparte, al estilo Youtube, o puede reemplazar alguna pelicula de la grilla. 

La arquitectura general de microservicios es la siguiente:

![Proyecto24](https://github.com/user-attachments/assets/85e96d79-80b4-4f4a-9a62-0370a7b6b36d)

El criterio de recomendación sigue esta prioridad:
 * Primero, recomienda películas del género más examinado.
 * Si no hay peliculas para recomendar del género examinado, sugiere del segundo género examinado.
 * Como último recurso, hace una recomendación aleatoria entre todas las películas.

El microservicio de historial guarda información en RabbitMQ, y el recomendador toma esta información para sugerir alguna película.

### Para ejecutar el proyecto

Tener Docker en su sistema y ejecutar en la raíz del proyecto ``` docker-compose up --build ```
El proyecto se puede probar en https://localhost:3000 
