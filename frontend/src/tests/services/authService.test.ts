import { describe, it, expect, vi, beforeEach } from 'vitest';
import { authService } from '@/services/authService';
import { ApiService } from '@/api/service';

vi.mock('@/api/service', () => ({
  ApiService: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

const mockApiService = vi.mocked(ApiService);

const mockUser = {
  id: '123',
  email: 'test@example.com',
  username: 'testuser',
  role: 'user' as const,
  avatar_url: null,
};

const mockResponse = { success: true, message: 'ok', data: mockUser, errors: null, meta: null };

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('calls login endpoint with credentials', async () => {
    mockApiService.post.mockResolvedValue(mockResponse);

    const result = await authService.login({ email: 'test@example.com', password: 'password' });

    expect(mockApiService.post).toHaveBeenCalledWith(
      '/api/v1/auth/login',
      { email: 'test@example.com', password: 'password' },
      expect.objectContaining({ showSuccessToast: true }),
    );
    expect(result.data).toEqual(mockUser);
  });

  it('calls register endpoint with user data', async () => {
    mockApiService.post.mockResolvedValue({ ...mockResponse, message: 'Account created' });

    await authService.register({ email: 'new@example.com', username: 'newuser', password: 'password123' });

    expect(mockApiService.post).toHaveBeenCalledWith(
      '/api/v1/auth/register',
      { email: 'new@example.com', username: 'newuser', password: 'password123' },
      expect.objectContaining({ showSuccessToast: true }),
    );
  });

  it('calls logout endpoint', async () => {
    mockApiService.post.mockResolvedValue({ success: true, message: 'Logged out', data: null, errors: null, meta: null });

    await authService.logout();

    expect(mockApiService.post).toHaveBeenCalledWith(
      '/api/v1/auth/logout',
      undefined,
      expect.objectContaining({ showErrorToast: false }),
    );
  });

  it('calls getMe endpoint', async () => {
    mockApiService.get.mockResolvedValue(mockResponse);

    const result = await authService.getMe();

    expect(mockApiService.get).toHaveBeenCalledWith(
      '/api/v1/users/me',
      undefined,
      expect.objectContaining({ showErrorToast: false }),
    );
    expect(result.data).toEqual(mockUser);
  });
});
