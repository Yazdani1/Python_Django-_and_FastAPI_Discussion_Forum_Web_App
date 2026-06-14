import { ApiService } from '@/api/service';
import type { IApiResponse } from '@/types/api.types';
import type { IAnswer, IAnswerCreateRequest, IAnswerUpdateRequest } from '@/types/answer.types';

export const answerService = {
  listAnswers(postId: string): Promise<IApiResponse<IAnswer[]>> {
    return ApiService.get<IAnswer[]>(`/api/v1/posts/${postId}/answers`);
  },

  addAnswer(postId: string, data: IAnswerCreateRequest): Promise<IApiResponse<IAnswer>> {
    return ApiService.post<IAnswer>(`/api/v1/posts/${postId}/answers`, data, {
      showSuccessToast: true,
      successMessage: 'Answer posted!',
    });
  },

  updateAnswer(answerId: string, data: IAnswerUpdateRequest): Promise<IApiResponse<IAnswer>> {
    return ApiService.put<IAnswer>(`/api/v1/answers/${answerId}`, data, {
      showSuccessToast: true,
      successMessage: 'Answer updated!',
    });
  },

  deleteAnswer(answerId: string): Promise<IApiResponse<null>> {
    return ApiService.delete<null>(`/api/v1/answers/${answerId}`, {
      showSuccessToast: true,
      successMessage: 'Answer deleted.',
    });
  },
};
