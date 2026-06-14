import { ApiService } from '@/api/service';
import type { IApiResponse } from '@/types/api.types';

export const adminService = {
  blockUser(userId: string): Promise<IApiResponse<null>> {
    return ApiService.post<null>(`/api/v1/admin/users/${userId}/block`, undefined, {
      showSuccessToast: true,
      successMessage: 'User blocked.',
    });
  },

  unblockUser(userId: string): Promise<IApiResponse<null>> {
    return ApiService.post<null>(`/api/v1/admin/users/${userId}/unblock`, undefined, {
      showSuccessToast: true,
      successMessage: 'User unblocked.',
    });
  },
};
