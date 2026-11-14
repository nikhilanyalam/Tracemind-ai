from fastapi import FastAPI
import httpx
from simulator.shared.telemetry import setup_telemetry

app = FastAPI(title="Gateway Service")
tracer = setup_telemetry(app, "gateway-service")

@app.get("/checkout")
async def checkout(item_id: str):
    # Create a custom span for this specific operation
    with tracer.start_as_current_span("gateway_checkout_process") as span:
        span.set_attribute("item_id", item_id)
        
        async with httpx.AsyncClient() as client:
            # Call the downstream Order Service running on port 8001
            response = await client.get(f"http://localhost:8001/process-order?item_id={item_id}")
        
        return {"status": "checkout_complete", "order_service": response.json()}