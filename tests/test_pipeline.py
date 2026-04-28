import pytest
import os
from core.pipeline import OSINTPipeline

os.environ["DEBUG_MODE"] = "true"

@pytest.mark.asyncio
async def test_pipeline_runs_successfully():
    pipeline = OSINTPipeline()
    result = await pipeline.run("test_target_APT32")
    
    assert result["status"] == "success"
    assert result["target"] == "test_target_APT32"
    assert result["threats_found"] >= 0
    assert "report_path" in result

@pytest.mark.asyncio
async def test_pipeline_generates_report_file():
    pipeline = OSINTPipeline()
    result = await pipeline.run("test_target_Lazarus")
    
    assert os.path.exists(result["report_path"])
