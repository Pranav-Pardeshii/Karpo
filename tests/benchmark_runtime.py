"""
Runtime performance and latency benchmark for Smart Crop Advisory API.
"""

import asyncio
import time

from httpx import ASGITransport, AsyncClient

from crop_advisory.api.main import create_app


async def benchmark():
    t0 = time.perf_counter()
    app = create_app()
    async with app.router.lifespan_context(app):
        t_startup = (time.perf_counter() - t0) * 1000
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Health Liveness
            t = time.perf_counter()
            r_live = await client.get("/api/v1/health/live")
            t_live = (time.perf_counter() - t) * 1000

            # 2. Health Readiness
            t = time.perf_counter()
            r_ready = await client.get("/api/v1/health/ready")
            t_ready = (time.perf_counter() - t) * 1000

            # 3. Crop Recommendation
            rec_payload = {
                "n": 90.0,
                "p": 42.0,
                "k": 43.0,
                "temperature": 21.0,
                "humidity": 82.0,
                "ph": 6.5,
                "rainfall": 202.0,
                "top_k": 3,
            }
            t = time.perf_counter()
            r_rec = await client.post("/api/v1/crops/recommend", json=rec_payload)
            t_rec = (time.perf_counter() - t) * 1000

            # 4. Yield Prediction
            yield_payload = {
                "crop": "rice",
                "season": "Kharif",
                "state": "Maharashtra",
                "soil_type": "Vertisols",
                "temperature": 25.0,
                "rainfall": 900.0,
                "humidity": 70.0,
                "ph": 6.5,
                "nitrogen": 90.0,
                "phosphorus": 40.0,
                "potassium": 40.0,
                "fertilizer": 100.0,
                "pesticide": 0.35,
            }
            t = time.perf_counter()
            r_yield = await client.post("/api/v1/yield/predict", json=yield_payload)
            t_yield = (time.perf_counter() - t) * 1000

            # 5. Full Advisory
            advisory_payload = {
                "n": 90.0,
                "p": 42.0,
                "k": 43.0,
                "temperature": 21.0,
                "humidity": 82.0,
                "ph": 6.5,
                "rainfall": 202.0,
                "state": "Maharashtra",
                "soil_type": "Vertisols",
                "season": "Kharif",
                "farm_area": 3.0,
                "area_unit": "acre",
                "top_k": 3,
            }
            t = time.perf_counter()
            r_advisory = await client.post("/api/v1/advisory/full", json=advisory_payload)
            t_advisory = (time.perf_counter() - t) * 1000

            # 6. OpenAPI JSON
            r_openapi = await client.get("/openapi.json")
            openapi_spec = r_openapi.json()
            paths_count = len(openapi_spec["paths"])

            print("=== REAL BENCHMARK MEASUREMENTS ===")
            print(f"Application & Model Startup Time: {t_startup:.2f} ms")
            print(f"Liveness Probe Latency: {t_live:.2f} ms (Status: {r_live.status_code})")
            print(f"Readiness Probe Latency: {t_ready:.2f} ms (Status: {r_ready.status_code})")
            print(
                f"Crop Recommendation Latency: {t_rec:.2f} ms (Status: {r_rec.status_code}, Top: {r_rec.json()['primary_crop']})"
            )
            print(
                f"Yield Prediction Latency: {t_yield:.2f} ms (Status: {r_yield.status_code}, Yield: {r_yield.json()['predicted_yield_kg_ha']} kg/ha)"
            )
            print(
                f"Full Composite Advisory Latency: {t_advisory:.2f} ms (Status: {r_advisory.status_code})"
            )
            print(f"OpenAPI Registered Paths: {paths_count}")


if __name__ == "__main__":
    asyncio.run(benchmark())
