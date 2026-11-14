import time
from fastapi import FastAPI
from simulator.shared.telemetry import setup_telemetry

app = FastAPI(title="Order Service")
tracer = setup_telemetry(app, "order-service")

@app.get("/process-order")
def process_order(item_id: str):
    with tracer.start_as_current_span("process_order_logic") as span:
        span.set_attribute("item_id", item_id)
        
        # Simulate some processing time
        time.sleep(0.1)
        
        # Log a specific event inside the trace
        span.add_event("Order validated and saved to DB (simulated)")
        return {"message": f"Order for item '{item_id}' processed successfully."}