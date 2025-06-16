import asyncio
from utils.config import precompute_vector_store
from utils.reports import IPCC_REPORTS
import os

async def main():
    for report_name, report_file in IPCC_REPORTS.items():
        report_path = f"data/reports/{report_file}"
        print(f"⏳ Precomputing vectors for {report_file}...")
        result = await precompute_vector_store(report_path)
        print(f"✅ {result}")

if __name__ == "__main__":
    asyncio.run(main())
