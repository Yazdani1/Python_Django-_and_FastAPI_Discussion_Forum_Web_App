export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  PROFILE: '/profile',
  CREATE_POST: '/posts/new',
  POST_DETAIL: (id: string) => `/posts/${id}`,
  EDIT_POST: (id: string) => `/posts/${id}/edit`,
  NOT_FOUND: '*',
} as const;

export type TRoute = string;
