import { ApiService } from '@/api/service';
import type { IApiResponse } from '@/types/api.types';
import type { IVoteRequest, IVoteResult } from '@/types/vote.types';

export const voteService = {
  votePost(postId: string, data: IVoteRequest): Promise<IApiResponse<IVoteResult>> {
    return ApiService.post<IVoteResult>(`/api/v1/posts/${postId}/vote`, data);
  },

  removePostVote(postId: string): Promise<IApiResponse<IVoteResult>> {
    return ApiService.delete<IVoteResult>(`/api/v1/posts/${postId}/vote`);
  },

  voteAnswer(answerId: string, data: IVoteRequest): Promise<IApiResponse<IVoteResult>> {
    return ApiService.post<IVoteResult>(`/api/v1/answers/${answerId}/vote`, data);
  },

  removeAnswerVote(answerId: string): Promise<IApiResponse<IVoteResult>> {
    return ApiService.delete<IVoteResult>(`/api/v1/answers/${answerId}/vote`);
  },
};
