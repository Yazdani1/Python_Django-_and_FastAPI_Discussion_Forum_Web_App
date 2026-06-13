import type { TUserRole } from './auth.types';

export interface IUserProfile {
  id: string;
  email: string;
  username: string;
  role: TUserRole;
  avatar_url: string | null;
  bio: string | null;
  is_active: boolean;
  created_at: string;
  post_count: number;
}

export interface IUserUpdateRequest {
  username?: string;
  bio?: string;
}
