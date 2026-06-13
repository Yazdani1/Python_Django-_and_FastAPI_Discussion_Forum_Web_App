import { ApiService } from '@/api/service';
import type { IApiResponse } from '@/types/api.types';
import type { IUserProfile, IUserUpdateRequest } from '@/types/user.types';

const BASE = '/api/v1/users';

export const userService = {
  getProfile(): Promise<IApiResponse<IUserProfile>> {
    return ApiService.get<IUserProfile>(`${BASE}/me`);
  },

  updateProfile(data: IUserUpdateRequest): Promise<IApiResponse<IUserProfile>> {
    return ApiService.patch<IUserProfile>(`${BASE}/me`, data, {
      showSuccessToast: true,
      successMessage: 'Profile updated successfully!',
    });
  },

  uploadAvatar(file: File): Promise<IApiResponse<IUserProfile>> {
    const formData = new FormData();
    formData.append('file', file);
    return ApiService.post<IUserProfile>(`${BASE}/me/avatar`, formData, {
      showSuccessToast: true,
      successMessage: 'Avatar updated!',
    });
  },
};
