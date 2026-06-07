"""Generate LinkedIn post texts for all blog posts."""

import re
from pathlib import Path

SITE_URL = "https://mauroloprete.github.io/mauroloprete/blog/posts"

# Post data: (dir, title, description, hashtags)
POSTS = [
    (
        "spark-de-ideas-intro",
        "Spark de Ideas: la chispa de la ingeniería de datos en español",
        "Por qué hace falta un podcast de Data Engineering en español. Databricks, arquitectura de datos, MLOps y carrera — desde la región, para la región.",
        "#DataEngineering #Podcast #Databricks #SparkDeIdeas",
    ),
    (
        "fundamentals-data-engineering",
        "Fundamentals of Data Engineering: las bases que todo ingeniero de datos necesita",
        "Review del libro de Joe Reis y Matt Housley (O'Reilly, 2da ed.). Ciclo de vida del dato, arquitecturas clave, undercurrents y qué cambió en esta edición.",
        "#DataEngineering #BookReview #FundamentalsOfDE",
    ),
    (
        "dataops-pipelines",
        "DataOps: cómo llevar tus pipelines al siguiente nivel",
        "Qué es DataOps de verdad, en qué se diferencia de DevOps, los tres pilares (automatización, observabilidad, colaboración) y errores comunes en producción.",
        "#DataOps #DataEngineering #Pipelines #DevOps",
    ),
    (
        "data-engineering-design-patterns",
        "Data Engineering Design Patterns: 8 patrones de ingesta que tenés que conocer",
        "Los 8 patrones de ingesta del libro de Bartosz Konieczny. Ejemplos en PySpark/SQL y cómo mapean a la arquitectura Medallion.",
        "#DataEngineering #DesignPatterns #PySpark #Medallion",
    ),
    (
        "si-arrancara-de-cero",
        "Si empezara de cero... qué priorizaría aprender en Data Engineering",
        "Python, SQL, Spark, dbt, Databricks — el orden importa. Lo que aprendí después de años laburando con datos y lo que haría distinto si volviera a empezar.",
        "#DataEngineering #Carrera #Python #SQL #Spark",
    ),
    (
        "databricks-asset-bundles-advanced",
        "Databricks Tips #1: Asset Bundles — lo que no te cuentan en la documentación",
        "Casos avanzados, patrones de deployment, variables complejas y trucos que descubrí laburando con DABs en producción.",
        "#Databricks #AssetBundles #DevOps #DataEngineering",
    ),
    (
        "databricks-tips-01-delta-lake",
        "Databricks Tips #2: 7 cosas de Delta Lake que ojalá me hubieran dicho antes",
        "Liquid clustering, OPTIMIZE, Z-ORDER, vacuum, time travel y trucos que cambian cómo trabajás con Delta.",
        "#Databricks #DeltaLake #DataEngineering #LiquidClustering",
    ),
    (
        "databricks-tips-02-unity-catalog",
        "Databricks Tips #3: Unity Catalog — el modelo de gobernanza que nadie implementa bien",
        "Namespace de 3 niveles, GRANTS heredados, linaje automático, row/column security y errores comunes de gobernanza.",
        "#Databricks #UnityCatalog #DataGovernance #DataEngineering",
    ),
    (
        "databricks-tips-03-structured-streaming",
        "Databricks Tips #4: Structured Streaming — watermarks, triggers y las trampas del micro-batch",
        "Trigger modes, watermarks, foreachBatch, Auto Loader y las trampas que te hacen perder datos o plata.",
        "#Databricks #StructuredStreaming #Streaming #DataEngineering",
    ),
    (
        "databricks-tips-04-mlflow-unity-catalog",
        "Databricks Tips #5: MLflow + Unity Catalog — del experimento al modelo en producción",
        "Registro de modelos en UC, aliases en vez de stages, linaje de datos a modelo, y model serving con AI Gateway.",
        "#Databricks #MLflow #UnityCatalog #MLOps",
    ),
    (
        "databricks-tips-05-feature-engineering",
        "Databricks Tips #6: Feature Engineering — features que sobrevivan a producción",
        "Feature Store, point-in-time lookups, online features, feature freshness y los errores clásicos de data leakage.",
        "#Databricks #FeatureEngineering #MLOps #DataEngineering",
    ),
    (
        "data-modeling-medallion-vault-kimball",
        "Medallion vs Data Vault vs Kimball: cuándo usar cada uno y por qué importa",
        "Comparativa práctica de los tres modelos de datos más usados en la industria. Con ejemplos reales, trade-offs y una guía para elegir.",
        "#DataModeling #Medallion #DataVault #Kimball #DataArchitecture",
    ),
    (
        "data-contracts-framework",
        "Data Contracts: cómo diseñar un framework desde cero",
        "Qué son los Data Contracts, por qué los necesitás, y cómo implementé un framework en producción con Databricks y PySpark.",
        "#DataContracts #DataArchitecture #Databricks #PySpark",
    ),
    (
        "data-mesh-practica",
        "Data Mesh en la práctica: lo que funciona, lo que no, y lo que nadie te dice",
        "Data Mesh más allá del hype. Los 4 principios, implementación real con Unity Catalog, y por qué la mayoría de las empresas lo implementan mal.",
        "#DataMesh #DataArchitecture #UnityCatalog #Databricks",
    ),
    (
        "databricks-tips-06-docker-containers",
        "Databricks Tips #7: Docker en Databricks — contenedores custom para entornos que no se rompen",
        "Databricks Container Services, imágenes custom, golden containers, CI/CD con Docker y los errores que te van a hacer perder horas.",
        "#Databricks #Docker #DataEngineering #CICD",
    ),
    (
        "databricks-tips-08-jobs-workflows",
        "Databricks Tips #8: Jobs & Workflows — streaming y triggers que arrancan solos",
        "File arrival triggers, table update triggers, Trigger.AvailableNow, Job Clusters y las limitaciones que no están en el tutorial.",
        "#Databricks #Workflows #Streaming #DataEngineering",
    ),
    (
        "databricks-tips-09-sql-warehouses",
        "Databricks Tips #9: SQL Warehouses — el compute que se prende solo",
        "Classic, Pro o Serverless: cuál elegir, cómo dimensionarlo y qué gotchas te van a ahorrar plata.",
        "#Databricks #SQLWarehouses #Serverless #DataEngineering",
    ),
    (
        "databricks-tips-10-lakeflow-declarative-pipelines",
        "Databricks Tips #10: Lakeflow Declarative Pipelines (ex DLT)",
        "Streaming tables, materialized views, expectations, AUTO CDC con SCD Type 1/2, modos triggered vs continuous y serverless.",
        "#Databricks #DLT #Lakeflow #DataEngineering #Streaming",
    ),
    (
        "databricks-tips-11-ai-gateway",
        "Databricks Tips #11: Unity AI Gateway — governance centralizada para LLMs",
        "Rate limiting, guardrails, usage tracking, cost attribution, fallbacks y traffic splitting para gobernar LLMs en producción.",
        "#Databricks #AIGateway #LLM #MLOps #GenAI",
    ),
]


def generate_linkedin_text(title: str, description: str, hashtags: str) -> str:
    """Generate engaging LinkedIn post text."""
    lines = [
        f"🚀 Nuevo post: {title}",
        "",
        description,
        "",
        "👉 Link en el primer comentario",
        "",
        hashtags,
    ]
    return "\n".join(lines)


def main() -> None:
    base = Path("blog/posts")
    for dir_name, title, desc, tags in POSTS:
        text = generate_linkedin_text(title, desc, tags)
        out = base / dir_name / "linkedin.txt"
        out.write_text(text, encoding="utf-8")
        print(f"Generated: {out}")

    # Also generate a comment template with the link
    for dir_name, *_ in POSTS:
        slug = dir_name
        url = f"{SITE_URL}/{slug}/"
        comment = f"📖 Leelo acá: {url}"
        out = base / dir_name / "linkedin_comment.txt"
        out.write_text(comment, encoding="utf-8")

    print(f"\nDone! Generated {len(POSTS)} LinkedIn texts + comments.")


if __name__ == "__main__":
    main()
