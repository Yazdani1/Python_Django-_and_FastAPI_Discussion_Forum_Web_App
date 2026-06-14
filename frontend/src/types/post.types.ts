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
  vote_count: number;
  answer_count: number;
  user_vote: string | null;
  created_at: string;
  updated_at: string;
}

export interface IPostListItem {
  id: string;
  title: string;
  preview: string;
  author: IPostAuthor;
  answer_count: number;
  vote_count: number;
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
  author?: string;
  date_from?: string;
  date_to?: string;
  page?: number;
  page_size?: number;
}
