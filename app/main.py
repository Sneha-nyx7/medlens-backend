import time
import asyncio

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    AnalysisResponse,
    Citation,
    LatencyBreakdown,
    StructuredReport,
)

from app.agents.vision_agent import run_vision_and_gradcam
from app.agents.context_agent import run_biomedbert
from app.agents.retrieval_agent import query_chromadb
from app.agents.report_agent import generate_llm_report
from app.agents.verification_agent import verify_and_triage


app = FastAPI(title="MedLens Backend API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "MedLens Backend Running"}


@app.post(
    "/api/v1/analyze",
    response_model=AnalysisResponse,
)
async def analyze_chest_xray(
    image: UploadFile = File(...),
    clinical_note: str = Form(""),
    session_id: str = Form(...),
):

    start_total = time.time()

    try:

        image_bytes = await image.read()

        # PHASE 1 — PARALLEL EXECUTION

        t0_parallel = time.time()

        vision_task = asyncio.create_task(
            run_vision_and_gradcam(image_bytes)
        )

        context_task = asyncio.create_task(
            run_biomedbert(clinical_note)
        )

        pathologies, heatmap_b64 = await vision_task

        embeddings, entities = await context_task

        t_parallel = time.time() - t0_parallel

        # PHASE 2 — RETRIEVAL

        t0_ret = time.time()

        retrieved_passages = await query_chromadb(
            entities,
            embeddings,
        )

        t_ret = time.time() - t0_ret

        # PHASE 3 — REPORT GENERATION

        t0_report = time.time()

        raw_report, short_citations = (
            await generate_llm_report(
                pathologies,
                entities,
                retrieved_passages,
            )
        )

        t_report = time.time() - t0_report

        # PHASE 4 — VERIFICATION

        triage_level, triage_justification = (
            await verify_and_triage(
                raw_report,
                retrieved_passages,
                pathologies,
            )
        )

        # BUILD FULL CITATIONS

        compiled_citations = []

        for citation in short_citations:

            for passage in retrieved_passages:

                if (
                    passage["passage_id"]
                    == citation["passage_id"]
                ):

                    compiled_citations.append(
                        Citation(
                            marker=citation["marker"],
                            passage_id=passage["passage_id"],
                            source=passage["source"],
                            passage=passage["passage"],
                        )
                    )

        total_latency = time.time() - start_total

        response = AnalysisResponse(
            pathologies=pathologies,
            heatmap_base64=heatmap_b64,
            structured_report=StructuredReport(
                **raw_report
            ),
            citations=compiled_citations,
            triage_level=triage_level,
            triage_justification=triage_justification,
            latency_breakdown=LatencyBreakdown(
                vision=round(t_parallel, 2),
                context=round(t_parallel, 2),
                retrieval=round(t_ret, 2),
                report=round(t_report, 2),
                total=round(total_latency, 2),
            ),
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Backend Error: {str(e)}",
        )