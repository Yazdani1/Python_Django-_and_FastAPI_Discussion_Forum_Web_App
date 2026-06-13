export type TUserRole = 'guest' | 'user' | 'moderator' | 'admin';

export interface IAuthUser {
  id: string;
  email: string;
  username: string;
  role: TUserRole;
  avatar_url: string | null;
}

export interface IAuthState {
  user: IAuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface ILoginRequest {
  email: string;
  password: string;
}

export interface IRegisterRequest {
  email: string;
  username: string;
  password: string;
}
