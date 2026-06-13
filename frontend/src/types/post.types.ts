import type { TUserRole } from './auth.types';

export interface IPostAuthor {
  id: string;
  username: string;
  avatar_url: string | null;
  role: TUserRole;
}

export interface IPost {
  id: string;
  title: string;
  content: string;
  author: IPostAuthor;
  created_at: string;
  updated_at: string;
}

export interface IPostListItem {
  id: string;
  title: string;
  preview: string;
  author: IPostAuthor;
  created_at: string;
}

export interface IPostCreateRequest {
  title: string;
  content: string;
}

export interface IPostUpdateRequest {
  title?: string;
  content?: string;
}

export interface IPostSearchParams {
  search?: string;
  date_from?: string;
  date_to?: string;
  page?: number;
  page_size?: number;
}
