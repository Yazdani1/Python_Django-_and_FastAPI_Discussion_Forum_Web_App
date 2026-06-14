export interface IVoteRequest {
  vote_type: 'up' | 'down';
}

export interface IVoteResult {
  vote_count: number;
  user_vote: string | null;
}
