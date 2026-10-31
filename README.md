<div align="center">
  <img src="./profile.svg" alt="Jhonatan Sánchez — perfil de backend" width="100%" />
</div>

> **EN — short version:** Systems Engineering student (6th semester), backend-focused.
> I build REST APIs with NestJS/Prisma and FastAPI/PostgreSQL, plus Python automation and
> scraping scripts. Open to small freelance work: bug fixes and data extraction.

## Sobre mí

Desarrollador backend, estudiante de Ingeniería de Sistemas (6º semestre). Construyo APIs
con NestJS + Prisma y FastAPI + PostgreSQL, y automatizo con Python lo que antes se hacía
a mano: scraping, extracción de datos y procesos que corren solos.

Me interesa el problema completo: modelar los datos, asegurar los endpoints, dejarlos
dockerizados y cubiertos con tests. Cuando el proyecto lo pide, también trabajo el
frontend con Next.js o React.

## Stack

<p>
  <img src="https://img.shields.io/badge/NestJS-E0234E?style=for-the-badge&logo=nestjs&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Prisma-2D3748?style=for-the-badge&logo=prisma&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-FF4438?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/JWT-191919?style=for-the-badge&logo=jsonwebtokens&logoColor=white" />
  <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" />
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/Jest-C21325?style=for-the-badge&logo=jest&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" />
  <img src="https://img.shields.io/badge/Expo-000020?style=for-the-badge&logo=expo&logoColor=white" />
  <img src="https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
</p>

## Entornos

<p>
  <img src="https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/WSL-4D4D4D?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCode-000000?style=for-the-badge&logo=opencode&logoColor=white" />
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white" />
</p>

## Proyectos

### [`book-scraper`](https://github.com/jhonatan-sz/book-scraper)

**Problema:** extraer un catálogo completo de 1000 libros repartido en 50 páginas de
listado, sin duplicados y con los datos validados.

**Solución:** el listado descubre URLs y cada página de detalle es la fuente canónica
(título, precio, rating, stock, categoría). Deduplicación por URL, salida CSV o JSON
validada, y tests sobre fixtures HTML guardados para no golpear el sitio en cada corrida.

**Stack:** Python (solo stdlib en runtime), pytest, uv.

### `lynx-stats-backend` — privado

**Problema:** API para estadísticas deportivas, con ingestión pesada y consultas
frecuentes sobre la misma data.

**Solución:** FastAPI async con SQLAlchemy, PostgreSQL y migraciones con Alembic, caché y
colas en segundo plano con Redis + arq, todo levantado con docker-compose y cubierto con
pytest.

**Estado:** pausado. El modelo predictivo no superó el baseline, así que no lo publiqué
como producto. El código sigue privado; la arquitectura es lo que quedó de ese trabajo.

## Ahora mismo

Construyendo una API de referencia con **NestJS + Prisma** — auth con JWT, roles,
migraciones, Swagger, tests y docker-compose — para tener mi stack de backend público y
reutilizable como base de proyectos.

## Actividad

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jhonatan-sz/jhonatan-sz/output/github-snake-dark.svg" />
    <img alt="Gráfico de contribuciones" src="https://raw.githubusercontent.com/jhonatan-sz/jhonatan-sz/output/github-snake.svg" />
  </picture>
</div>


## Contacto

Abierto a trabajos freelance pequeños: arreglo de bugs en Python / JS / TS, scripts de
automatización y extracción de datos.

<div align="center">

[![Email](https://img.shields.io/badge/email-jhonatan2000j%40gmail.com-F59E0B?style=flat-square&labelColor=0D1117)](mailto:jhonatan2000j@gmail.com)
[![GitHub](https://img.shields.io/badge/github-jhonatan--sz-F59E0B?style=flat-square&logo=github&labelColor=0D1117)](https://github.com/jhonatan-sz)

</div>
