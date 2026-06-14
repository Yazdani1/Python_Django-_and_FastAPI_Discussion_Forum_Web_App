import { type FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Avatar, Box, Chip, Typography } from '@mui/material';
import { ChatBubbleOutline, Delete, Edit } from '@mui/icons-material';
import { postService } from '@/services/postService';
import { voteService } from '@/services/voteService';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/router/routes';
import type { IApiResponse } from '@/types/api.types';
import type { IPostListItem } from '@/types/post.types';
import type { IVoteResult } from '@/types/vote.types';
import { VoteButtons } from './VoteButtons';
import { ActionsMenu } from '@/components/common/ActionsMenu';

interface IPostRowProps {
  post: IPostListItem;
  queryKey: object;
}

export const PostRow: FC<IPostRowProps> = ({ post, queryKey }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const isOwner = user?.id === post.author.id;
  const isPrivileged = user?.role === 'moderator' || user?.role === 'admin';
  const canManage = isOwner || isPrivileged;

  const applyVoteResult = (result: IApiResponse<IVoteResult>) => {
    if (result.data == null) return;
    const newCount = result.data.vote_count;
    queryClient.setQueryData(
      ['posts', queryKey],
      (old: IApiResponse<IPostListItem[]> | undefined) => {
        if (!old?.data) return old;
        return { ...old, data: old.data.map(p => p.id === post.id ? { ...p, vote_count: newCount } : p) };
      },
    );
  };

  const voteMutation = useMutation({
    mutationFn: () => voteService.votePost(post.id, { vote_type: 'up' }),
    onSuccess: applyVoteResult,
  });

  const deleteMutation = useMutation({
    mutationFn: () => postService.deletePost(post.id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['posts'] }),
  });

  const formattedDate = new Date(post.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

  return (
    <Box
      sx={{
        display: 'flex',
        gap: 2,
        p: { xs: 2, sm: 3 },
        alignItems: 'flex-start',
        '&:hover': { bgcolor: 'rgba(99,102,241,0.03)' },
        transition: 'background-color 0.15s',
      }}
    >
      {/* Vote + stats column */}
      <Box
        sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1, minWidth: 52, pt: 0.5 }}
        onClick={(e) => e.stopPropagation()}
      >
        <VoteButtons
          voteCount={post.vote_count}
          onToggle={() => voteMutation.mutate()}
          isLoading={voteMutation.isPending}
          disabled={!user}
        />
        <Chip
          icon={<ChatBubbleOutline sx={{ fontSize: '13px !important' }} />}
          label={post.answer_count}
          size="small"
          variant="outlined"
          sx={{ fontSize: 11, height: 22, color: 'text.secondary', borderColor: 'divider' }}
        />
      </Box>

      {/* Content column */}
      <Box
        sx={{ flexGrow: 1, cursor: 'pointer', minWidth: 0 }}
        onClick={() => navigate(ROUTES.POST_DETAIL(post.id))}
      >
        <Typography
          variant="subtitle1"
          fontWeight={600}
          sx={{ color: 'text.primary', lineHeight: 1.4, mb: 0.5, '&:hover': { color: 'primary.main' }, transition: 'color 0.15s' }}
        >
          {post.title}
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ mb: 1.5, lineHeight: 1.6, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}
        >
          {post.preview}
          {post.preview.length >= 200 && '…'}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
          <Avatar
            src={post.author.avatar_url ?? undefined}
            sx={{ width: 20, height: 20, bgcolor: 'primary.main', fontSize: 10 }}
          >
            {post.author.username[0].toUpperCase()}
          </Avatar>
          <Typography variant="caption" color="text.secondary">{post.author.username}</Typography>
          <Typography variant="caption" color="text.disabled">·</Typography>
          <Typography variant="caption" color="text.disabled">{formattedDate}</Typography>
        </Box>
      </Box>

      {/* Actions menu — only visible to owner / mod / admin */}
      {canManage && (
        <Box onClick={(e) => e.stopPropagation()} sx={{ flexShrink: 0, pt: 0.25 }}>
          <ActionsMenu
            items={[
              {
                label: 'Edit',
                icon: <Edit fontSize="small" />,
                onClick: () => navigate(ROUTES.EDIT_POST(post.id)),
              },
              {
                label: 'Delete',
                icon: <Delete fontSize="small" />,
                onClick: () => deleteMutation.mutate(),
                color: 'error',
                disabled: deleteMutation.isPending,
              },
            ]}
          />
        </Box>
      )}
    </Box>
  );
};
