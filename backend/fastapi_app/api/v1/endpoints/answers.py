import uuid

from fastapi import APIRouter, Depends, status

from fastapi_app.api.v1.dependencies import get_answer_service, get_vote_service
from fastapi_app.core.dependencies import get_current_user, get_optional_current_user
from fastapi_app.models.user import User
from fastapi_app.schemas.answer import AnswerCreate, AnswerRead, AnswerUpdate
from fastapi_app.schemas.vote import VoteRequest, VoteResult
from fastapi_app.services.answer_service import AnswerService
from fastapi_app.services.vote_service import VoteService
from fastapi_app.utils.responses import ApiResponse

router = APIRouter(tags=["answers"])


@router.get(
    "/posts/{post_id}/answers",
    response_model=ApiResponse[list[AnswerRead]],
)
async def list_answers(
    post_id: uuid.UUID,
    current_user: User | None = Depends(get_optional_current_user),
    service: AnswerService = Depends(get_answer_service),
) -> ApiResponse[list[AnswerRead]]:
    answers = await service.list_answers(
        post_id, current_user.id if current_user else None
    )
    return ApiResponse.ok(data=answers)


@router.post(
    "/posts/{post_id}/answers",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[AnswerRead],
)
async def add_answer(
    post_id: uuid.UUID,
    data: AnswerCreate,
    current_user: User = Depends(get_current_user),
    service: AnswerService = Depends(get_answer_service),
) -> ApiResponse[AnswerRead]:
    answer = await service.add_answer(post_id, current_user, data)
    return ApiResponse.created(data=answer, message="Answer added successfully")


@router.put("/answers/{answer_id}", response_model=ApiResponse[AnswerRead])
async def update_answer(
    answer_id: uuid.UUID,
    data: AnswerUpdate,
    current_user: User = Depends(get_current_user),
    service: AnswerService = Depends(get_answer_service),
) -> ApiResponse[AnswerRead]:
    answer = await service.update_answer(answer_id, current_user, data)
    return ApiResponse.ok(data=answer, message="Answer updated successfully")


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: AnswerService = Depends(get_answer_service),
) -> None:
    await service.delete_answer(answer_id, current_user)


# ── Vote on answers ───────────────────────────────────────────────────────────


@router.post("/answers/{answer_id}/vote", response_model=ApiResponse[VoteResult])
async def vote_answer(
    answer_id: uuid.UUID,
    data: VoteRequest,
    current_user: User = Depends(get_current_user),
    service: VoteService = Depends(get_vote_service),
) -> ApiResponse[VoteResult]:
    result = await service.vote_answer(answer_id, current_user, data.vote_type)
    return ApiResponse.ok(data=result)


@router.delete(
    "/answers/{answer_id}/vote",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[VoteResult],
)
async def remove_answer_vote(
    answer_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service: VoteService = Depends(get_vote_service),
) -> ApiResponse[VoteResult]:
    result = await service.remove_answer_vote(answer_id, current_user)
    return ApiResponse.ok(data=result)
