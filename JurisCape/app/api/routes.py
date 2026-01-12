from fastapi import APIRouter, HTTPException
from app.models.case_file import CaseFileRequest, FactExtractionResponse
from app.services.llmengine import analyze_case_text
from app.data.legal_codes import BNS_mapping 

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "Juris-Cape System Online"}

@router.post("/analyze", response_model=FactExtractionResponse)
async def analyze_case(request: CaseFileRequest):
    try:
        # Call the AI service
        result = await analyze_case_text(request.case_text)
        
        return FactExtractionResponse(
            case_id=request.case_id,
            chronological_facts=result["chronological_facts"],
            potential_bns_sections=result["potential_bns_sections"],
            summary=result["summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/map-law/{ipc_section}")
async def get_bns_mapping(ipc_section: str):
    mapping = BNS_MAPPING.get(ipc_section)
    if not mapping:
        raise HTTPException(status_code=404, detail="IPC Section not found in mapping")
    return {
        "ipc_section": ipc_section,
        "bns_equivalent": mapping["bns_section"],
        "title": mapping["title"],
        "key_changes": mapping["changes"]
    }