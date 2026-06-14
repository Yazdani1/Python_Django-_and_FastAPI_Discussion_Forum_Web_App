import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  Avatar,
  Box,
  Button,
  CircularProgress,
  Container,
  Divider,
  Paper,
  Tooltip,
  Typography,
} from '@mui/material';
import { ArrowBack, Block, Delete, Edit, LockOpen } from '@mui/icons-material';
import { postService } from '@/services/postService';
import { voteService } from '@/services/voteService';
import { adminService } from '@/services/adminService';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/router/routes';
import { VoteButtons } from '@/components/posts/VoteButtons';
import { ActionsMenu } from '@/components/common/ActionsMenu';
import { AnswerList } from '@/components/answers/AnswerList';

const PostDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: res, isLoading } = useQuery({
    queryKey: ['post', id],
    queryFn: () => postService.getPost(id!),
    enabled: !!id,
  });

  const deleteMutation = useMutation({
    mutationFn: () => postService.deletePost(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      navigate(ROUTES.HOME);
    },
  });

  const voteMutation = useMutation({
    mutationFn: () => voteService.votePost(id!, { vote_type: 'up' }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['post', id] }),
  });

  const blockMutation = useMutation({
    mutationFn: (userId: string) => adminService.blockUser(userId),
  });

  const unblockMutation = useMutation({
    mutationFn: (userId: string) => adminService.unblockUser(userId),
  });

  const post = res?.data;

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!post) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography color="error">Post not found.</Typography>
      </Container>
    );
  }

  const isOwner = user?.id === post.author.id;
  const isPrivileged = user?.role === 'moderator' || user?.role === 'admin';
  const isAdmin = user?.role === 'admin';
  const canManage = isOwner || isPrivileged;
  const canAdminAuthor = isAdmin && !isOwner;

  const formattedDate = new Date(post.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const postMenuItems = [
    {
      label: 'Edit',
      icon: <Edit fontSize="small" />,
      onClick: () => navigate(ROUTES.EDIT_POST(post.id)),
    },
    {
      label: 'Delete',
      icon: <Delete fontSize="small" />,
      onClick: () => deleteMutation.mutate(),
      color: 'error' as const,
      disabled: deleteMutation.isPending,
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Button startIcon={<ArrowBack />} onClick={() => navigate(ROUTES.HOME)} sx={{ mb: 3 }}>
        Back to Discussions
      </Button>

      <Paper elevation={2} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h4" fontWeight={700} sx={{ flexGrow: 1, pr: 2 }}>
            {post.title}
          </Typography>

          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexShrink: 0 }}>
            {canAdminAuthor && (
              <>
                <Tooltip title={`Block ${post.author.username}`}>
                  <span>
                    <Button
                      startIcon={<Block />}
                      variant="outlined"
                      color="warning"
                      size="small"
                      onClick={() => blockMutation.mutate(post.author.id)}
                      disabled={blockMutation.isPending}
                    >
                      Block
                    </Button>
                  </span>
                </Tooltip>
                <Tooltip title={`Unblock ${post.author.username}`}>
                  <span>
                    <Button
                      startIcon={<LockOpen />}
                      variant="outlined"
                      size="small"
                      onClick={() => unblockMutation.mutate(post.author.id)}
                      disabled={unblockMutation.isPending}
                    >
                      Unblock
                    </Button>
                  </span>
                </Tooltip>
              </>
            )}
            {canManage && <ActionsMenu items={postMenuItems} />}
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
          <Avatar
            src={post.author.avatar_url ?? undefined}
            sx={{ width: 28, height: 28, bgcolor: 'secondary.main', fontSize: 13 }}
          >
            {post.author.username[0].toUpperCase()}
          </Avatar>
          <Typography variant="body2" color="text.secondary">
            {post.author.username} · {formattedDate}
          </Typography>
          <VoteButtons
            voteCount={post.vote_count}
            isLiked={post.user_vote === 'up'}
            onToggle={() => voteMutation.mutate()}
            isLoading={voteMutation.isPending}
            disabled={!user}
          />
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>
          {post.content}
        </Typography>
      </Paper>

      <AnswerList postId={post.id} />
    </Container>
  );
};

export default PostDetailPage;
