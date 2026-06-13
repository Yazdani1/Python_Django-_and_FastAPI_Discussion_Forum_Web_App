import { ApiService } from '@/api/service';
import type { IApiResponse } from '@/types/api.types';
import type {
  IPost,
  IPostCreateRequest,
  IPostListItem,
  IPostSearchParams,
  IPostUpdateRequest,
} from '@/types/post.types';

const BASE = '/api/v1/posts';

export const postService = {
  listPosts(params?: IPostSearchParams): Promise<IApiResponse<IPostListItem[]>> {
    return ApiService.get<IPostListItem[]>(BASE, params as Record<string, unknown>);
  },

  getPost(id: string): Promise<IApiResponse<IPost>> {
    return ApiService.get<IPost>(`${BASE}/${id}`);
  },

  createPost(data: IPostCreateRequest): Promise<IApiResponse<IPost>> {
    return ApiService.post<IPost>(BASE, data, {
      showSuccessToast: true,
      successMessage: 'Post created successfully!',
    });
  },

  updatePost(id: string, data: IPostUpdateRequest): Promise<IApiResponse<IPost>> {
    return ApiService.put<IPost>(`${BASE}/${id}`, data, {
      showSuccessToast: true,
      successMessage: 'Post updated successfully!',
    });
  },

  deletePost(id: string): Promise<IApiResponse<null>> {
    return ApiService.delete<null>(`${BASE}/${id}`, {
      showSuccessToast: true,
      successMessage: 'Post deleted.',
    });
  },
};
