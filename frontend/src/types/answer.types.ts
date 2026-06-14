import type { IPostAuthor } from './post.types';

export interface IAnswer {
  id: string;
  content: string;
  author: IPostAuthor;
  post_id: string;
  vote_count: number;
  user_vote: string | null;
  created_at: string;
  updated_at: string;
}

export interface IAnswerCreateRequest {
  content: string;
}

export interface IAnswerUpdateRequest {
  content: string;
}
